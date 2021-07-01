"""
Lineage object definition
"""


from __future__ import annotations
from typing import List
from collections import UserList
from .Node import Node


class Lineage(UserList):
    """
    Taxomic Lineage
    
    Defines a linear and ordered succession of Nodes.
    A Lineage is created by providing a single Node that 
    will be used as a base to retrieve higher Nodes.
    Ranks are ascending by default.
    
    Parameters
    ----------
    base_node: 
        The base node, from which the ancestry should be retrieved
    ascending: 
        Should the Lineage by sorted by ascending ranks?
    
    Notes
    -----
    A Lineage does not have to be continuous. Nodes can have parents that
    are not included in the Lineage, as long as Nodes in a Lineage form a 
    linear path.
    
    Examples
    --------
    >>> root = Node(1, "root", "root")
    >>> child1 = Node(2, "child1", "child_rank", root)
    >>> child2 = Node(3, "child2", "sub_child_rank", child1)
    >>> Lineage(child2)
    Lineage(['3', '2', '1'])
    
    Lineage elements are the Node objects themselves
    
    >>> Lineage(child2)[-1]
    Node object:
            Taxid: 1
            Name: root
            Rank: root
            Parent: None
    
    A Lineage can also be descending
    >>> Lineage(child2, ascending = False)
    Lineage(['1', '2', '3'])
    """
    
    def __init__(self, base_node: Node, ascending: bool = True) -> None:
         if not isinstance(base_node, Node):
            raise ValueError("Lineage should be instanciated with a Node or list of Nodes")
        
        self._baseNode = base_node
        
        vec = [base_node]
        
        while vec[-1].parent:
            vec.append(vec[-1].parent)
        
        self.data = vec
        
        if not ascending:
            self.reverse()
    
    def filter(self, ranks: list[str], ascending: bool = True) -> Lineage:
        """
        Filter a lineage to keep specific ranks
        
        Lineage order will be conserved and missing ranks will be ignored.
        Be careful that the returned list can be shorter that the input ranks!
        If you want the output length to be consistent with the input length, 
        use `forceRanks`.
        
        Parameters
        ----------
        ranks:
            List of ranks to keep. Missing ranks in the Lineage will be skipped.
        ascending: 
            Should the Lineage by sorted by ascending ranks?
        
        Notes
        -----
        The Nodes are not modified by this method! That means that Node.parent will
        still point to the original parent Node, even if it was masked in the Lineage.
        
        See Also
        --------
        taxidTools.Lineage.forceRanks
        
        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> child1 = Node(2, "child1", "child_rank", root)
        >>> child2 = Node(3, "child2", "sub_child_rank", child1)
        >>> lin = Lineage(child2)
        >>> lin.filter(["sub_child_rank", "child_rank"])
        Lineage(['3', '2'])
        
        Node order is conserved
        
        >>> lin.filter(["root", "sub_child_rank"])
        Lineage(['3', '1'])
        
        Missing ranks are ignored
        
        >>> lin.filter(["root", "norank", "name_rank", "sub_child_rank"])
        Lineage(['3', '1'])
        """
        new = Lineage(self._baseNode)
        new.data = [node for node in self.data if node.rank in ranks]
        return new
    
    def forceRanks(self, ranks: list[str]) -> Lineage:
        """
        Force ranks and order on a Lineage
        
        This force the given rank structure on the Lineage.
        As a result, the ranks will be reordered to follow the input.
        Missing ranks in the Lineage will be filled with None values.
        
        Not implemented
        """
        raise NotImplementedError
    
    def __repr__(self):
        return f"Lineage({[node.taxid for node in self]})"
    
def formatLineages(lineages: list[Lineage]) -> list[Lineage]:
    """Not Implemented"""
    raise NotImplementedError