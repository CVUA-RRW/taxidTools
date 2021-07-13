# Quickstart guide

No time to read everything, here is how to start
using the package:

Make sure that:
* taxidTools is [installed](install.md)
* You have a local copy of the [NCBI taxdump files](https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/)

While you can use the package with other taxonomy definitions (or none!),
using the Taxdump files is the easiest solution.

## Loading taxonomy information

Start by importing taxidTools:

```python
>>> import taxidTools
```

Then load the taxdump files that you saved and unpacked locally:

```python
>>> tax = taxidTools.Taxonomy.from_taxdump(
        "path/to/nodes.dmp", 
        "path/to/rankedlineage.dmp")
```

Parsing the whole files can take a moment! 
Speeding up this process will be discussed in the [advanced usage](advances.md) section.

The nodes.dmp and rankedlineage.dmp are the only files you need
from the taxdump archive. 

## Accessing node infos

A Taxonomy object contains a bunch of nodes that represent
individual branchings or organisms within the clasification.

Each node has three basic properties:
* A unique identifier (taxid)
* A name, scientific or common. Beware that these names are not 
nescessarily unique and may be shared by several nodes.
* A rank, representing where this node is place in the taxonomy.
Some ranks are unique (e.g. species or genus) but some other appear
at different heights in the Taxonomy (e.g. clade or the well named norank).

Additionally each node has a single parent, the node directly above it in
the Taxonomy and can have any number of children. The only parent-less node
is refered to as root node and represent the top of the taxonomy.

All these properties can be easily accessed, using the taxid number:

```python
>>> tax.getName('9606')
'Homo sapiens'
>>> tax.getRank('9606')
'species'
>>> tax.getParent('9606')
Node(9605)
>>> tax.getChildren('9606')
[Node(63221), Node(744458)]
```

You probably notices that some methodes return a Node. 
These are the basic objects containing all of the node information. 
Actually the Taxonomy object is just a dictionnary of Nodes.
You can access a Node object directly by passing its taxid as a key
to a Taxonomy object and retrieve the Node properties:

```python
>>> hs = tax['9606']
>>> hs.name
'Homo sapiens'
>>> hs.rank
'species'
>>> hs.parent
Node(9605)
>>> hs.parent.name
'Homo'
>>> [node.name for node in hs.children]
['Homo sapiens neanderthalensis', "Homo sapiens subsp. 'Denisova'"]
```

## Ancestries



