"""
Taxonomy object definition
"""


from __future__ import annotations
from typing import List, Union, Iterator
from collections import UserDict, Counter
from .Node import Node
from .Lineage import Lineage


class Taxonomy(UserDict):
    """
    Store Taxonomy nodes
    
    A Taxonomy is instanciated as a dictionnary and 
    each Node can be accessed by its taxid.
    The proper way to populate a Taxonomy is to use the
    `Taxonomy.addNode` method or use a factory function such as
    `load_taxdump`.
    
    See Also
    --------
    Taxidtools.Taxonomy.load_taxdump: load a Taxonomy object from taxdump files
    
    Examples
    --------
    >>> root = Node(1, "root", "root")
    >>> branch1 = Node(11, "node11", "middle", root)
    >>> branch2 = Node(12, "node12", "middel", root)
    >>> leaf1 = Node(111, "node111", "leaf", branch1)
    >>> leaf2 = Node(112, "node112", "leaf", branch1)
    >>> leaf3 = Node(121, "node121", "leaf", branch2)
    >>> leaf4 = Node(13, "node13", "leaf", root)
    >>> tax = Taxonomy()
    >>> for node in [root, branch1, branch2, leaf1, leaf2, leaf3, leaf4]:
    ...     tax._addNode(node)
    ...
    >>> tax
    {'1': Node object:
            Taxid: 1
            Name: root
            Rank: root
            Parent: None, '11': Node object:
            Taxid: 11
            Name: node11
            Rank: middle
            Parent: 1, '12': Node object:
            Taxid: 12
            Name: node12
            Rank: middel
            Parent: 1, '111': Node object:
            Taxid: 111
            Name: node111
            Rank: leaf
            Parent: 11, '112': Node object:
            Taxid: 112
            Name: node112
            Rank: leaf
            Parent: 11, '121': Node object:
            Taxid: 121
            Name: node121
            Rank: leaf
            Parent: 12, '13': Node object:
            Taxid: 13
            Name: node13
            Rank: leaf
            Parent: 1}
    
    You can also pass a dict of Nodes:
    
    >>> tax = Taxonomy({"1" : root,
    ...     11: branch1,
    ...     12: branch2,
    ...     111: leaf1,
    ...     112: leaf2,
    ...     121: leaf3,
    ...     13: leaf4})
    >>> tax
    {'1': Node object:
            Taxid: 1
            Name: root
            Rank: root
            Parent: None, 11: Node object:
            Taxid: 11
            Name: node11
            Rank: middle
            Parent: 1, 12: Node object:
            Taxid: 12
            Name: node12
            Rank: middel
            Parent: 1, 111: Node object:
            Taxid: 111
            Name: node111
            Rank: leaf
            Parent: 11, 112: Node object:
            Taxid: 112
            Name: node112
            Rank: leaf
            Parent: 11, 121: Node object:
            Taxid: 121
            Name: node121
            Rank: leaf
            Parent: 12, 13: Node object:
            Taxid: 13
            Name: node13
            Rank: leaf
            Parent: 1}
    """
    
    def addNode(self, node: Node) -> None:
        """
        Add a Node to an existing Taxonomy object.
        
        The Node taxid will be used a key to access element.
        
        Parameters
        ----------
        node:
            A Node to add to the Taxonomy
        
        Examples
        --------
        >>> tax = Taxonomy()
        >>> tax.addNode(Node(1))
        >>> tax
        {'1': Node object:
                Taxid: 1
                Name: None
                Rank: None
                Parent: None}
        """
        self[node.taxid] = node
    
    def getName(self, taxid: Union[str,int]) -> str:
        """
        Get taxid name
        
        Parameters
        ----------
        taxid: 
            Taxonomic identification number
        
        Examples
        --------
        >>> node = Node(1, "node", "rank")
        >>> tax = Taxonomy({'1':node})
        >>> tax.getName(1)
        'node'
        """
        return self[str(taxid)].name
    
    def getRank(self, taxid: Union[str,int]) -> str:
        """
        Get taxid rank
        
        Parameters
        ----------
        taxid: 
            Taxonomic identification number
        
        Examples
        --------
        >>> node = Node(1, "node", "rank")
        >>> tax = Taxonomy({'1':node})
        >>> tax.getRank(1)
        'rank'
        """
        return self[str(taxid)].rank
    
    def getParent(self, taxid: Union[str,int]) -> Node:
        """
        Retrieve parent Node
        
        Parameters
        ----------
        taxid: 
            Taxonomic identification number
        
        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> tax = Taxonomy({'1': root, '2': node})
        >>> tax.getParent(2)
        Node object:
                Taxid: 1
                Name: root
                Rank: root
                Parent: None
        """
        return self[str(taxid)].parent
    
    def getChildren(self, taxid: Union[str, int]) -> list[Node]:
        """
        Retrieve the children Nodes
        
        Parameters
        ----------
        taxid: 
            Taxonomic identification number
        
        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> tax = Taxonomy({'1': root, '2': node})
        >>> tax.getChildren(1)
        [Node object:
                Taxid: 2
                Name: node
                Rank: rank
                Parent: 1]
        """
        return self[str(taxid)].children
    
    def getAncestry(self, taxid: Union[str,int]) -> Lineage:
        """
        Retrieve the ancestry of the given taxid
        
        Parameters
        ----------
        taxid: 
            Taxonomic identification number
        
        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> tax = Taxonomy({'1': root, '2': node})
        >>> tax.getAncestry(2)
        Lineage(['2', '1'])
        """
        return Lineage(self[str(taxid)])
    
    def isAncestorOf(self, taxid: Union[str,int], child: Union[str,int]) -> bool:
        """
        Test if taxid is an ancestor of child
        
        Parameters
        ----------
        taxid: 
            Taxonomic identification number
        child: 
            Taxonomic identification number
        
        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> tax = Taxonomy({'1': root, '2': node})
        >>> tax.isAncestorOf(1, 2)
        True
        >>> tax.isAncestorOf(2, 1)
        False
        """
        if str(taxid) == str(child):
            return False
        else:
            ancestors = Lineage(self[str(child)])
            return str(taxid) in [node.taxid for node in ancestors]
    
    def isDescendantOf(self, taxid: Union[str,int], parent: Union[str,int]) -> bool:
        """
        Test if taxid is an descendant of parent
        
        Parameters
        ----------
        taxid: 
            Taxonomic identification number
        parent: 
            Taxonomic identification number
        
        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> tax = Taxonomy({'1': root, '2': node})
        >>> tax.isDescendantOf(1, 2)
        False
        >>> tax.isDescendantOf(2, 1)
        True
        """
        if str(taxid) == str(parent):
            return False
        else:
            ancestors = Lineage(self[str(taxid)])
            return str(parent) in [node.taxid for node in ancestors]
    
    def consensus(self, taxid_list: list[Union[str, int]], min_consensus: float) -> str:
        """
        Find a taxonomic consensus for the given taxid with a minimal agreement level.
        
        Parameters
        ----------
        taxid_list: 
            list of taxonomic identification numbers
        min_consensus: 
            minimal consensus level, between 0.5 and 1.
            Note that a minimal consensus of 1 will return the same result as `lastCommonNode()`
        """
        # Consensus under 50% is ambiguous
        if min_consensus <= 0.5 or min_consensus > 1:
            raise ValueError("Minimal consensus should be above 0.5 and under 1")
        
        # Get lineages in REVERSED order 
        lineages = [Lineage(self[str(txd)], ascending = False) for txd in taxid_list] 
        total = len(taxid_list)
        max_iter = min([len(lin) for lin in lineages])
        
        i=0
        
        while i < max_iter: 
            count = Counter([lin[i].taxid for lin in lineages])
            mostCommon = count.most_common(1)
            
            if mostCommon[0][1]/total >= min_consensus:
                # save current succesful consensus, and check the next one
                last = str(mostCommon[0][0])
                i+=1
            
            else:
                break
        
        return last
    
    def lca(self, taxid_list: list[Union[str, int]]) -> str:
        """
        Get lowest common node of a bunch of taxids
        
        Parameters
        ----------
        taxid_list: 
            list of taxonomic identification numbers
        """
        return self.consensus(taxid_list, 1)
    
    def distance(self, taxid1: Union[str,int], taxid2: Union[str,int]) -> int:
        """
        Measures the distance between two nodes.
        
        Parameters
        ----------
        taxid1: 
            Taxonomic identification number
        
        taxid2: 
            Taxonomic identification number
        """
        lca = self.lca([taxid1, taxid2])
        
        d1 = len(Lineage(self[taxid1])) - 1
        d2 = len(Lineage(self[taxid2])) - 1
        dlca = len(Lineage(self[lca])) - 1
        
        return d1 + d2 - 2 * dlca
    
    def listDescendant(self, taxid: Union[str, int]) -> list[Node]:
        """
        List all descendant of node
        
        Parameters
        ----------
        taxid: 
            Taxonomic identification number
        """
        current = self[str(taxid)].children
        next = flatten([child.children for child in current])
        
        all = current
        
        while next:
            all.extend(next)
            current = next
            next = flatten([child.children for child in current])
        
        return all
    
    
    def subtree(self, new_root: Union[str, int]) -> Taxonomy:
        """
        Returns a sutree with the given taxid as new root.
        
        Parameters
        ----------
        new_root: 
            taxid of the new root
        """
        new_root_node = self[str(new_root)]
        nodes = self.listDescendant(new_root)
        
        new = Taxonomy()
        new.addNode(new_root_node)
        
        for node in nodes:
            new.addNode(node)
        
        return new


def load_taxdump(nodes: str, rankedlineage: str) -> Taxonomy:
    """
    Parse NCBI taxdump files
    
    Parameters
    ----------
    nodes: 
        Path to the nodes.dmp file
    rankedlineage: 
        Path to the rankedlineage.dmp file
    """
    txd = Taxonomy()
    parent_dict = {}
    
    # Creating nodes
    for line in _parse_dump(nodes):
        txd.addNode(Node(taxid = line[0], rank = str(line[2])))
        parent_dict[str(line[0])] = line[1] # storing parent id
    
    # Add names form rankedlineage
    for line in _parse_dump(rankedlineage):
        txd[line[0]].name = line[1]
    
    # Update parent info
    for k, v in parent_dict.items():
        txd[k].parent = txd[v]
    
    return txd

def _parse_dump(filepath: str) -> Iterator:
    """
    Dump file line iterator, returns a yields of fields
    """
    with open(filepath, 'r') as dmp:
        for line in dmp:
            yield [item.strip() for item in line.split("|")]

flatten = lambda t: [item for sublist in t for item in sublist]
