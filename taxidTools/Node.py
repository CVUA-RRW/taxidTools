"""
Node objects definition.
Should be used internally only.
"""


from __future__ import annotations
from typing import Union, Optional


class Node(object):
    """
    Taxonomic Node
    
    Store information relative to a specific taxonomic node.
    """
    def __init__(self, 
                 taxid: Union[str,int], 
                 name: Optional[str] = None, 
                 rank: Optional[str] = None, 
                 parent: Optional[str] = None) -> None:
        """
        Create a Node object
        
        Parameters
        ---------
        taxid: 
            Taxonomic identification number
        name: 
            Node name
        rank: 
            Node rank
        parent: 
            The parent Node object
        """
        self._children = []
        self._name = name
        self._rank = rank
        self._parent = parent
        self._taxid = str(taxid)
        
        self._updateParent()
    
    # Property methods
    @property
    def taxid(self) -> str:
        """Taxonomic identification number"""
        return self._taxid
    
    @property
    def name(self) -> str:
        """Name of the taxonomic node"""
        return self._name
    
    @property
    def rank(self) -> str:
        """Rank of the taxonomic node"""
        return self._rank
    
    @property
    def parent(self) -> str:
        """Parent node"""
        return self._parent
    
    @property
    def children(self) -> list:
        """Children nodes"""
        return self._children
    
    # Setter methods
    @taxid.setter
    def taxid(self, taxid: Union[str,int]) -> None:
        self._taxid = str(taxid)
    
    @name.setter
    def name(self, name: str) -> None:
        self._name = name
    
    @rank.setter
    def rank(self, rank: str) -> None:
        self._rank = rank
    
    @parent.setter
    def parent(self, parent: Node) -> None:
        "Set parent node and update children attribute of parent node"
        if parent and parent.taxid != self.taxid: # root node as circular reference to self..
            assert isinstance(parent, Node)
            self._parent = parent
            self._updateParent()
        else:
            self._parent = None
    
    def _updateParent(self):
        if self.parent:
            self.parent.children.append(self)
    
    def __str__(self) -> str:
        if self.parent:
            return f"Node object:\n\tTaxid: {self.taxid}\n\tName: {self.name}\n\tRank: {self.rank}\n\tParent: {self.parent.taxid}"
        else:
            return f"Node object:\n\tTaxid: {self.taxid}\n\tName: {self.name}\n\tRank: {self.rank}\n\tParent: {self.parent}"
    
