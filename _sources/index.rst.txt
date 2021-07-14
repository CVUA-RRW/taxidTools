taxidTools: A Python Toolkit for Taxonomy
=========================================

.. image:: https://img.shields.io/github/v/release/CVUA-RRW/taxidTools   :alt: GitHub release (latest by date)

.. image:: https://img.shields.io/pypi/l/Django?style=plastic   :alt: License

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
   
   Taxonomy module <taxidTools.Taxonomy.rst>
   Lineage module <taxidTools.Lineage>
   Node module <taxidTools.Node>
   utils module <taxidTools.utils>

Changes
-------

.. toctree::
   :maxdepth: 2
   
   history