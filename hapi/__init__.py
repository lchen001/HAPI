from dataclasses import dataclass
from pathlib import Path

from dataclasses import dataclass
import json
import os
from typing import Dict, List, Union
from urllib.request import urlretrieve

from tqdm.auto import tqdm
import pandas as pd

from .dataset import get_dataset

DATA_URL = "https://storage.googleapis.com/hapi-data/hapi.tar.gz"

__all__ = ["get_dataset", "download", "get_predictions", "get_labels", "summary"]


@dataclass
class HAPIConfig:
    def __init__(self, data_dir: str, *args, **kwargs):
        self._data_dir = data_dir
        super().__init__(*args, **kwargs)

    @property
    def data_dir(self):
        if self._data_dir is None or not os.path.exists(
            os.path.join(self._data_dir, "tasks")
        ):
            raise ValueError(
                "Set `data_dir` in the hapi config to point to the directory where "
                "you've downloaded hapi `hapi.config.data_dir = /path/to/data`. If you "
                "haven't downloaded the data yet, set `hapi.config.data_dir` to point  "
                "to the directory where you want to download the data to and call "
                "`hapi.download()`."
            )
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir: str):
        self._data_dir = data_dir
        os.makedirs(self._data_dir, exist_ok=True)
        assert os.path.exists(self._data_dir)


config = HAPIConfig(
    data_dir=os.environ.get(
        "HAPI_DATA_DIR", os.path.join(os.path.join(Path.home(), ".hapi"))
    )
)


def download(data_dir: str = None) -> str:
    """Download the HAPI database.

    The database is stored in a GCP bucket named hapi-data. All model predictions are
    stored in hapi.tar.gz (Compressed size: 205.3MB, Full size: 1.2GB). This function
    downloads the archive and extracts it.

    Args:
        data_dir (str, optional): Directory to download. Defaults to None, in which case
        `config.data_dir` is used. If `config.data_dir` is not set, then the default
        directory is used: `~/.hapi`.

    Returns:
        str: The path to the downloaded data.
    """
    if data_dir is None:
        data_dir = config._data_dir

    os.makedirs(data_dir, exist_ok=True)

    urlretrieve(
        DATA_URL,
        os.path.join(data_dir, "hapi.tar.gz"),
    )

    # extract the tarball
    import tarfile

    with tarfile.open(os.path.join(data_dir, "hapi.tar.gz")) as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar, data_dir)

    return data_dir


