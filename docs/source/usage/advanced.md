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

Alternatively you can save the Taxonomy in JSON format for a later use (see next section).

## Create, save and load subtrees

If you don't care about part of the Taxonomy 
you can extract a subtree and/or filter the Taxonomy to keep only specific 
ranks.

```python
>>> tax.reroot('40674')
>>> tax.filterRanks(['species', 'genus', 'family', 'order', 'class', 'phylum', 'kingdom'])
>>> tax.getAncestry('9606')
# Fix method - currently broken
```

Note the presence of a special kind of Node is this Lineage.
The DummyNode objects are place-holders for non-existing nodes. 
Here it replaces the phylum and kingdom ranks, that were removed 
by rerooting the tree at the Chardates (class) node.

Dummy nodes will also be inserted between existing nodes if you request a
rank that does not exist in a Lineage:

```python
# TODO example
```

As you probably already noticed, parsing the Taxonomy definition can 
take a couple of minutes. If you plan on regularly using a subset of the Taxonomy, 
it can be beneficial to save a filtered version to a JSON file and to reload it later.

```python
>>> tax.write("my_filtered_taxonomy.json")
>>> new_tax = taxidTools.load("my_filtered_taxonomy.json")
```

## Consensus determination 

LCA and consensus

## Distances

Rank normalization for distances

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


Here a boilerplate code for such a function, assuming that each node 
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
