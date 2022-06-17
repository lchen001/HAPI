from dataclasses import dataclass


from dataclasses import dataclass
import json
import os
from typing import List, Union
from tqdm import tqdm


@dataclass
class HAPIConfig:
    def __init__(self, data_dir: str, *args, **kwargs):
        self._data_dir = data_dir
        super().__init__(*args, **kwargs)

    @property
    def data_dir(self):
        if self._data_dir is None or not os.path.exists(self._data_dir):
            raise ValueError(
                "Set `data_dir` in the hapi config to point to the directory where "
                "you've downloaded hapi `hapi.config.data_dir = /path/to/data`."
            )
        return self._data_dir

    @data_dir.setter
    def data_dir(self, data_dir: str):
        if not os.path.exists(os.path.join(data_dir, "meta.csv")):
            raise ValueError(
                "Trying to set `data_dir` to a directory that doesn't "
                "contain `meta.csv`. Are you sure this is the directory where you've "
                "downloaded hapi?"
            )
        self._data_dir = data_dir
        assert os.path.exists(self._data_dir)


config = HAPIConfig(data_dir=os.environ.get("HAPI_DATA_DIR", None))


def download():
    pass


def list():
    import pandas as pd

    df = pd.read_csv(os.path.join(config.data_dir, "meta.csv"))
    return df


def get_predictions(
    task: Union[str, List[str]] = None,
    dataset: Union[str, List[str]] = None,
    api: Union[str, List[str]] = None,
    date: Union[str, List[str]] = None,
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

    preds = {}
    for path in tqdm(df["path"]):
        preds[os.path.splitext(path)[0]] = json.load(
            open(os.path.join(config.data_dir, path))
        )
    
    return preds

def get_dataset(dataset: str):

    if dataset == "pascal":

        pass 