def get_predictions(
    task: Union[str, List[str]] = None,
    dataset: Union[str, List[str]] = None,
    api: Union[str, List[str]] = None,
    date: Union[str, List[str]] = None,
    include_dataset: bool = None,
) -> Dict[str, List[Dict]]:
    """Load API predictions into memory.

    Use the `task`, `dataset`, `api`, and `date` parameters to filter to a subset of
    the database. If more than one of these parameters is specified, the results will
    be filtered to include only those rows that match all of the specified filters
    (i.e. we apply AND logic).

    Args:
        task (Union[str, List[str]]): The task(s) to include. If None, all tasks are
            loaded.  Default is None. Use ``hapi.summary()["task"].unique()`` to see
            options.
        dataset (Union[str, List[str]]): The dataset(s) to include. If None, all
            datasets are loaded. Default is None. Use
            ``hapi.summary()["dataset"].unique()`` to see options.
        api (Union[str, List[str]]): The API(s) to include. If None, all APIs are
            loaded. Default is None. Use ``hapi.summary()["api"].unique()`` to see
            options.
        date (Union[str, List[str]]): The date(s) to include in format "y-m-d". For
            example, "20-03-29". If None, all dates are loaded. Default is None.
        include_dataset (bool, optional): If True, the raw dataset is downloaded and 
            loaded using `hapi.get_dataset()`. The dataset is then merged with the
            predictions on the "example_id" column. Default is False.

    Returns:
        Dict[str, List[Dict]]: A dictionary mapping keys in the format
        "{task}/{dataset}/{api)/{date}" (e.g. "scr/command/google_scr/20-03-29") to a
        list of dictionaries, each representing one prediction. These dictionaries
        include keys "confidence", "predicted_label", and "example_id". For example,

        .. code-block:: python

            {
                "scr/command/google_scr/20-03-29": [
                    {
                        'confidence': 0.9128385782,
                        'predicted_label': 0,
                        'example_id': 'COMMAND_004ae714_nohash_0.wav'
                    },
                ],
                ...
            }
    """
    df = summary()
    if task is not None:
        if isinstance(task, str):
            df = df[df["task"] == task]
        else:
            df = df[df["task"].isin(task)]

    if dataset is not None:
        if isinstance(dataset, str):
            df = df[df["dataset"] == dataset]
        else:
            df = df[df["dataset"].isin(dataset)]

    if api is not None:
        if isinstance(api, str):
            df = df[df["api"] == api]
        else:
            df = df[df["api"].isin(api)]

    if date is not None:
        if isinstance(date, str):
            df = df[df["date"] == date]
        else:
            df = df[df["date"].isin(date)]

    if include_dataset:
        dataset_to_data = {
            dataset: get_dataset(dataset)
            for dataset in ([dataset] if isinstance(dataset, str) else dataset)
        }

    path_to_preds = {}
    for _, row in tqdm(df.iterrows(), total=len(df)):
        path = row["path"]
        preds = json.load(open(os.path.join(config.data_dir, "tasks", path)))

        if include_dataset:
            import meerkat as mk

            preds = mk.DataPanel(preds).merge(
                dataset_to_data[row["dataset"]], on="example_id"
            )

        path_to_preds[os.path.splitext(path)[0]] = preds

    return path_to_preds


def get_labels(
    task: Union[str, List[str]] = None,
    dataset: Union[str, List[str]] = None,
) -> Dict[str, List[Dict]]:
    """Load labels into memory.

    Use the `task` and `dataset` parameters to filter to a subset of the database.
    If more than one of these parameters is specified, the results will be filtered
    to include only those rows that match all of the specified filters (i.e. we apply
    AND logic).

    Args:
        task (Union[str, List[str]]): The task(s) to include. If None, all tasks are
            loaded.  Default is None. Use ``hapi.summary()["task"].unique()`` to see
            options.
        dataset (Union[str, List[str]]): The dataset(s) to include. If None, all
            datasets are loaded. Default is None. Use
            ``hapi.summary()["dataset"].unique()`` to see options.

    Returns:
        Dict[str, List[Dict]]: A dictionary mapping keys in the format
        "{task}/{dataset}" (e.g. "scr/command") to a
        list of dictionaries, each representing one label. These dictionaries
        include keys "label", "example_id", and "confidence". For example,

        .. code-block:: python

            {
                "scr/command": [
                    {
                        'true_label': 0,
                        'example_id': 'COMMAND_004ae714_nohash_0.wav',
                    },
                ],
                ...
            }
    """
    df = summary()
    df = df[["task", "dataset"]].drop_duplicates()
    if task is not None:
        if isinstance(task, str):
            df = df[df["task"] == task]
        else:
            df = df[df["task"].isin(task)]

    if dataset is not None:
        if isinstance(dataset, str):
            df = df[df["dataset"] == dataset]
        else:
            df = df[df["dataset"].isin(dataset)]

    path_to_labels = {}
    for _, row in tqdm(df.iterrows(), total=len(df)):
        path = os.path.join(row["task"], row["dataset"])
        labels = json.load(
            open(os.path.join(config.data_dir, "tasks", path, "labels.json"))
        )
        path_to_labels[path] = labels
    return path_to_labels


def summary() -> pd.DataFrame:
    """Summarize the HAPI database.

    Returns:
        pd.DataFrame: A dataframe where each row corresponds to one instance of API
            predictions (i.e. predictions from a single api on a single dataset on a
            single date). The dataframe contains the following columns: "task",
            "dataset", "api", "date", "path", and "cost_per_10k".
    """
    df = pd.read_csv(os.path.join(config.data_dir, "tasks", "meta.csv"))
    return df
