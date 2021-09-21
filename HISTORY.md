# Release History

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