"""
Lineage object definition
"""


from __future__ import annotations
from typing import List
from collections import UserList
from .Node import Node


class Lineage(UserList):
    """
    Store Lineage information.
    Ranks are ascending
    """
    
    def __init__(self, base_node: Node, ascending: bool = True) -> None:
        """
        Retrieve the Ancestry of a Node
        
        Parameters
        ----------
        base_node: Node
            The base node, from hich the ancestry should be retrieved
        ascending: bool
            Should the Lineage by sorted by ascending ranks?
        
        Returns
        -------
        Lineage
            A Lineage object
        """
        assert(isinstance(base_node, Node))
        
        self.data = [base_node]
        
        while self[-1].parent:
            self.append(self[-1].parent)
        
        if not ascending:
            self.reverse()
    
    def filter(self, ranks: list[str]) -> Lineage:
        raise NotImplementedError
    
    def __repr__(self):
        return f"Lineage({[node.taxid for node in self]})"
    
def formatLineages(lineages: list[Lineage]) -> list[Lineage]:
    raise NotImplementedError