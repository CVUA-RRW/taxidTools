# Comparing taxonomic assignement results to expectations

Let's say we assigned some sequences (let's say a OTUs) to taxonomic nodes using 
a classifier of any kind. In practice this could be BLAST or SINTAX
or anything of the like. We now want to verify whether the classifier results
are in agreement with the expected composition of the sample to calculate to performance 
of a method for example.

First things first, let`s load the taxdump file in a Taxonomy object:
``` py
import taxidTools
tax = taxidTools.read_taxdump("nodes.dmp", "rankedlineage.dmp", "merged.dmp")
```

## Getting a taxid for each sequence

### From SINTAX

If we used a bayesian classifier like SINTAX, we have one assignement per sequence,
usually with  a score of some sort, for example:

```
Bos genus   0.8
Gallus gallus   species 0.9
```

In order to work with these nodes later we want to create a list of Nodes from this output:

``` py
# This allows you to run the code in your interpreter
# in practice you should parse the sintax output into a list of names
names = ["Bos", "Gallus gallus"]

taxids = [tax.getTaxid(n) for n in names]
nodes = [tax[t] for t in taxids]
```

### From BLAST

If we used an alignement software like BLAST, we most likely have a list of hits for each 
one of our sequences. BLAST can typically output taxids directly, otherwise get taxids from the 
names like above. Let`s say we parsed our BLAST file in a list of list of taxids. Each element of
the outer list is a list of hits for a single sequence:

``` py
res = [
    [9913, 9913, 72004],
    [9031, 9031]
]
```

Ideally we would like to have a single assignement for each sequence. We can do this by assigning the last common ancestor 
of all the hits for this sequence, or use a less stringent approach, like a majority agreement:

``` py
# Here we could also choose to use tax.lca() instead
nodes = [tax.consensus(ids, 0.51) for ids in res]
```

We now have a single Node object for each sequence, neatly organized in a list!

## Comparing to expected composition

In order to verify that our results are correct, we want to compare 
this list to a list of expected taxids, for example Bos taurus (cattle) and 
Gallus gallus (chicken), bot at the species level:

``` py
expected = [9913, 9031] 
```

Now we don't nescessarily have a consensus at the species rank for each sequence, and that's often
perfectly fine. One approach to compare the two lists is to determine to which expected 
component each sequence could correspond, and then to get the rank at which they meet, effectively 
determining the degree of aggreement.

The easiest way to do this is to calculate the distance between the sequence assignement and each of the 
expected components. The smallest distance indicates the correponding expected component.
One has to keep in mind that different branches of the taxonomy can have a wildly different number of nodes,
so it can greatly simplify things first normalize to taxonomy for such an approach:

``` py
norm = tax.filterRanks(inplace=False)

distances = []
for n in nodes:
    distances.append(
        [norm.distance(n.taxid, e) for e in expected]
    )
# Getting the index of the minimum distance
index_corr = [d.index(min(d)) for d in distances]
```

Now that we have a list which links each consensus to the index of its closest match in the list of 
expected species, it is straightforward to determine the agreement rank between result and expectation:

``` py
ranks = []
for i in range(len(nodes)):
    ranks.append(
        tax.lca(
            [nodes[i].taxid,
            expected[index_corr[i]]]
        ).rank
    )
```

The last step for us is to assign each result to a binary value (positiv/negativ) that we can
later use to build a confusion matrix and calculate performance values like recall or precision.
Let's say we want to determine these values at the genus resolution. The advantage of normalizing 
the taxonomy earlier is that we don't need to care about the precise order of ranks in each branch,
we can simply check wether the agreement rank in either of 'genus' or 'species':

``` py
[True if r in ['genus', 'species'] else False for r in ranks]
```

### Unnormalized taxonomy

Of course it is possible to follow a similar approach without normalizing the taxonomy. It is however
slightly more complicated. For example checking wether *Bos taurus* (9913) consensus (here genus) is
under the genus level involves determining the correpsonding expected node with the unnormalized taxonomy.
The trick here is to calculate the distance to the last common ancestor so that different branches length 
don't bias the analysis:

``` py
distances = [tax.distance(9913, tax.lca(9913, e).taxid) for e in expected]
index_corr = distances.index(min(distances))
agreement = expected[index_corr]
```

Now instead of simply checking the rank of the agreement, we will rather determine the ancestor
node of the expected species at the required resolution:

``` py
lin = tax.getAncestry(agreement)
lin.filter(['genus'])
target = lin[0]
```

Now the last common ancestor of our result and the corresponding expected species is either
an ancestor of `target`, in which case the result did not reach the expected resolution,
or its descendant or the target itself, in which case the required resolution is attained:

``` py
not tax.isAncestorOf(target.taxid, tax.lca([agreement, 9913]))
```

Note that in the last expression above we added `not` in order to have the results in the same form 
as previously.
