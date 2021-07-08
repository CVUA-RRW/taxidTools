"""
Lineage object definition
"""


from __future__ import annotations
from typing import List
from collections import UserList
from .Node import Node, DummyNode
from .utils import linne


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
    
    Lineage methods will never modify the Node objects it contains
    
    Examples
    --------
    >>> root = Node(1, "root", "root")
    >>> child1 = Node(2, "child1", "child_rank", root)
    >>> child2 = Node(3, "child2", "sub_child_rank", child1)
    >>> Lineage(child2)
    Lineage([Node(3), Node(2), Node(1)])
    
    Lineage elements are the Node objects themselves
    
    >>> Lineage(child2)[-1]
    Node object:
            Taxid: 1
            Name: root
            Rank: root
            Parent: None
    
    A Lineage can also be descending
    >>> Lineage(child2, ascending = False)
    Lineage([Node(1), Node(2), Node(3)])
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
    
    def filter(self, ranks: list[str] = linne()) -> None:
        """
        Filter a Lineage to a set of specified ranks.
        
        Modifies a Lineage in-place.
        Lineage order will not be conserved and dummy nodes will
        be added as placeholders for missing ranks.
        
        Parameters
        ----------
        ranks:
            List of ranks to filter. It is assumed to be sorted
            in the same order as Lineage.
        no_check:
            Do not check the length of the ouput. This can result in 
            the output being longer than the input list of ranks.
        
        Notes
        -----
        The Nodes are not modified by this method! That means that Node.parent will
        still point to the original parent Node, even if it was masked in the Lineage.
        
        
        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> child1 = Node(2, "child1", "child_rank", root)
        >>> child2 = Node(3, "child2", "sub_child_rank", child1)
        >>> lin = Lineage(child2)
        >>> lin.filter(["sub_child_rank", "norank", "child_rank"])
        >>> lin
        Lineage([Node(3), 'dummy', Node(2)])
        
        Order is not conserved!
        
        >>> lin = Lineage(child2)
        >>> lin.filter(["root", "sub_child_rank"])
        Lineage([Node(1), Node(3)])
        """
        nodedict = {node.rank: node for node in self if node.rank in ranks}    
        
        new = []
        for rank in ranks:
            try:
                new.append(nodedict[rank])
            except KeyError:
                new.append(DummyNode(rank = rank))
        
        self.data = new

    def __repr__(self):
        return f"Lineage({[node for node in self]})"
