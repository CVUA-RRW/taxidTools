TaxidTools - A Python Toolkit for Taxonomy

[![Python package](https://github.com/CVUA-RRW/taxidTools/actions/workflows/python-package.yml/badge.svg?branch=main)](https://github.com/CVUA-RRW/taxidTools/actions/workflows/python-package.yml)
![PyPI - License](https://img.shields.io/pypi/l/Django?style=plastic)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/CVUA-RRW/taxidTools?style=plastic)

## Overview

Provides a set of classes and tools to work with taxonomy data.
Although built to work with the NCBI Taxdump files it can also work with other taxonomy definitions.
Currently impelemented:
* Easily load the NCBI taxdump files
* Retrieve name, rank, parent or full ancestry from a unique taxonomic identifier
* Test if a node is parent or descendant of an other 
* Find last common ancestor or consensus node from a list of ids
* Calculate the distance between two nodes
* List all children of a given node
* Re-root Taxonomy
* Format to given ranks

## Requirements

Python >= 3.9 
Optionally some taxonomy definiton files usch as the [Taxdump definition files](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/) from the NCBI server.

## Installation

Clone or copy the github repository to your project for the developement version.

## Contributing

I add new functionnalities as I need them, if you think of a cool new thing you would like to see implemented, post an issue 
or a pull request! 

## License

This project is licensed under a BSD 3-Clauses License, see the LICENSE file for details.

## Author

For questions, problems, suggestions or requests, feel free to contact:

Grégoire Denay, Chemisches- und Veterinär-Untersuchungsamt Rhein-Ruhr-Wupper 

<gregoire.denay@cvua-rrw.de>



