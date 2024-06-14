"""
Taxonomy object definition
"""


from __future__ import annotations
from typing import Union, Iterator, Optional, Any
from collections import UserDict, Counter
from copy import copy, deepcopy
import json
from .Node import Node, DummyNode, _BaseNode, MergedNode
from .Lineage import Lineage
from .utils import linne, _deprecation
from .exceptions import InvalidNodeError


class Taxonomy(UserDict):
    """
    Stores Taxonomy nodes and their relationships

    A Taxonomy is instanciated as a dictionnary and
    each Node can be accessed by its taxid.
    A Taoxonomy object can be instanciated directly from a dictionnary,
    iteratively with the method `Taxonomy.addNode` method or from a
    list of taxdump files..

    Attributes
    ----------
    root
    data: dict
        data store

    Raises
    ------
    taxidTools.InvalidNodeError
        If trying to access a Node that doesn't exist with a bracket expression

    Notes
    -----
    Taxonomy objects are mutable and some methods will modify the
    underlying Node objects.
    Do a deep copy or use the Taxonomy.copy() method if you wish to keep the original object.

    A Taxonomy always assumes a unique root node.

    See Also
    --------
    Taxonomy.from_list: load a Taxonomy object from a list of Node
    read_taxdump: load a Taxonomy object from taxdump files
    read_json: load a Taxonomy from a previously exported json file
    Taxonomy.addNode: add a Node to a Taxonomy

    Examples
    --------
    >>> root = Node(1, "root", "root")
    >>> branch1 = Node(11, "node11", "middle", root)
    >>> branch2 = Node(12, "node12", "middel", root)
    >>> leaf1 = Node(111, "node111", "leaf", branch1)
    >>> leaf2 = Node(112, "node112", "leaf", branch1)
    >>> leaf3 = Node(121, "node121", "leaf", branch2)
    >>> leaf4 = Node(13, "node13", "leaf", root)

    From a dictionnary of Nodes:

    >>> tax = Taxonomy({"1" : root,
    ...     11: branch1,
    ...     12: branch2,
    ...     111: leaf1,
    ...     112: leaf2,
    ...     121: leaf3,
    ...     13: leaf4})

    Instanciate from a list:

    >>> tax = Taxonomy.from_list(
        [root, branch1, branch2, leaf1, leaf2, leaf3, leaf4])

    Or iteratively:

    >>> tax = Taxonomy()
    >>> for node in [root, branch1, branch2, leaf1, leaf2, leaf3, leaf4]:
    ...     tax.addNode(node)
    ...

    Or from the taxdump files:

    >>> tax = Taxonomy.read_taxdump("nodes.dmp', 'rankedlineage.dmp', 'merged.dmp')
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # create name dict for backward lookup
        self._namedict = {}
        for k, v in self.items():
            if v.name:
                self._namedict[v.name] = k

    def __getitem__(self, key: str) -> Node:
        """
        Element getter with brackets

        Overloading default behavior to:
        - return a specific error on non-existing key
        - handle MergedNodes to return the new node
        """
        try:
            node = super().__getitem__(key)
        except KeyError:
            raise InvalidNodeError(f"There is no Node with taxid '{key}' in this Taxonomy")
        if isinstance(node, MergedNode):
            # call to getitem in case new_node was merged too
            return self.__getitem__(node.new_node)
        return node

    def __repr__(self):
        return f"{set(self.values())}"

    @classmethod
    def from_list(cls, node_list: list[_BaseNode]) -> Taxonomy:
        """
        Create a Taxonomy object from a list of Nodes

        Convert a list of Nodes into a valid Taxonomy object
        where each Node can be accessed using its taxid as key.

        Parameters
        ----------
        node_list:
            List of Node objects

        Returns
        -------
        Taxonomy

        Examples
        --------
        >>> txd = Taxonomy.from_list([Node(1), Node(2)])
        """
        for node in node_list:
            if not isinstance(node, (_BaseNode, MergedNode)):
                raise ValueError("Elements of node_list must be of type Node")

        as_dict = {node.taxid: node for node in node_list}

        return cls(as_dict)

    def copy(self) -> Taxonomy:
        """
        Create a deepcopy of the current Taxonomy instance.

        Equivalent to running copy.deepcopy()

        Returns
        -------
        Taxonomy
        """
        new = deepcopy(self.data)
        return Taxonomy(new)

    @property
    def root(self) -> Node:
        """
        Returns the root Node, assumes a single root shared by all Nodes
        """
        anynode = next(iter(self.values()))
        return Lineage(anynode)[-1]

    def addNode(self, node: Node) -> None:
        """
        Add a Node to an existing Taxonomy object.

        The Node taxid will be used a key to access element.

        Parameters
        ----------
        node: taxidTools._BaseNode
            A Node to add to the Taxonomy

        Examples
        --------
        >>> tax = Taxonomy()
        >>> tax.addNode(Node(1))
        """
        self[node.taxid] = node
        if node.name:
            self._namedict[node.name] = node.taxid

    def getTaxid(self, name: Union[int, str], value: Optional[Any] = None) -> str:
        """
        Get taxid from name


        Parameters
        ----------
        name: str or int
            Node name
        value:
            A value to return if name does not exist

        Returns
        -------
        str

        Examples
        --------
        >>> node = Node(1, "node", "rank")
        >>> tax = Taxonomy({'1':node})
        >>> tax.getTaxid('node')
        '1'
        """
        try:
            return self._namedict[name]
        except KeyError:
            return value

    def getName(self, taxid: Union[str, int], value: Optional[Any] = None) -> str:
        """
        Get taxid name

        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        value:
            A value to return if name does not exist

        Returns
        -------
        str

        Examples
        --------
        >>> node = Node(1, "node", "rank")
        >>> tax = Taxonomy({'1':node})
        >>> tax.getName(1)
        'node'
        """
        try:
            return self[str(taxid)].name
        except InvalidNodeError:
            return value

    def getRank(self, taxid: Union[str, int], value: Optional[Any] = None) -> str:
        """
        Get taxid rank

        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        value:
            A value to return if name does not exist

        Returns
        -------
        str

        Examples
        --------
        >>> node = Node(1, "node", "rank")
        >>> tax = Taxonomy({'1':node})
        >>> tax.getRank(1)
        'rank'
        """
        try:
            return self[str(taxid)].rank
        except InvalidNodeError:
            return value

    def getParent(self, taxid: Union[str, int], value: Optional[Any] = None) -> _BaseNode:
        """
        Retrieve parent Node

        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        value:
            A value to return if name does not exist

        Returns
        -------
        taxidTools._BaseNode

        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> tax = Taxonomy({'1': root, '2': node})
        >>> tax.getParent(2)
        Node(1)
        """
        try:
            return self[str(taxid)].parent
        except InvalidNodeError:
            return value

    def getChildren(self, taxid: Union[str, int], value: Optional[Any] = None) -> list[Node]:
        """
        Retrieve the children Nodes

        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        value:
            A value to return if name does not exist

        Returns
        -------
        list

        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> tax = Taxonomy({'1': root, '2': node})
        >>> tax.getChildren(1)
        [Node(2)]
        """
        try:
            return self[str(taxid)].children
        except InvalidNodeError:
            return value

    def getAncestry(self, taxid: Union[str, int]) -> Lineage:
        """
        Retrieve the ancestry of the given taxid

        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number

        Returns
        -------
        taxidTools.Lineage

        Examples
        --------
        >>> root = Node(1, "root", "root")
        >>> node = Node(2, "node", "rank", root)
        >>> tax = Taxonomy({'1': root, '2': node})
        >>> tax.getAncestry(2)
        Lineage([Node(2), Node(1)])
        """
        return Lineage(self[str(taxid)])

    def isAncestorOf(self, taxid: Union[str, int],
                     child: Union[str, int]) -> bool:
        """
        Test if taxid is an ancestor of child

        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        child: str or int
            Taxonomic identification number

        Returns
        -------
        bool

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
        return self[str(taxid)].isAncestorOf(self[str(child)])

    def isDescendantOf(self, taxid: Union[str, int],
                       parent: Union[str, int]) -> bool:
        """
        Test if taxid is an descendant of parent

        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        parent: str or int
            Taxonomic identification number

        Returns
        -------
        bool

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
        return self[str(taxid)].isDescendantOf(self[str(parent)])

    def consensus(self, taxid_list: list[Union[str, int]],
                  min_consensus: float) -> Node:
        """
        Find a taxonomic consensus for the given
        taxid with a minimal agreement level.

        Parameters
        ----------
        taxid_list: list
            list of taxonomic identification numbers
        min_consensus: float
            minimal consensus level, between 0.5 and 1.
            Note that a minimal consensus of 1 will
            return the same result as `lastCommonNode()`

        Returns
        -------
        taxidTools._BaseNode

        Notes
        -----
        If no consensus can be found (for example because
        the Taxonomy contains multiple trees),
        an `IndexError` will be raised.

        See Also
        --------
        Taxonomy.lca


        Examples
        --------
        >>> node0 = Node(taxid = 0, name = "root",
                         rank = "root", parent = None)
        >>> node1 = Node(taxid = 1, name = "node1",
                         rank = "rank1", parent = node0)
        >>> node2 = Node(taxid = 2, name = "node2",
                         rank = "rank1", parent = node0)
        >>> node11 = Node(taxid = 11, name = "node11",
                          rank = "rank2", parent = node1)
        >>> node12 = Node(taxid = 12, name = "node12",
                          rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node0, node1, node2, node11, node12])
        >>> tax.consensus([11, 12, 2], 0.8)
        Node(0)
        >>> tax.consensus([11, 12, 2], 0.6)
        Node(1)
        """
        # Consensus under 50% is ambiguous
        if min_consensus <= 0.5 or min_consensus > 1:
            raise ValueError(
                "Minimal consensus should be above 0.5 and under 1")

        # Get lineages in REVERSED order
        lineages = [Lineage(self[str(txd)], ascending=False)
                    for txd in taxid_list]

        # Extend lineages so that they all are same size
        maxlen = max([len(lin) for lin in lineages])
        for lin in lineages:
            if len(lin) < maxlen:
                lin.extend([DummyNode()] * (maxlen - len(lin)))

        # Iterate over ranks descending to find last node above consensus level
        total = len(taxid_list)
        i = 0
        last = None

        while i < maxlen:
            count = Counter([lin[i] for lin in lineages])
            mostCommon = count.most_common(1)

            if mostCommon[0][1] / total >= min_consensus:
                if not(isinstance(mostCommon[0][0], DummyNode)):
                    # save current succesful consensus, and check the next one
                    last = mostCommon[0][0]
                i += 1
            else:
                break

        return last

    def lca(self, taxid_list: list[Union[str, int]]) -> Node:
        """
        Get lowest common node of a bunch of taxids

        Parameters
        ----------
        taxid_list: list
            list of taxonomic identification numbers

        Returns
        -------
        taxidTools._BasNode

        See Also
        --------
        Taxonomy.consensus

        Examples
        --------
        >>> node0 = Node(taxid = 0, name = "root",
                         rank = "root", parent = None)
        >>> node1 = Node(taxid = 1, name = "node1",
                         rank = "rank1", parent = node0)
        >>> node2 = Node(taxid = 2, name = "node2",
                         rank = "rank1", parent = node0)
        >>> node11 = Node(taxid = 11, name = "node11",
                          rank = "rank2", parent = node1)
        >>> node12 = Node(taxid = 12, name = "node12",
                          rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node0, node1, node2, node11, node12])
        >>> tax.lca([11, 12, 2])
        Node(0)
        """
        return self.consensus(taxid_list, 1)

    def distance(self, taxid1: Union[str, int],
                 taxid2: Union[str, int]) -> int:
        """
        Measures the distance between two nodes.

        Parameters
        ----------
        taxid1: str or int
            Taxonomic identification number
        taxid2: str or int
            Taxonomic identification number

        Returns
        -------
        int

        Examples
        --------
        >>> node0 = Node(taxid = 0, name = "root",
                         rank = "root", parent = None)
        >>> node1 = Node(taxid = 1, name = "node1",
                         rank = "rank1", parent = node0)
        >>> node2 = Node(taxid = 2, name = "node2",
                         rank = "rank1", parent = node0)
        >>> node11 = Node(taxid = 11, name = "node11",
                          rank = "rank2", parent = node1)
        >>> node12 = Node(taxid = 12, name = "node12",
                          rank = "rank2", parent = node1)
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

    def listDescendant(self, taxid: Union[str, int],
                       ranks: Optional[list] = None) -> list[Node]:
        """
        List all descendant of a node

        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        ranks: list, optional
            list of ranks for which to return nodes

        Returns
        -------
        list

        Examples
        --------
        >>> node0 = Node(taxid = 0, name = "root",
                         rank = "root", parent = None)
        >>> node1 = Node(taxid = 1, name = "node1",
                         rank = "rank1", parent = node0)
        >>> node2 = Node(taxid = 2, name = "node2",
                         rank = "rank1", parent = node0)
        >>> node11 = Node(taxid = 11, name = "node11", #
                          rank = "rank2", parent = node1)
        >>> node12 = Node(taxid = 12, name = "node12",
                          rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node0, node1, node2, node11, node12])
        >>> tax.listDescendant(1)
        [Node(11), Node(12)]
        >>> tax.listDescendant(2)
        []
        """
        current = copy(self[str(taxid)].children)
            # dont't want to update the original set!
        next = _flatten([child.children for child in current])

        all = current

        while next:
            all.update(next)
            current = next
            next = _flatten([child.children for child in current])

        if ranks:
            return [e for e in all if e.rank in ranks]
        return all

    def prune(self, taxid: Union[str, int], inplace: Optional[bool] = True) -> None:
        """
        Prune the Taxonomy at the given taxid

        Nodes not in the lineage (upwards and downwards)
        of the given taxid will be discarded.
        The Ancestors of the given taxid will be kept!

        Parameters
        ----------
        taxid: str or int
            taxid whose Lineage to keep
        inplace: bool, optional
            perfrom the operation inplace and mutate the underlying objects
            or return a mutated copy of the instance, keep the original unchanged

        Returns
        -------
        None

        Examples
        --------
        >>> node0 = Node(taxid = 0, name = "root",
                         rank = "root", parent = None)
        >>> node1 = Node(taxid = 1, name = "node1",
                         rank = "rank1", parent = node0)
        >>> node2 = Node(taxid = 2, name = "node2",
                         rank = "rank1", parent = node0)
        >>> node11 = Node(taxid = 11, name = "node11",
                          rank = "rank2", parent = node1)
        >>> node12 = Node(taxid = 12, name = "node12",
                          rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node0, node1, node2, node11, node12])
        >>> tax.prune(1)

        Ancestry is kept

        >>> tax.getAncestry(11)
        Lineage([Node(11), Node(1), Node(0)])

        But other branches are gone

        >>> tax.get('2')
        None

        We can keep a copy of the:

        >>> new = tax.prune(11, inplace=False)
        >>> new.get('12')
        KeyError: '12'
        >>> tax.getAncestry('12')
        Lineage([Node(12), Node(1), Node(0)])
        """
        if inplace:
            tax = self
        else:
            tax = self.copy()

        # Getting upstream nodes
        nodes = self.getAncestry(taxid)

        # Unlinking other branches from upstream nodes
        # No need to change parents of the other nodes,
        # they will be removed from Taxonomy
        for i in range(1, len(nodes)):
            nodes[i].children = [nodes[i - 1]]

        # Adding all downstream nodes
        nodes.extend(tax.listDescendant(taxid))

        # Update taxonomy
        tax.data = {node.taxid: node for node in nodes}

        if not inplace:
            return tax

    def filterRanks(self, ranks: Optional[list[str]] = linne(), inplace: Optional[bool] = True) -> None:
        """
        Filter a Taxonomy to keep only the ranks provided as arguments.

        Modifies Taxonomy in-place to keep only the Nodes at the requested
        ranks. Nodes will be modified to conserve linkage in the Taxonomy.

        Parameters
        ----------
        ranks: list
            List of ranks to keep. Must be sorted by ascending ranks.
        inplace: bool, optional
            perfrom the operation inplace and mutate the underlying objects
            or return a mutated copy of the instance, keep the original unchanged

        Returns
        -------
        None

        Notes
        -----
        In order to enforce ankering of the Taxonomy, the root node will
        always be kept.

        Examples
        --------
        >>> node1 = Node(1, rank = "root")
        >>> node11 = Node(11, rank = "rank1", parent = node1)
        >>> node111 = Node(111, rank = "rank2", parent = node11)
        >>> node001 = Node('001', rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node1, node11, node111, node001])
        >>> tax.filterRanks(['rank2', 'rank1', 'root'])
        >>> tax
        {Node(1), Node(11), DummyNode(tO841ymu), Node(111), Node(001)}

        DummyNodes are created as placeholders
        for missing ranks in the taxonomy:

        >>> node001.parent
        DummyNode(tO841ymu)

        Note that the root will be kept regardless of the input:

        >>> node1 = Node(1, rank = "root")
        >>> node11 = Node(11, rank = "rank1", parent = node1)
        >>> node111 = Node(111, rank = "rank2", parent = node11)
        >>> node001 = Node('001', rank = "rank2", parent = node1)
        >>> tax = Taxonomy.from_list([node1, node11, node111, node001])
        >>> tax.filterRanks(['rank2', 'rank1'])
        >>> tax
        {DummyNode(wmnar5QT), Node(001), Node(1), Node(11), Node(111)}

        It is also possible to keep the original instance intact and return a filtered copy:

        >>> new = tax.filterRanks(['rank1'], inplace=False)
        >>> new
        {DummyNode(wmnar5QT), Node(1), Node(11)}
        >>> tax
        {DummyNode(wmnar5QT), Node(001), Node(1), Node(11), Node(111)}
        """
        if inplace:
            tax = self
        else:
            tax = self.copy()

        # Create a list of nodes that will be used to update self
        new_nodes = []

        # First step, reduce tree
        # Remove unwanted nodes
        for node in tax.values():
            if node.rank in ranks:
                new_nodes.append(node)
            else:
                try:
                    node._relink()
                except TypeError:
                    # relinking a parent-less node raises TypeError
                    # The root will be kept whatever is asked to keep coherence
                    new_nodes.append(node)

        # Second step, expand tree
        # Reccursively add DummyNode to fill gaps
        root = tax.root
        if ranks[-1] == tax.root:
            ranks = ranks[:-1]
        new_nodes.extend(_insert_nodes_recc(root, ranks))

        # Update self
        tax.data = {node.taxid: node for node in new_nodes}

        if not inplace:
            return tax

    def write(self, path: str) -> None:
        """
        Write taxonomy to a JSON file.

        Parameters
        ----------
        path: str
            File path for the output

        See Also
        --------
        taxidTools.read_json
        """
        writer = json.dumps([node._to_dict()
                             for node in self.values()],
                            indent=4)
        with open(path, 'w') as fi:
            fi.write(writer)

    def toNewick(self, names: str = 'name') -> str:
        """
        Generate a Newock string fro the current taxonomy

        Export as Newick tree string for compatibility with other packages
        Import in ETE with format 8 (all names).
        Experimental feature

        Parameters
        ----------
        names: str
            Node attribute to use as node name, choice of 'name' or 'taxid'

        Returns
        -------
        str
        """

        def subtree(node, names):
            if names == 'name':
                namestring = str(node.name.replace(" ", "_"))
            elif names == 'taxid':
                namestring = str(node.taxid)

            if not node.children:
                return namestring
            subtrees = [subtree(child) for child in node.children]
            return f"({','.join(subtrees)}){namestring}"

        if names not in ['name', 'taxid']:
            raise ValueError("Parameter 'names' must be either 'name' or 'taxid'")

        return f"{subtree(self.root, names)};"


