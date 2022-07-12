
<div align="center">
    <img src="docs/assets/banner.png" height=120 alt="banner"/>

-----


[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)



A longitudinal database of ML API predictions. 

[**Getting Started**](#%EF%B8%8F-quickstart)
| [**Website**](https://hapi-explore.github.io/)
| [**Contributing**](CONTRIBUTING.md)
| [**About**](#%EF%B8%8F-about)
</div>


## 💡 What is HAPI?
History of APIs (HAPI) is a large-scale, longitudinal database of commercial ML API predictions. It contains 1.7 million predictions collected from 2020 to 2022 and spanning APIs from Amazon, Google, IBM, and Microsoft. The database include diverse machine learning tasks including image tagging, speech recognition and text mining.


## 💾  Downloading
The database is stored in a GCP bucket named [`hapi-data`](https://console.cloud.google.com/storage/browser/hapi-data). All model predictions are stored in [`hapi.tar.gz`](https://storage.googleapis.com/hapi-data/hapi.tar.gz) (Compressed size: `205.3MB`, Full size: `1.2GB`). 
    
From the command line, you can download and extract the predictions with: 
```bash
    wget https://storage.googleapis.com/hapi-data/hapi.tar.gz && tar -xzvf hapi.tar.gz 
```
or use our python package as described below... 

## ⚡️ Quickstart
We provide a lightweight python package for getting started with HAPI. 
```bash
pip install hapi @ git+https://github.com/lchen001/hapi@main
```

Import the library and specify the path to downloaded predictions (as described [above](#💾-downloading)). 

```python
import hapi
hapi.config.data_dir = "/path/to/data
```

We can list the available APIs, datasets, and tasks with `hapi.list()`. This returns a [Pandas DataFrame](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html) with columns `task, dataset, api, date, path, cost_per_10k`. 
```python
df = hapi.list()
```

To load the predictions into memory we use `hapi.get_predictions()`. The keyword arguments allow us to load predictions for a subset of tasks, datasets, apis and/or dates. 
```python
predictions =
hapi.get_predictions(task="mic", dataset="pascal", api=["google_mic", "ibm_mic"])
```

By default, the predictions are returned as a dictionary mapping from `"{task}/{dataset}/{api}/{date}"` to lists of dictionaries, each with keys `"id"`, `"prediction"`, `"confidence"`. For example,
```python
{
    "mic/pascal/google_mic/20-10-28": [
        {
            'image_name': '2011_000494.jpg',
            'confidence': 0.9798267782,
            'example_id': '2011_000494',
            'predicted_label': ['bird', 'bird']
        },
        ...
    ],
    "mic/pascal/microsoft_mic/20-10-28": [...],
    ...
}
```



## ✉️ About
`HAPI` was developed at Stanford in the Zou Group. Reach out to Lingjiao Chen (lingjiao [at] stanford [dot] edu) and Sabri Eyuboglu (eyuboglu [at] stanford [dot] edu) if you would like to get involved!
