import os
import tarfile
import pandas as pd
import json
import meerkat as mk
import re
from google.cloud import storage
from pyrsistent import l
from tqdm import tqdm

DATASET_TO_TASK = {
    "coco": "mic",
    "mir": "mic",
    "pascal": "mic",
    "gmb": "ner",
    "conll": "ner",
    "zhner": "ner",
    "lsvt": "str",
    "rects": "str",
    "mtwi": "str",
    "expw": "fer",
    "ferplus": "fer",
    "rafdb": "fer",
    "afnet": "fer",
    "imdb": "sa",
    "waimai": "sa",
    "yelp": "sa",
    "shop": "sa",
    "digit": "scr",
    "command": "scr",
    "amnist": "scr",
    "fluent": "scr",
}


DATA_DIR = "/Users/eyubogln/code/hapi/data/legacy"

DST_DIR = "/Users/eyubogln/code/hapi/data/tasks"

BUCKET_NAME = "hapi-data"


def get_structured_predictions(
    predictions_dir: str, model: str, include_original: bool = False
):

    # regex pattern for converting from came
    pattern = re.compile(r"(?<!^)(?=[A-Z])")

    # load in column with all the paths to images
    dp = {}
    for column in ["ImageName", "Context", "Confidence"]:
        path = os.path.join(predictions_dir, f"{model}_{column}.txt")
        if not os.path.exists(path):
            continue
        column = pattern.sub("_", column).lower()
        dp[column] = pd.read_csv(path, names=[column], index_col=False)[column]

    # create the dp to be output, create a new column for image name
    dp = mk.DataPanel(dp)
    dp["example_id"] = dp["image_name"]
    for suffix in [".jpg", ".jpeg", ".png", ".txt"]:
        dp["example_id"] = dp["example_id"].str.removesuffix(suffix)

    # match predicted labels to rows of the dataset by performing a merge
    columns = (
        ["PredictedLabel", "OriginalPredictedLabel"]
        if include_original
        else ["PredictedLabel"]
    )
    for column in columns:
        path = os.path.join(predictions_dir, f"{model}_{column}.txt")
        column = pattern.sub("_", column).lower()

        out = json.load(open(path, "rb"))
        other = mk.DataPanel(
            {"example_id": list(out.keys()), column: list(out.values())}
        )
        predicted_labels = dp.merge(other, on="example_id", validate="one_to_one")[
            column
        ]
        assert len(predicted_labels) == len(dp)

        # add the original labels to the output dp
        dp[column] = [
            [pred["transcription"] for pred in example] for example in predicted_labels
        ]
    dp.remove_column("image_name")

    return dp


def get_class_predictions(predictions_dir: str, model: str):
    # regex pattern for converting from came
    pattern = re.compile(r"(?<!^)(?=[A-Z])")

    # load in column with all the paths to images
    dp = {}
    for column in ["ImageName", "Context", "Confidence", "PredictedLabel"]:
        path = os.path.join(predictions_dir, f"{model}_{column}.txt")
        if not os.path.exists(path):
            continue
        column = pattern.sub("_", column).lower()
        dp[column] = pd.read_csv(path, names=[column], index_col=False)[column]

    # create the dp to be output, create a new column for image name
    dp = mk.DataPanel(dp)
    dp["example_id"] = dp["image_name"]
    for suffix in [".jpg", ".jpeg", ".png", ".txt"]:
        dp["example_id"] = dp["example_id"].str.removesuffix(suffix)

    dp.remove_column("image_name")

    return dp


def get_structured_labels(
    predictions_dir: str, model: str, include_original: bool = False
):
    # regex pattern for converting from came
    pattern = re.compile(r"(?<!^)(?=[A-Z])")

    # load in column with all the paths to images
    dp = {}
    for column in ["ImageName"]:
        path = os.path.join(predictions_dir, f"{model}_{column}.txt")
        if not os.path.exists(path):
            continue
        column = pattern.sub("_", column).lower()
        dp[column] = pd.read_csv(path, names=[column], index_col=False)[column]

    # create the dp to be output, create a new column for image name
    dp = mk.DataPanel(dp)
    dp["example_id"] = dp["image_name"]
    for suffix in [".jpg", ".jpeg", ".png", ".txt"]:
        dp["example_id"] = dp["example_id"].str.removesuffix(suffix)

    # match predicted labels to rows of the dataset by performing a merge
    columns = ["TrueLabel"]
    for column in columns:
        path = os.path.join(predictions_dir, f"{model}_{column}.txt")
        column = pattern.sub("_", column).lower()

        out = json.load(open(path, "rb"))
        other = mk.DataPanel(
            {"example_id": list(out.keys()), column: list(out.values())}
        )
        predicted_labels = dp.merge(other, on="example_id", validate="one_to_one")[
            column
        ]
        assert len(predicted_labels) == len(dp)

        # add the original labels to the output dp
        dp[column] = [
            [pred["transcription"] for pred in example] for example in predicted_labels
        ]
    dp.remove_column("image_name")
    return dp


