
<div align="center">
    <img src="docs/assets/banner.png" height=150 alt="banner"/>

-----
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/data-centric-ai/dcbench/CI)
![GitHub](https://img.shields.io/github/license/data-centric-ai/dcbench)
[![Documentation Status](https://readthedocs.org/projects/dcbench/badge/?version=latest)](https://dcbench.readthedocs.io/en/latest/?badge=latest)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dcbench)](https://pypi.org/project/dcbench/)
[![codecov](https://codecov.io/gh/data-centric-ai/dcbench/branch/main/graph/badge.svg?token=MOLQYUSYQU)](https://codecov.io/gh/data-centric-ai/dcbench)
[![standard-readme compliant](https://img.shields.io/badge/readme%20style-standard-brightgreen.svg?style=flat-square)](https://github.com/RichardLitt/standard-readme)
[![License](https://img.shields.io/badge/license-Apache%202-blue.svg)](LICENSE)



A longitudinal database of ML API predictions. 

[**Getting Started**](#%EF%B8%8F-quickstart)
| [**What is HAPI?**](#-what-is-dcbench)
| [**Docs**](https://dcbench.readthedocs.io/en/latest/index.html)
| [**Contributing**](CONTRIBUTING.md)
| [**Website**](https://www.datacentricai.cc/)
| [**About**](#%EF%B8%8F-about)
</div>


## ⚡️ Quickstart
 The full data can be downloaded [Here](https://drive.google.com/drive/folders/1jK6KywfUbh3T3SorP18nAZDhES1xZm4p?usp=sharing)


```bash
pip install hapi
```
> Optional: some parts of Meerkat rely on optional dependencies. If you know which optional dependencies you'd like to install, you can do so using something like `pip install hapi[dev]` instead. See setup.py for a full list of optional dependencies.

> Installing from dev: `pip install "hapi[dev] @ git+https://github.com/data-centric-ai/dcbench@main"`

Using a Jupyter notebook or some other interactive environment, you can import the library  
and explore the data-centric problems in the benchmark:

```python
import hapi
```
To learn more, follow the [walkthrough](https://dcbench.readthedocs.io/en/latest/intro.html#api-walkthrough) in the docs. 


## 💡 What is HAPI?
History of APIs (HAPI) is a large-scale, longitudinal database of commercial ML API predictions. It contains 1.7 million predictions spanning APIs from Amazon, Google, IBM, Microsoft. The database include diverse machine learning tasks including image tagging, speech recognition and text mining from 2020 to 2022.


## 📚 Docs

The folder structure:
```
tasks/
    ner/
        conll/
            google_ner_20200.
        zhner/
        ...
    str/
    asr/
```

## ✉️ About
`HAPI` was developed at Stanford in the Zou Group. Reach out to Lingjiao Chen (lingjiao [at] stanford [dot] edu) and Sabri Eyuboglu (eyuboglu [at] stanford [dot] edu) if you would like to get involved!
