from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    import meerkat as mk

DATASET_INFO = {
    "gmb": "GMB is a named entity recognition dataset. \n\nWe only focus on three types of entities: person, location, and organization.\n\nAll texts are in English. \n\nOne can get access directly from the original source: https://www.kaggle.com/datasets/shoumikgoswami/annotated-gmb-corpus.\n\n\n\n",
    "mtwi": "MTWI is a scene text recognition dataset. \n\nIt was originally from the ICPR MTWI 2018 Challenge. We only adopted the fully annotated images.\n\nSince we cannot release the raw image content, one can get access directly from the original source: https://tianchi.aliyun.com/competition/entrance/231651/information.\n\nWe use the 2014 train/val split.\n\n\n",
    "cmd": "CMD is a spoken command recognition dataset. \n\nIt can be downloaded here: https://pyroomacoustics.readthedocs.io/en/pypi-release/pyroomacoustics.datasets.google_speech_commands.html.\n\nThe label map is as follows.\n\n\n0: zero\n1: one\n2: two\n3: three\n4: four\n5: five\n6: six\n7: seven\n8: eight\n9: nine\n10: bed\n11: bird\n12: cat\n13: dog\n14: down\n15: go\n16: happy\n17: house\n18: left\n19: marvin\n20: no\n21: off\n22: on\n23: right\n24: sheila\n25: stop\n26: tree\n27: up\n28: wow\n29: yes\n30: ' '\n",
    "pascal": "PASCAL is an image recognition dataset. \n\nSince we cannot release the raw image content, one can get access directly from the original source: http://host.robots.ox.ac.uk/pascal/VOC/voc2012/.\n\n",
    "waimai": "WAIMAI.zip contains delivery reviews from https://github.com/SophonPlus/ChineseNlpCorpus/tree/master/datasets/waimai_10k. \n\n\n0: positive \n1: negative",
    "rafdb": "RAFDB is a facial emotion recognition dataset. \n\nSince we cannot release the raw image content, one can get access directly from the original source: http://www.whdeng.cn/raf/model1.html.\n\nWe only use its single-label subset, which contains 15339 face images.\n\n\nThe label map is as follows.\n\n\n\n0: anger\n1: fear\n2: disgusting\n3: happy\n4: sad\n5: surprise\n6: natural",
    "fluent": "FLUENT is a spoken command recognition dataset. \n\nIt can be downloaded here: https://fluent.ai/fluent-speech-commands-a-dataset-for-spoken-language-understanding-research/.\n\n",
    "conll": "CONLL is a named entity recognition dataset. \n\nWe only focus on three types of entities: person, location, and organization.\n\nOne can get access directly from the original source: https://www.kaggle.com/datasets/alaakhaled/conll003-englishversion.\n\n\n\n",
    "shop": "SHOP.zip contains delivery reviews from https://github.com/SophonPlus/ChineseNlpCorpus/tree/master/datasets/online_shopping_10_cats.\n\n\n0: positive \n1: negative",
    "yelp": "YELP20K_raw.zip contains 20,000 samples from the original YELP Challenge. \n\n\n0: positive \n1: negative",
    "afnet": "AFNET is a facial emotion recognition dataset. \n\nSince we cannot release the raw image content, one can get access directly from the original source: http://mohammadmahoor.com/affectnet/.\n\nWe only use the subset with basic emotions. \n\nThe label map is as follows.\n\n\n0: anger\n1: fear\n2: disgusting\n3: happy\n4: sad\n5: surprise\n6: natural",
    "coco": "COCO is an image recognition dataset. \n\nSince we cannot release the raw image content, one can get access directly from the original source: https://cocodataset.org/#download.\n\nWe use the 2014 train/val split.\n\n\n",
    "lsvt": "LSVT is an scene text recognition dataset. \n\nIt was originally from the ICDAR2019 Robust Reading Challenge on Large-scale Street View Text. We only adopted the fully annotated images, which contained 30,000 images.\n\nSince we cannot release the raw image content, one can get access directly from the original source: https://rrc.cvc.uab.es/?ch=16.\n\nWe use the 2014 train/val split.\n\n\n",
    "imdb": "IMDB25K_raw.zip contains 25,000 samples from the original IMDB review dataset. \n\n\n0: positive \n1: negative",
    "zhner": "ZHNER is a named entity recognition dataset. \n\nWe only focus on three types of entities: person, location, and organization.\n\nAll texts are in Chinese. \n\nOne can get access directly from the original source: https://github.com/zjy-ucas/ChineseNER/tree/master/data.\n\n\n\n",
    "rects": "ReCTS is an scene text recognition dataset. \n\nIt was originally from the ICDAR 2019 Robust Reading Challenge on Reading Chinese Text on Signboard.\n\nSince we cannot release the raw image content, one can get access directly from the original source: https://rrc.cvc.uab.es/?ch=12.\n\nWe use the 2014 train/val split.\n\n\n",
    "mir": "MIR is an image recognition dataset. \n\nIt was originally from the MIRFLICKR-25000 dataset, which contains 25,000 images.\n\nSince we cannot release the raw image content, one can get access directly from the original source: https://press.liacs.nl/mirflickr/.\n\nWe use the 2014 train/val split.\n\n\n",
    "ferplus": "FER+ is a facial emotion recognition dataset. \nThe labels can be found here: https://github.com/microsoft/FERPlus\nThe raw images can be found here: https://www.kaggle.com/c/challenges-in-representation-learning-facial-expression-recognition-challenge/data \n\nThe label map is as follows.\n\n0: anger\n1: fear\n2: disgusting\n3: happy\n4: sad\n5: surprise\n6: natural",
    "expw": "EXPW (Expression in-the-Wild) is a facial emotion recognition dataset. \n\nSince we cannot release the raw image content, one can get access directly from the original source: http://mmlab.ie.cuhk.edu.hk/projects/socialrelation/index.html.\n\nThe label map is as follows.\n\n\n\n0: anger\n1: fear\n2: disgusting\n3: happy\n4: sad\n5: surprise\n6: natural",
    "digit": "DIGIT is a spoken digit recognition dataset. \n\nIt can be downloaded here: https://github.com/Jakobovski/free-spoken-digit-dataset.\n\nWhen we downloaded it, only data produced by four speakers were avaiable. This led to 2000 samples in our experiments.\n\nThe label map is as follows.\n\n\n0: zero\n1: one\n2: two\n3: three\n4: four\n5: five\n6: six\n7: seven\n8: eight\n9: nine",
    "amnist": "AMNIST is a spoken digit recognition dataset. \n\nIt can be downloaded here: https://github.com/soerenab/AudioMNIST.\n\nThe label map is as follows.\n\n\n0: zero\n1: one\n2: two\n3: three\n4: four\n5: five\n6: six\n7: seven\n8: eight\n9: nine",
}