def _flatten(t: list) -> list:
    """
    Flatten nested list
    """
    return [item for sublist in t for item in sublist]


def _insert_nodes_recc(node: Node, ranks: list[str]) -> list[Node]:
    """
    Insert Dummy Nodes to fill gaps in ranks

    Reccursively relinks all nodes under node
    to follow the order given by ranks.
    Note that parents will be relinked with one dummy pro child!

    Notes:
    ------
    Assumes that the Taxonomy has been purged of not wanted
    ranks.

    Parameter:
    ----------
    node:
        The starting (top) node, should be the root
        when calling the function from the top level:
    ranks:
        Ascending list of ranks desired in the output.
        Should not include the root rank!

    Returns:
    --------
    list of added nodes
    """
    if 'root' in ranks:  #Move this to filter to properly check against root naming
        raise ValueError("'root' should not be included when filtering ranks. Use the Taxonomy.root property instead.")

    # if no ranks left return an empty list
    if not ranks:
        return []

    # Keep track of created dummyNodes
    new_nodes = _insert_dummies(node, ranks[-1])

    for child in node.children:
        new_nodes.extend(_insert_nodes_recc(child, ranks[:-1]))

    return new_nodes


def _insert_dummies(node, next_rank):
    dummies = []
    if node.children and next_rank:
        rerank = []
        # First check all children and keep track of
        # those that must be reranked
        for child in node.children:
            if child.rank != next_rank:
                rerank.append(child)
        # Then create dummies and insert between parent and child
        # Note: both steps uncoupled to avoid creating children
        # while iterating on children attribute.
        for child in rerank:
            dummy = DummyNode(rank=next_rank)
            dummy.insertNode(parent=node, child=child)
            dummies.append(dummy)
    elif next_rank:
        # Leaf node but still ranks left
        dummy = DummyNode(rank=next_rank, parent=node)
        dummies.append(dummy)
    return dummies
