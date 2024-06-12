# Release History

## dev

* Update docstrings

## 2.5.1

**Improvements**

* taxidTools.InvalidNodeError now ihnerits from KeyError as well, this might be more intuitive for some users

## 2.5.0

**New features**

* It is now possible to provide merged nodes, either form the taxdump file `merged.dmp` or directly via instances of the class `MergedNode`
* Attempting to retrieve a MergedNode from a Taxonomy instance will return the node it was merged with.

**Bug Fix**

* Instanciating a Lineagefrom a DummyNode doesn't raise an Error anymore

## 2.4.0

**New features**

* Added a `Taxonomy.copy()` method as a shorthand for `copy.deepcopy(Taxonomy)`
* Added an `inplace` argument to `Taxonomy` methods `filterRanks()` and `prune()`, allowing chose whether to return a modified deepcopy of the instance od modifiy it in place

**Improvements**

* Unit tests now use temporary directories to test IO methods
* The `Taxonomy.filter()` method will now return a `ValueError` when attempting to use `root` rank in the filtering instead of creating new root Nodes

**Pending deprecation**

* `Taxonomy.from_json` will be removed in 3.0.0, it is replaced by `read_json`, a module level constructor.
* `load` will be removed in 3.0.0, it is replaced by `read_json`, a module level constructor.
* `Taxonomy.from_taxdump` will be removed in 3.0.0, it is replaced by `read_taxdump`, a module level constructor.
* `load_ncbi` will be removed in 3.0.0, it is replaced by `read_ncbi`, a better-named module level constructor.

**Bug Fix**

* `Taxonomy.listDescendant` now does filter output based on the ranks parameter
* Repaired `Node.node_info` output to actually use newlines instead of printing '\n'

## 2.3.1 (2024-06-04)

**Distribution**

* It is now possible to install taxidTools from DockerHub:

```
docker pull gregdenay/taxidtools
```

* `conda-forge` release should now auomatically find the last release from Github/Pypi

## 2.3.0 (2024-05-13)

**New features**

* Attempting to access an invalid Node with the Taxonomy __getitem__ method (`Taxonomy["node_id"]`) now returns a specifc `InvalidNodeError`
* Added the `load_ncbi` function as a shorthand for the constructor `Taxonomy.from_taxdump`.

## 2.2.3 (2021-10-08)

**Bug Fix**

* Fixed an error in the listDescendant method that affected the prune and filterRanks methods.

**Performance**

* Node.children attribute is now a set, considerably speeding up file loading.

## 2.2.2 (2021-09-21)

**Bug Fix**

* Fixed some bugged references to Node class

## 2.2.0(2021-09-21)

**Bug Fix**

* Fixed broken implementation of `Taxonomy.filterRanks`

**Implementation changes**

* `Node` and `Dummy Node` classes now ihnerit from the new _BaseNode classe. No impact on methods and properties.

## 2.1.2 (2021-08-18)

**Bug Fix**

* Fix a bug resulting in the deletion of the children attribute of Nodes after writing to a JSON file (#2)
* Fix an issue with the creation of DummyNdoes from JSON files (#3)

## 2.1.1 (2021-07-15)

**Bug fix**

* Fixed unlinking of removed branches in `Taxonomy.prune`

**Other**

* Linting code, still ignoring W293 and W291 =)

## 2.1.0 (2021-07-14)

**Bug fix**

* `Taxonomy.filterRanks` now correctly handles rerooted trees
* Fixed and bug to `Taxonomy.consensus` where search would only be in range of the shortest lineage

**Changes**

* Implementation of `Taxonomy.reroot` was changed to conserve the ancestry of the input taxid.
* `Taxonomy.reroot` was renamed to `Taxonomy.prune`

**Additions**

* Added taxid search by name `Taxonomy.getTaxid`

## 2.0.0 (2021-07-13)

* Released version 2. Implementation reworked from scraps. 
* NOT backwards compatible
