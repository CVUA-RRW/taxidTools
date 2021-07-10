"""
Node objects definition.
Should be used internally only.
"""


from __future__ import annotations
from typing import Union, Optional
from .utils import _rand_id


class Node(object):
    """
    Taxonomic Node
    
    Create a Node object contining taxonomic information
    as well as a link to parent and children nodes.
    
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
    
    Notes
    -----
    The `children` property will be dynamically populated when children Nodes
    declare a Node as parent.
    
    Examples
    --------
    >>> root = Node(1, "root", "root")
    >>> child = Node(2, "child", "child_rank", root)
    
    >>> child.taxid
    '2'
    >>> child.rank
    'child_rank'
    >>> child.name
    'child'
    
    >>> child.parent
    Node object:
            Taxid: 1
            Name: root
            Rank: root
            Parent: None
    
    >>> root.children
    [Node object:
            Taxid: 2
            Name: child
            Rank: child_rank
            Parent: 1]
    """
    
    def __init__(self, 
                 taxid: Union[str,int], 
                 name: Optional[str] = None, 
                 rank: Optional[str] = None, 
                 parent: Optional[str] = None) -> None:
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
        """Set parent node and update children attribute of parent node"""
        if parent and parent.taxid != self.taxid: # root node as circular reference to self..
            assert isinstance(parent, Node)
            self._parent = parent
            self._updateParent()
        else:
            self._parent = None
    
    @property
    def node_info(self) -> str:
        """
        Node information
        """
        return f"{self.__repr__()}\ntype: {self.__class__.__name__}\ntaxid: {self.taxid}\nname: {self.name}\nrank: {self.rank}\nparent: {self.parent}\nchildren: {self.children}\n"
    
    def isAncestorOf(self, node: Node) -> bool:
        """
        Test if the object is an ancestor of another Node.
        
        Parameters
        ----------
        node: 
            Putative descendant node
        
        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> node.isAncestorOf(root)
        False
        root.isAncestorOf(node)
        True
        """
        if not node.parent or node.parent.taxid == node.taxid:
            return False
        elif node.parent.taxid == self.taxid:
            return True
        else:
            return self.isAncestorOf(node.parent)
    
    def isDescendantOf(self, node: Node) -> bool:
        """
        Test if the object is an ancestor of another Node.
        
        Parameters
        ----------
        node: 
            Putative ancestor node
        
        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> node.isDescendantOf(root)
        True
        root.isDescendantOf(node)
        False
        """
        if not self.parent or self.parent.taxid == self.taxid:
            return False
        elif self.parent.taxid == node.taxid:
            return True
        else:
            return self.parent.isDescendantOf(node)
        
    def _updateParent(self) -> None:
        """
        Add self to parent's children list
        """
        if self.parent:
            if self not in self.parent.children:
                self.parent.children.append(self)
    
    def _relink(self) -> None:
        """
        Bypass self by relinking children to parents
        """
        if not self.parent:
            raise TypeError("Cannot relink a root Node")
            
        for child in self.children:
            child.parent = self.parent
            # Will auto update the parent node
        self.parent.children.remove(self)
    
    def __repr__(self) -> str:
        return f"Node({self.taxid})"
    
    def _to_dict(self):
        """
        Create a dict of self with information to recreate the object.
        """
        dic = self.__dict__
        if self.parent:
            dic['_parent'] = dic['_parent'].taxid
        dic['type'] = self.__class__.__name__
        del dic['_children']
        return dic

class DummyNode(Node):
    """
    A placeholder for a non-existing Node.
    
    Will be assigned a random hash id in place of a taxid 
    upon creation.
    """
    def __init__(self, *args, **kwargs) -> None:
        hash = _rand_id()
        super().__init__(taxid = hash, *args, **kwargs)
    
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
        """Set parent node and update children attribute of parent node"""
        if parent and parent.taxid != self.taxid: # root node as circular reference to self..
            assert isinstance(parent, Node)
            self._parent = parent
            self._updateParent()
        else:
            self._parent = None
    
    def insertNode(self, parent: Node, child: Node) -> None:
        """
        Insert the dummy node between parent and child
        """   
        child.parent = self
        parent.children.remove(child)
        self.parent = parent
    
    def __repr__(self) -> str:
        return f"DummyNode({self.taxid})"