def get_class_labels(predictions_dir: str, model: str):
    # regex pattern for converting from came
    pattern = re.compile(r"(?<!^)(?=[A-Z])")

    # load in column with all the paths to images
    dp = {}
    for column in ["ImageName", "TrueLabel"]:
        path = os.path.join(predictions_dir, f"{model}_{column}.txt")
        if not os.path.exists(path):
            continue
        column = pattern.sub("_", column).lower()
        dp[column] = pd.read_csv(path, names=[column], index_col=False)[column]

    # create the dp to be output, create a new column for image name
    dp = mk.DataPanel(dp)
    dp["example_id"] = dp["image_name"]
    for suffix in [".jpg", ".jpeg", ".png", ".txt"]:
        dp["example_id"] = dp["example_id"].str.removesuffix(suffix)
    dp.remove_column("image_name")

    return dp


if __name__ == "__main__":
    meta = []
    for predictions_dir in tqdm(os.listdir(DATA_DIR)):
        if predictions_dir.startswith("."):
            # ignore hiddne files
            continue
        _, run_id = predictions_dir.split("_", 1)
        predictions_dir = os.path.join(DATA_DIR, predictions_dir)
        dataset, date = run_id.split("20", 1)
        dataset = dataset.lower()
        date = f"{date[:2]}-{date[2:4]}-{date[4:]}"

        models = set([f.split("_")[0] for f in os.listdir(predictions_dir)])

        task = DATASET_TO_TASK[dataset]

        old_meta_df = pd.read_csv(os.path.join(predictions_dir, "meta.csv"))
        model_to_api = {
            f"Model{index}": f"{api.lower()}_{task}"
            for index, api in zip(old_meta_df["Index"], old_meta_df["MLaaS(API)"])
        }

        # get column starting with Cost per 10k
        cost_column = [
            col for col in old_meta_df.columns if col.startswith("Cost per 10k")
        ][0]
        model_to_cost = {
            f"Model{index}": cost
            for index, cost in zip(old_meta_df["Index"], old_meta_df[cost_column])
        }

        for model in models:
            if model not in model_to_api:
                continue
            labels_path = os.path.join(DST_DIR, task, dataset, "labels.json")
            if not os.path.exists(labels_path):
                if task in ["ner", "mic", "str"]:
                    dp = get_structured_labels(predictions_dir, model)
                else:
                    dp = get_class_labels(predictions_dir, model)
                dp.to_pandas().to_json(labels_path, orient="records")

            api = model_to_api[model]

            if task in ["ner", "mic", "str"]:
                dp = get_structured_predictions(predictions_dir, model)
            else:
                dp = get_class_predictions(predictions_dir, model)

            new_dir = os.path.join(
                DST_DIR,
                task,
                dataset,
                api,
            )
            os.makedirs(new_dir, exist_ok=True)

            path = os.path.join(new_dir, f"{date}.json")
            dp.to_pandas().to_json(path, orient="records")

            meta.append(
                {
                    "task": task,
                    "dataset": dataset,
                    "api": api,
                    "date": date,
                    "path": os.path.relpath(path, DST_DIR),
                    "cost_per_10k": model_to_cost[model],
                }
            )

    pd.DataFrame(meta).to_csv(os.path.join(DST_DIR, "meta.csv"), index=False)

    with tarfile.open(DST_DIR + ".tar.gz", "w:gz") as tar:
        tar.add(DST_DIR, arcname=os.path.basename(DST_DIR))

    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob("hapi.tar.gz")
    blob.upload_from_filename(DST_DIR + ".tar.gz")
