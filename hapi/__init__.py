from dataclasses import dataclass
from pathlib import Path

from dataclasses import dataclass
import json
import os
from typing import List, Union
from urllib.request import urlretrieve
from tqdm.auto import tqdm

DATA_URL = "https://storage.googleapis.com/hapi-data/hapi.tar.gz"


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
        assert os.path.exists(self._data_dir)


config = HAPIConfig(
    data_dir=os.environ.get(
        "HAPI_DATA_DIR", os.path.join(os.path.join(Path.home(), ".hapi"))
    )
)


def download(data_dir: str = None):
    """Download the HAPI database.

    Args:
        data_dir (str, optional): . Defaults to None, in which case `config.data_dir` is
            used.
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
        tar.extractall(data_dir)


def list():
    import pandas as pd

    df = pd.read_csv(os.path.join(config.data_dir, "tasks", "meta.csv"))
    return df


def get_predictions(
    task: Union[str, List[str]] = None,
    dataset: Union[str, List[str]] = None,
    api: Union[str, List[str]] = None,
    date: Union[str, List[str]] = None,
    include_data: bool = None,
):
    df = list()
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

    if include_data:
        dataset_to_data = {
            dataset: get_data(dataset)
            for dataset in ([dataset] if isinstance(dataset, str) else dataset)
        }

    path_to_preds = {}
    for _, row in tqdm(df.iterrows()):
        path = row["path"]
        preds = json.load(open(os.path.join(config.data_dir, path)))
        if include_data:
            import meerkat as mk

            preds = mk.DataPanel(preds).merge(
                dataset_to_data[row["dataset"]], on="example_id"
            )

        path_to_preds[os.path.splitext(path)[0]] = preds

    return path_to_preds


def get_data(
    dataset: str,
):

    import meerkat as mk

    if dataset == "expw":
        dp = mk.get("expw")

        # remove file extension and add the face_id
        dp["example_id"] = (
            dp["image_name"].str.replace(".jpg", "", regex=False)
            + "_"
            + dp["face_id_in_image"].astype(str)
        )

        return dp
