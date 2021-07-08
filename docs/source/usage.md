# Usage

The easiest way to get started with tha package is todownload the 
taxdump files from the NCBI FTP server and start python.

## Loading taxdump files

Once you downlaoded the up-to-date taxdump files from the NCBI FTP server,
you can load the full taxonomy as simply as:

```python
import taxidTools as txd

nodes_dmp = "path/to/nodes.dmp"
rankedlineage = "path/to/rankedlineage.dmp"

tax = txd.load_taxdump(nodes_dmp, rankedlineage_dmp)
```

## Retrieving node informations

access node str or int

getParent

getRank

getName

## Working with lineages

### Simple relationship tests

isDescendantOf

isAncestorOf


### Full ancestries

Lineage() and getAncestry

Lineage behavior

## Taxonomy subsets

getChildren

subtree

## Operations on multiple nodes

distance

lca

consensus

## Creating a taxonomy without Taxdump files

### Creating Nodes

Node creation

### Updating parents

### Constructing taxonomy