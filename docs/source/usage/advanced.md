# Advanced usage

If you mastered the [basic operations](quickstart.md) on Taxonomies, here are some
more advances uses.

## A word of caution on mutable types

All three object types in this package are mutable types.
That means that methods will modify the object rather than
return a new instance of the class.

However a big difference exists between Lineage and Taxonomy objects:
* Lineages are used as simple references to Nodes, therefore methods 
modifying a Lineage, such as `Lineage.filter` will never mutate the underlying 
Node objects.
* Taxonomy are a description of the nodes relationships. Therefore methods 
modifying the Taxonomy such as `Taxonomy.reroot`, `Taxonomy.filterRanks` do 
modify at least some of the underlying nodes. This is nescessary to relink 
Nodes after unwanted ranks have been discarded in the case of `filterRanks`
for example.

Should you want to keep a copy of the original Taxonomy (and the Nodes), you should 
do a deep copy:

```python
>>> import copy
>>> tax_copy = copy.deepcopy(tax)
```

Alternatively you can save the Taxonomy in JSON format for a later use (see next sections).

## Consensus determination 

Determining a consensus node from a bunch of taxid can be done as easily as:

```python
>>> tax.lca(['9606', '10090']).name  # Mice and men
'Euarchontoglires'
```

However, sometimes you may want to determine a consensus node dependent on the 
frequencies of a bunch of taxids. You can set a minimal frequency threshold (between 0.5 and 1).
As soon a a single node meets this threshold, it will be returned as a consensus. If this threshold is 
not met with the given input, then the parents of the input will be considered, and so on.

```python
>>> tax_list = ['9606']*6 + ['314146']*3 + ['4641']*8  # Mice and men and bananas
>>> tax.consensus(tax_list, 0.51).name
'Euarchontoglires'
>>> tax.consensus(tax_list, 1).name
'Eukaryota'
```

## Distances

Distance between two nodes is straightforward to calculate:

```python
>>> tax.distance('9606', '10090')
18
```

Note that if you want to compare distances it could be a good idea to normalize the taxonomy 
first in order to impose homogeneous ranks across lineages (see next section).

## Rerooting, filtering and normalizing taxonomies

If you don't care about part of the Taxonomy 
you can extract a subtree and/or filter the Taxonomy to keep only specific 
ranks.

```python
>>> tax.prune('40674') # mammals class
>>> tax.filterRanks(['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom'])
>>> tax.getAncestry('9606')
Lineage([Node(9606), Node(9605), Node(9604), Node(9443), Node(40674), Node(7711), Node(33208), Node(1)])
```

Note that the `Taxonomy.prune` method does not excatly cut the tree at the given node 
but rather supresses all other branches and leaves the ancestry of this node.
This is by design and allows to keep ancestries up to the root node.

Normalizing a Taxonomy using `Taxonomy.filterRanks` can be especially useful
to calculate internode distances or comparing Lineages. When requesting a rank 
which nodes are missing, these nodes will be replaced by a DummyNode.
These special kind of nodes act as place-holders for non-existing nodes.

```python
>>> tax.filterRanks(['species', 'subgenus', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom'])
>>> tax.getAncestry('9606')
Lineage([Node(9606), DummyNode(AAeFFWcs), Node(9605), Node(9604), Node(9443), Node(40674), 
Node(7711), Node(33208), Node(1)])
```

Note that the above methods **mutate** the nodes:

```python
>>> tax.getParent('9606')
DummyNode(AAeFFWcs)
>>> tax.getRank('AAeFFWcs')
'subgenus'
```

The formatted Linaean taxonomy ranks can be retrieved from the utility function `linne()`
for use in diverse methods:

```python
>>> taxidTools.linne()
['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom']
>>> tax.filterRanks(taxidTools.linne())
>>> tax.getAncestry('9606')
Lineage([Node(9606), Node(9605), Node(9604), Node(9443), Node(40674), Node(7711), Node(33208), Node(1)])
```

## Reading and writing taxonomies

As you probably already noticed, parsing the Taxonomy definition can 
take a couple of minutes. If you plan on regularly using a subset of the Taxonomy, 
it can be beneficial to save a filtered version to a JSON file and to reload it later.

```python
>>> tax.write("my_filtered_taxonomy.json")
>>> new_tax = taxidTools.load("my_filtered_taxonomy.json")
```

## Working with non-NCBI taxonomies

Creating a Taxonomy object can also be done without the Taxdump files.
You can either manually create Nodes and build a Taxonomy from them:

```python
>>> root = taxidTools.Node(taxid = 1, name = 'root', rank = 'root')
>>> node1 = taxidTools.Node(taxid = 2, name = 'node1', rank = 'rank1', parent = root)
>>> tax = taxidTools.Taxonomy.from_list([root, node1])
>>> node2 = taxidTools.Node(taxid = 3, name = 'node2', rank = 'rank1', parent = root)
>>> tax.addNode(node2)
```

If you have a Taxonomy definition file, the best thing to do is
to create a parsing function to:
* Create Node objects
* Link parents and children
* Create a Taxonomy

Here is a boilerplate code for such a function, assuming that each node 
is defined on a single line:

```python
def custom_parser(file):
    # Create two empty dict that will store the node
    # information and parent information respectively
    txd = {} 
    parent_dict = {}
    
    # Creating nodes
    with open(file, 'r') as fi:
        # Parse file information, one node record at a time
        for line in fi.readlines():
            # Get the taxid field and so on for the other fields
            taxid = line.split(sep)[index]
            name = ...
            rank = ...
            parent = ...
            
            # Create nodes
            txd[taxid] = Node(taxid, name = name, rank = rank)
            # need to delay parent linking as the parent node might not exist yet
            parent_dict[taxid] = parent
        
    # Update parent info now that all Nodes are created
    for k, v in parent_dict.items():
        txd[k].parent = txd[v]
    
    return taxidTools.Taxonomy(txd)
```

Also check the implementations of `Taxonomy.from_taxdump` and `Taxonomy.from_json` for 
specific examples.
