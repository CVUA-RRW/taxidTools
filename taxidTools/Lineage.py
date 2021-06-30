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
        base_node: 
            The base node, from which the ancestry should be retrieved
        ascending: 
            Should the Lineage by sorted by ascending ranks?
        """
        assert(isinstance(base_node, Node))
        
        self.data = [base_node]
        
        while self[-1].parent:
            self.append(self[-1].parent)
        
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
        """
        raise NotImplementedError
    
    def forceRanks(self, ranks: list[str]) -> Lineage:
        """
        Force ranks and order on a Lineage
        
        This force the given rank structure on the Lineage.
        As a result, the ranks will be reordered to follow the input.
        Missing ranks in the Lineage will be filled with None values.
        
        Handle mutliple rank values???
        """
        raise NotImplementedError
    
    def __repr__(self):
        return f"Lineage({[node.taxid for node in self]})"
    
def formatLineages(lineages: list[Lineage]) -> list[Lineage]:
    raise NotImplementedError