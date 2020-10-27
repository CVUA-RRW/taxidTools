# TaxidTools

A Python module for common operations on NCBIs Taxdump files:
Provides the Taxdump class to work with the NCBI Taxonomy informations from the taxdump files.
Supports conversion of taxid numbers to rank or names, finding parents, retrieving ancestry and finding lowest common 
ancestor from a list of taxids.

## Requirements

Taxidtools is supported and tested on Python 3.7, it does not require external libraries.

You will need the [Taxdump definition files](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/) from the NCBI server.

## Installation

Clone or copy the github repository to your project.
Taxidtools is not available as a python package as of yet.

## Documentation

This module implements the Taxdump class. Instance of the class store the taxonomic information contained in the NCBI'see
taxdump files: rankedlineage.dmp and nodes.dmp.

### Usage

#### Taxdump objects

Start by creating a instance of Taxdump:

```python
>>> from taxidTools import Taxdump 

>>> txd = Taxdump('/path/to/ncbi/rankedlineage.dmp', '/path/to/ncbi/nodes.dmp')
```

Taxdump objects are basically immutable dictionnaries. However items should be accessed via specific methods.

```python
>>> len(txd)
2256125
>>> len(txd.values())
2256125
>>> len(txd.items())
2256125
>>> len(txd.keys())
2256125
>>> txd['9606']
('Homo sapiens', 'species', '9605') # values are stored as (name, rank, parent_taxid)
>>> txd.pop()
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Taxdump' object has no attribute 'pop'
```

#### Retrieving basic node information

You can then retrieve name, taxid and rank informations:

```python
# Method names should be self-explanatory
>>> txd.getName('9606')
'Homo sapiens'
>>> txd.getRank('9606')
'species'
>>> txd.getParent('9606')
'9605'
>>> txd.getTaxid('Homo sapiens')
'9606'
```

#### Retrieving Ancestry

Several methods are implemented to work with ancestry:

```python
# Test relationships:
>>> txd.isAncestorOf('9605', '9606')
True
>>> txd.isAncestorOf('9606', '9605')
False
>>> txd.isDescendantOf('9606', '9605')
True
>>> txd.isDescendantOf('9605', '9606')
False
# Note that nodes are not ancestors nor descendants of themselves:
>>> txd.isDescendantOf('9605', '9605')
False
>>> txd.isAncestorOf('9605', '9605')
False

# Retrieve the full ancestry:
>>> txd.getAncestry('9606') 
['9606', '9605', '207598', '9604', '314295', '9526', '314293', '376913', '9443', '314146', '1437010', '9347', '32525', 
'40674', '32524', '32523', '1338369', '8287', '117571', '117570', '7776', '7742', '89593', '7711', '33511', '33213', '6072', 
'33208', '33154', '2759', '131567', '1']

# List comprehension can get you anywhere:
>>> [txd.getName(node) for node in txd.getAncestry('9606')]
['Homo sapiens', 'Homo', 'Homininae', 'Hominidae', 'Hominoidea', 'Catarrhini', 'Simiiformes', 'Haplorrhini', 'Primates', 
'Euarchontoglires', 'Boreoeutheria', 'Eutheria', 'Theria', 'Mammalia', 'Amniota', 'Tetrapoda', 'Dipnotetrapodomorpha', 
'Sarcopterygii', 'Euteleostomi', 'Teleostomi', 'Gnathostomata', 'Vertebrata', 'Craniata', 'Chordata', 'Deuterostomia', 
'Bilateria', 'Eumetazoa', 'Metazoa', 'Opisthokonta', 'Eukaryota', 'cellular organisms', 'root']
>>> [txd.getName(node)
...     for node in txd.getAncestry('9606')
...     if txd.getRank(node) in ['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom']
...     ]
['Homo sapiens', 'Homo', 'Hominidae', 'Primates', 'Mammalia', 'Chordata', 'Metazoa']
```

#### Inputs as list

Methods that take a name of taxid as an input also handle list of inputs. 
The method's output will always match the input:

```python
# The methods will also handle list input. Note the output will match input type:
>>> txd.getName(['9606', '10090', '4641'])
['Homo sapiens', 'Mus musculus', 'Musa acuminata']
>>> txd.getTaxid(['Bos', 'Homo'])
['9903', '9605']
>>> txd.isDescendantOf(['9606', '10090', '4641'], '9605')
[True, False, False]
# Output always matches input:
>>> txd.getName(['9606'])
['Homo sapiens']
```

#### Filter specific ranks

it is also possible to filter specific ranks:

```python
 >>> txd.filterRanks(txd.getAncestry('9606'), ['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom'])
['9606', '9605', '9604', '9443', '40674', '7711', '33208']
# Using this considerably simplifies the list comprehension above:
>>> txd.getName(
...             txd.filterRanks(
...                     txd.getAncestry('9606'),
...             ['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom']
...             )
...     )
['Homo sapiens', 'Homo', 'Hominidae', 'Primates', 'Mammalia', 'Chordata', 'Metazoa']
# Be careful ranks are not unique!
>>> txd.getName(
...             txd.filterRanks(
...                     txd.getAncestry('9606'), ['clade', 'no rank']))
['Boreoeutheria', 'Eutheria', 'Theria', 'Amniota', 'Tetrapoda', 'Dipnotetrapodomorpha', 'Euteleostomi', 'Teleostomi', 'Gnathostomata', 'Vertebrata', 'Deuterostomia', 'Bilateria', 'Eumetazoa', 'Opisthokonta', 'cellular organisms', 'root']

```

#### Find lowest common ancestor node

Finding the lowest common ancestor from a list of taxids is straightforward:

```python
>>> txd.lowestCommonNode(['9606', '10090'])
'314146'
>>> txd.lowestCommonNode(['9606', '4641'])
'2759'
```

if you want to find the lowest common node at a specific rank, you will have to use a bit of magic:

```python
>>> txd.getName(txd.lowestCommonNode(['9606', '10090']))
'Euarchontoglires'
>>> txd.getRank(txd.lowestCommonNode(['9606', '10090']))
'superorder'

>>> txd.getName(
...     txd.filterRanks(
...             txd.getAncestry(
...                     txd.lowestCommonNode(['9606', '10090'])
...             ), ['class'])
... )
['Mammalia']
```

## Contributing

I add new functionnalities as I need them, if you think of a cool new thing you would like to see implemented, post an issue 
or a pull request! 

## License

This project is licensed under a BSD 3-Clauses License, see the LICENSE file for details.

## Author

For questions about the pipeline, problems, suggestions or requests, feel free to contact:

Grégoire Denay, Chemisches- und Veterinär-Untersuchungsamt Rhein-Ruhr-Wupper 

<gregoire.denay@cvua-rrw.de>



