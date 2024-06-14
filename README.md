
[![CD/CI](https://github.com/CVUA-RRW/taxidTools/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/CVUA-RRW/taxidTools/actions/workflows/python-package.yml)
[![PyPI - License](https://img.shields.io/pypi/l/Django?style=flat)](LICENSE)
[![GitHub release (latest by date)](https://img.shields.io/github/v/release/CVUA-RRW/taxidTools?logo=GitHub)](https://github.com/CVUA-RRW/taxidtools/releases)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/taxidtools.svg?logo=Conda-Forge)](https://anaconda.org/conda-forge/taxidtools)
[![Pypi Version](https://img.shields.io/pypi/v/taxidTools?style=flat?logo=pypi)](https://pypi.org/project/taxidTools/)
[![Docker Image Version](https://img.shields.io/docker/v/gregdenay/taxidtools?logo=Docker&label=DockerHub)](https://hub.docker.com/r/gregdenay/taxidtools/tags)
[![DOI](https://zenodo.org/badge/300595196.svg)](https://zenodo.org/doi/10.5281/zenodo.5094583)

# TaxidTools - A Python Toolkit for Taxonomy

**taxidTools** is a Python library to handle Taxonomy definitions.

## Highlights

* Load taxonomy defintions for the NCBI's taxdump files
* Prune, filter, and normalize branches
* Save as JSON for later use
* Determine consensus, last common ancestor, or distances
* Retrieve ancestries or list descendants

## Installation

With `pip`:

```bash
pip install taxidtools
```

With `conda`:

```bash
conda install -c conda-forge taxidtools
```

With `docker`:

```bash
docker pull gregdenay/taxidtools
```

## Quickstart

With the [NCBI's taxdump files](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/) installed locally:

```python
>>> import taxidTools as txd
>>> ncbi = txd.read_taxdump('nodes.dmp', 'rankedlineage.dmp', 'merged.dmp')
>>> tax.getName('9606')
'Homo sapiens'
>>> lineage = tax.getAncestry('9606')
>>> lineage.filter()
>>> [node.name for node in lineage]
['Homo sapiens', 'Homo', 'Hominidae', 'Primates', 'Mammalia', 'Chordata', 'Metazoa']
>>> tax.lca(['9606', '10090']).name
'Euarchontoglires'
>>> tax.distance('9606', '10090')
18
```

## Documentation

Full documentation is hosted on the [homepage](https://cvua-rrw.github.io/taxidtools/)

## Cite us

If you use taxidTools for your reasearch, you can cite it using the 
DOI at the top of this page.