def get_dataset(
    dataset: str,
) -> "mk.DataPanel":
    """ Load a dataset from the Meerkat registry. If the dataset is not downloaded,
    it will be downloaded automatically. Not all datasets in HAPI are supported: 
    If the dataset is not yet available through the Meerkat Dataset Registry, a `
    ValueError` will be raised containing instructions for manually downloading the 
    dataset. For example:

    .. code-block:: python

        >> dp = hapi.get_dataset("cmd")

        ValueError: Data download for 'cmd' not yet available for download through the  HAPI Python API. Please download manually following the instructions below: 
        
        CMD is a spoken command recognition dataset. 

        It can be downloaded here: https://pyroomacoustics.readthedocs.io/en/...

    Args:
        dataset (str): The name of the dataset. 

    Raises:
        ValueError: If the dataset is not yet included in the registry. The ValueError
            will contain instructions for manually downloading the dataset.

    Returns:
        mk.DataPanel: A Meerkat DataPanel holding the dataset. A Meerkat DataPanel is a
            DataFrame-like object that houses the dataset. See the Meerkat User Guide 
            for more information.  The DataPanel will have  an "example_id" column that 
            corresponds to the "example_id" key in the outputs of 
            `hapi.get_predictions()` and `hapi.get_labels()`. 
    """

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

    elif dataset == "pascal":
        dp = mk.get("pascal")
        dp["example_id"] = dp["id"]
        dp.remove_column("id")
        return dp

    elif dataset == "coco":
        dp = mk.get("coco")
        dp["example_id"] = dp["coco_url"].apply(
            lambda x: os.path.splitext(os.path.basename(x))[0]
        )
        dp.remove_column("id")
        return dp

    elif dataset == "mir":
        dp = mk.get("mirflickr")
        dp["example_id"] = dp["id"]
        dp.remove_column("id")
        return dp

    elif dataset in DATASET_INFO:
        raise ValueError(
            f"Data download for '{dataset}' not yet available for download through the "
            " HAPI Python API. Please download manually following the instructions "
            "below: \n \n"
            f"{DATASET_INFO[dataset]}"
        )
    else:
        raise ValueError(
            f"Unknown dataset '{dataset}'. Please pass one of the following: "
            f"{list(DATASET_INFO.keys())}"
        )
