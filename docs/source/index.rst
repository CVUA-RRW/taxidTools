taxidTools: A Python Toolkit for Taxonomy
=========================================

.. image:: https://img.shields.io/pypi/l/Django?style=flat
   :alt: License

.. image:: https://img.shields.io/pypi/v/taxidTools
   :alt: PyPI

.. image:: https://img.shields.io/conda/vn/conda-forge/taxidtools.svg
   :target: https://anaconda.org/conda-forge/taxidtools
   :alt: conda-forge

.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.5556006.svg
   :target: https://doi.org/10.5281/zenodo.5556006
   :alt: DOI


**taxidTools** is a Python library to handle Taxonomy definitions.

-------------------

**Usage example**::

    >>> import taxidTools
    >>> tax = taxidTools.Taxonomy.from_taxdump("nodes.dmp", "rankedlineage.dmp")
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

**taxidTools** allows you to easily handle complex taxonomies
from different sources and perform common operations such as 
consensus determination, finding a last common ancestor or 
calculating node distances. 

User Guide
----------

Get it installed and jump right in:

.. toctree::
   :maxdepth: 2
   
   Installation guide <usage/install>
   Quickstart <usage/quickstart>
   Advanced usage <usage/advanced>

API Documentation
-----------------

Source code documentation.

.. toctree::
   :maxdepth: 2
   
   Taxonomy module <taxidTools.Taxonomy>
   Lineage module <taxidTools.Lineage>
   Node module <taxidTools.Node>
   factories module <taxidTools.factories>
   utils module <taxidTools.utils>

Cite us
-------

If you are using taxidTools for your reasearch, cite the latest version from `Zenodo <https://doi.org/10.5281/zenodo.5556006)>`_.

Changes
-------

.. toctree::
   :maxdepth: 2
   
   history