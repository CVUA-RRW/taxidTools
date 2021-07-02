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
    A Taoxonomy object can be instanciated directly from a dictionnary,
    iteratively with the method `Taxonomy.addNode` method or from a 
    list of taxdump files..
    
    See Also
    --------
    Taxidtools.Taxonomy.from_taxdump: load a Taxonomy object from taxdump files
    Taxidtools.Taxonomy.from_list: load a Taxonomy object from a list of Node
    Taxidtools.Taxonomy.addNode: add a Node to a Taxonomy
    
    Examples
    --------
    >>> root = Node(1, "root", "root")
    >>> branch1 = Node(11, "node11", "middle", root)
    >>> branch2 = Node(12, "node12", "middel", root)
    >>> leaf1 = Node(111, "node111", "leaf", branch1)
    >>> leaf2 = Node(112, "node112", "leaf", branch1)
    >>> leaf3 = Node(121, "node121", "leaf", branch2)
    >>> leaf4 = Node(13, "node13", "leaf", root)
    
    >>> tax = Taxonomy({"1" : root,
    ...     11: branch1,
    ...     12: branch2,
    ...     111: leaf1,
    ...     112: leaf2,
    ...     121: leaf3,
    ...     13: leaf4})
    
    Instanciate from a list:
    
    >>> tax = Taxonomy.from_list([root, branch1, branch2, leaf1, leaf2, leaf3, leaf4])
    
    Or iteratively:
    
    >>> tax = Taxonomy()
    >>> for node in [root, branch1, branch2, leaf1, leaf2, leaf3, leaf4]:
    ...     tax.addNode(node)
    ...
    
    Or from the taxdump files:
    
    >>> tax = Taxonomy.from_taxdump("nodes.dmp', 'rankedlineage.dmp')
    """
    
    @classmethod
    def from_list(cls, node_list: list[Node]) -> Taxonomy:
        """
        Create a Taxonomy object from a list of Nodes
        
        Convert a list of Nodes into a valid Taxonomy object 
        where each Node can be accessed using its taxid as key.
        
        Parameters
        ----------
        node_list:
            List of Node objects
        
        Examples
        --------
        >>> txd = Taxonomy.from_list([Node(1), Node(2)])
        """
        for node in node_list:
            if not isinstance(node, Node):
                raise ValueError("Elements of node_list must be of type Node")
        
        as_dict = {node.taxid : node for node in node_list}
        
        return cls(as_dict)
    
    @classmethod
    def from_taxdump(cls, nodes: str, rankedlineage: str) -> Taxonomy:
        """
        Create a Taxonomy object from the NBI Taxdump files
        
        Load the taxonomic infromation form the nodes.dmp and
        rankedlineage.dmp files available from the NCBI servers.
        
        Parameters
        ----------
        nodes: 
            Path to the nodes.dmp file
        rankedlineage: 
            Path to the rankedlineage.dmp file
        
        Examples
        --------
        >>> tax = Taxonomy.from_taxdump("nodes.dmp', 'rankedlineage.dmp')
        """
        txd = {}
        parent_dict = {}
        
        # Creating nodes
        for line in _parse_dump(nodes):
            txd[line[0]] = Node(taxid = line[0], rank = str(line[2]))
            parent_dict[str(line[0])] = line[1] # storing parent id
        
        # Add names form rankedlineage
        for line in _parse_dump(rankedlineage):
            txd[line[0]].name = line[1]
        
        # Update parent info
        for k, v in parent_dict.items():
            txd[k].parent = txd[v]
        
        return cls(txd)
    
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
        
        See Also
        --------
        Taxonomy.isDescendantOf
        
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
        
        See Also
        --------
        Taxonomy.isAncestorOf
        
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
    
    def consensus(self, taxid_list: list[Union[str, int]], min_consensus: float) -> Node:
        """
        Find a taxonomic consensus for the given taxid with a minimal agreement level.
        
        Parameters
        ----------
        taxid_list: 
            list of taxonomic identification numbers
        min_consensus: 
            minimal consensus level, between 0.5 and 1.
            Note that a minimal consensus of 1 will return the same result as `lastCommonNode()`
        
        Notes
        -----
        If no consensus can be found (for example because the Taxonomy contains multiple trees),
        an `IndexError` will be raised.
        
        See Also
        --------
        Taxonomy.lca
        
        
        Examples
        --------
        >>> node0 = Node(taxid = 0, name = "root", rank = "root", parent = None)
        >>> node1 = Node(taxid = 1, name = "node1", rank = "rank1", parent = node0)
        >>> node2 = Node(taxid = 2, name = "node2", rank = "rank1", parent = node0)
        >>> node11 = Node(taxid = 11, name = "node11", rank = "rank2", parent = node1)
        >>> node12 = Node(taxid = 12, name = "node12", rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node0, node1, node2, node11, node12])
        >>> tax.consensus([11, 12, 2], 0.8)
        Node object:
                Taxid: 0
                Name: root
                Rank: root
                Parent: None
        >>> tax.consensus([11, 12, 2], 0.6)
        Node object:
                Taxid: 1
                Name: node1
                Rank: rank1
                Parent: 0
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
            count = Counter([lin[i] for lin in lineages])
            mostCommon = count.most_common(1)
            
            if mostCommon[0][1]/total >= min_consensus:
                # save current succesful consensus, and check the next one
                last = mostCommon[0][0]
                i+=1
            
            else:
                break
        
        return last
    
    def lca(self, taxid_list: list[Union[str, int]]) -> Node:
        """
        Get lowest common node of a bunch of taxids
        
        Parameters
        ----------
        taxid_list: 
            list of taxonomic identification numbers
        
        See Also
        --------
        Taxonomy.consensus
        
        Examples
        --------
        >>> node0 = Node(taxid = 0, name = "root", rank = "root", parent = None)
        >>> node1 = Node(taxid = 1, name = "node1", rank = "rank1", parent = node0)
        >>> node2 = Node(taxid = 2, name = "node2", rank = "rank1", parent = node0)
        >>> node11 = Node(taxid = 11, name = "node11", rank = "rank2", parent = node1)
        >>> node12 = Node(taxid = 12, name = "node12", rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node0, node1, node2, node11, node12])
        >>> tax.lca([11, 12, 2])
        Node object:
                Taxid: 0
                Name: root
                Rank: root
                Parent: None
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
        
        Examples
        --------
        >>> node0 = Node(taxid = 0, name = "root", rank = "root", parent = None)
        >>> node1 = Node(taxid = 1, name = "node1", rank = "rank1", parent = node0)
        >>> node2 = Node(taxid = 2, name = "node2", rank = "rank1", parent = node0)
        >>> node11 = Node(taxid = 11, name = "node11", rank = "rank2", parent = node1)
        >>> node12 = Node(taxid = 12, name = "node12", rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node0, node1, node2, node11, node12])
        >>> tax.distance(11, 2)
        3
        >>> tax.distance(11, 12)
        2
        """
        lca = self.lca([str(taxid1), str(taxid2)]).taxid
        
        d1 = len(Lineage(self[str(taxid1)])) - 1
        d2 = len(Lineage(self[str(taxid2)])) - 1
        dlca = len(Lineage(self[lca])) - 1
        
        return d1 + d2 - 2 * dlca
    
    def listDescendant(self, taxid: Union[str, int]) -> list[Node]:
        """
        List all descendant of a node
        
        Parameters
        ----------
        taxid: 
            Taxonomic identification number
        
        Examples
        --------
        >>> node0 = Node(taxid = 0, name = "root", rank = "root", parent = None)
        >>> node1 = Node(taxid = 1, name = "node1", rank = "rank1", parent = node0)
        >>> node2 = Node(taxid = 2, name = "node2", rank = "rank1", parent = node0)
        >>> node11 = Node(taxid = 11, name = "node11", rank = "rank2", parent = node1)
        >>> node12 = Node(taxid = 12, name = "node12", rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node0, node1, node2, node11, node12])
        >>> tax.listDescendant(1)
        [Node object:
                Taxid: 11
                Name: node11
                Rank: rank2
                Parent: 1, Node object:
                Taxid: 12
                Name: node12
                Rank: rank2
                Parent: 1]
        >>> tax.listDescendant(2)
        []
        """
        current = self[str(taxid)].children
        next = _flatten([child.children for child in current])
        
        all = current
        
        while next:
            all.extend(next)
            current = next
            next = _flatten([child.children for child in current])
        
        return all
    
    
    def subtree(self, new_root: Union[str, int]) -> Taxonomy:
        """
        Returns a sutree with the given taxid as new root.
        
        Parameters
        ----------
        new_root: 
            taxid of the new root
        
        Examples
        --------
        >>> node0 = Node(taxid = 0, name = "root", rank = "root", parent = None)
        >>> node1 = Node(taxid = 1, name = "node1", rank = "rank1", parent = node0)
        >>> node2 = Node(taxid = 2, name = "node2", rank = "rank1", parent = node0)
        >>> node11 = Node(taxid = 11, name = "node11", rank = "rank2", parent = node1)
        >>> node12 = Node(taxid = 12, name = "node12", rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node0, node1, node2, node11, node12])
        >>> tax.subtree(1)
        {'1': Node object:
                Taxid: 1
                Name: node1
                Rank: rank1
                Parent: 0, '11': Node object:
                Taxid: 11
                Name: node11
                Rank: rank2
                Parent: 1, '12': Node object:
                Taxid: 12
                Name: node12
                Rank: rank2
                Parent: 1}
        """
        new_root_node = self[str(new_root)]
        nodes = self.listDescendant(new_root)
        
        new = Taxonomy()
        new.addNode(new_root_node)
        
        for node in nodes:
            new.addNode(node)
        
        return new


def _parse_dump(filepath: str) -> Iterator:
    """
    Dump file line iterator, returns a yields of fields
    """
    with open(filepath, 'r') as dmp:
        for line in dmp:
            yield [item.strip() for item in line.split("|")]

_flatten = lambda t: [item for sublist in t for item in sublist]
