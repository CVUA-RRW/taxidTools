"""
Taxonomy object definition
"""


from __future__ import annotations
from typing import Union, Iterator, Optional
from collections import UserDict, Counter
import json 
from .Node import Node, DummyNode, _BaseNode
from .Lineage import Lineage
from .utils import linne


class Taxonomy(UserDict):
    """
    Store Taxonomy nodes
    
    A Taxonomy is instanciated as a dictionnary and 
    each Node can be accessed by its taxid.
    A Taoxonomy object can be instanciated directly from a dictionnary,
    iteratively with the method `Taxonomy.addNode` method or from a 
    list of taxdump files..
    
    Notes
    -----
    Taxonomy objects are mutable and some methods will modify the 
    underlying Node objects.
    Do a deep copy if you wish to keep the original object.
    
    A Taxonomy always assumes a unique root node.
    
    See Also
    --------
    Taxonomy.from_taxdump: load a Taxonomy object from taxdump files
    Taxonomy.from_list: load a Taxonomy object from a list of Node
    Taxonomy.from_json: load a Taxonomy from a previously exported json file
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
    
    >>> tax = Taxonomy.from_taxdump("nodes.dmp', 'rankedlineage.dmp')
    """
    
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        # create name dict for backward lookup
        self._namedict = {}
        for k, v in self.items():
            if v.name:
                self._namedict[v.name] = k
    
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
        
        Examples
        --------
        >>> txd = Taxonomy.from_list([Node(1), Node(2)])
        """
        for node in node_list:
            if not isinstance(node, _BaseNode):
                raise ValueError("Elements of node_list must be of type Node")
        
        as_dict = {node.taxid: node for node in node_list}
        
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
            txd[line[0]] = Node(taxid=line[0], rank=str(line[2]))
            parent_dict[str(line[0])] = line[1]  # storing parent id
        
        # Add names form rankedlineage
        for line in _parse_dump(rankedlineage):
            txd[line[0]].name = line[1]
        
        # Update parent info
        for k, v in parent_dict.items():
            txd[k].parent = txd[v]
        
        return cls(txd)
    
    @classmethod
    def from_json(cls, path: str) -> Taxonomy:
        """
        Load a Taxonomy from a previously exported json file.
        
        Parameters
        ----------
        path:
            Path of file to load
        
        See Also
        --------
        Taxonomy.write
        """
        # parse json
        with open(path, 'r') as fi:
            parser = json.loads(fi.read())
        
        txd = {}
        parent_dict = {}
        
        # Create nodes from records
        for record in parser:
            class_call = eval(record['type'])
            txd[record['_taxid']] = class_call(taxid=record['_taxid'],
                                               name=record['_name'],
                                               rank=record['_rank'])
            parent_dict[record['_taxid']] = record['_parent']
        
        # Update parent info
        for k, v in parent_dict.items():
            try:
                txd[k].parent = txd[v]
            except KeyError:
                pass
        
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
        """
        self[node.taxid] = node
        if node.name:
            self._namedict[node.name] = node.taxid
    
    def getTaxid(self, name: str) -> str:
        """
        Get taxid from name
        
        Parameters
        ----------
        name:
            Node name
        
        Examples
        --------
        >>> node = Node(1, "node", "rank")
        >>> tax = Taxonomy({'1':node})
        >>> tax.getTaxid('node')
        '1'
        """
        return self._namedict[name]
    
    def getName(self, taxid: Union[str, int]) -> str:
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
    
    def getRank(self, taxid: Union[str, int]) -> str:
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
    
    def getParent(self, taxid: Union[str, int]) -> Node:
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
        Node(1)
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
        [Node(2)]
        """
        return self[str(taxid)].children
    
    def getAncestry(self, taxid: Union[str, int]) -> Lineage:
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
        Lineage([Node(2), Node(1)])
        """
        return Lineage(self[str(taxid)])
    
    def isAncestorOf(self, taxid: Union[str, int], 
                     child: Union[str, int]) -> bool:
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
        return self[str(taxid)].isAncestorOf(self[str(child)])
    
    def isDescendantOf(self, taxid: Union[str, int], 
                       parent: Union[str, int]) -> bool:
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
        return self[str(taxid)].isDescendantOf(self[str(parent)])
    
    def consensus(self, taxid_list: list[Union[str, int]], 
                  min_consensus: float) -> Node:
        """
        Find a taxonomic consensus for the given 
        taxid with a minimal agreement level.
        
        Parameters
        ----------
        taxid_list: 
            list of taxonomic identification numbers
        min_consensus: 
            minimal consensus level, between 0.5 and 1.
            Note that a minimal consensus of 1 will 
            return the same result as `lastCommonNode()`
        
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
        taxid_list: 
            list of taxonomic identification numbers
        
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
        taxid1: 
            Taxonomic identification number
        taxid2: 
            Taxonomic identification number
        
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
        taxid: 
            Taxonomic identification number
        ranks:
            list of ranks for which to return nodes
        
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
        current = self[str(taxid)].children
        next = _flatten([child.children for child in current])
        
        all = current
        
        while next:
            all.extend(next)
            current = next
            next = _flatten([child.children for child in current])
        
        return all
    
    def prune(self, taxid: Union[str, int]) -> None:
        """
        Prune the Taxonomy at the given taxid
        
        Nodes not in the lineage (upwards and downwards)
        of the given taxid will be discarded.
        The Ancestors of the given taxid will be kept!
        
        Parameters
        ----------
        taxid: 
            taxid whose Lineage to keep
        
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
        
        Ancestry is kept_
        
        >>> tax.getAncestry(11)
        Lineage([Node(11), Node(1), Node(0)])
        
        But other branches are gone
        
        >>> tax.get('2')
        KeyError: '2'
        """
        # Getting upstream nodes
        nodes = self.getAncestry(taxid)
        
        # Unlinking other branches from upstream nodes
        # No need to change parents of the other nodes, 
        # they will be removed from Taxonomy
        for i in range(1, len(nodes)):
            nodes[i]._children = [nodes[i - 1]]
        
        # Adding all downstream nodes
        nodes.extend(self.listDescendant(taxid))
        
        # Update taxonomy
        self.data = {node.taxid: node for node in nodes}
    
    def filterRanks(self, ranks: list[str] = linne()) -> None:
        """
        Filter a Taxonomy to keep only the ranks provided as arguments.
        
        Modifies Taxonomy in-place to keep only the Nodes at the requested
        ranks. Nodes will be modified to conserve linkage in the Taxonomy.
        
        Parameters
        ----------
        ranks:
            List of ranks to keep. Must be sorted by ascending ranks.
        
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
        
        DummyNodes are created s placeholders 
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
        """
        # Create a list of nodes that will be used to update self
        new_nodes = []
        
        # First step, reduce tree
        # Remove unwanted nodes
        for node in self.values():
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
        root = self.root
        if ranks[-1] == self.root:
            ranks = ranks[:-1]
        new_nodes.extend(_insert_nodes_recc(root, ranks))
        
        # Update self
        self.data = {node.taxid: node for node in new_nodes}
    
    def write(self, path: str) -> None:
        """
        Write taxonomy to a JSON file.
        
        Parameters
        ----------
        path:
            File path for the output
        """
        writer = json.dumps([node._to_dict() 
                             for node in self.values()], 
                            indent=4)
        with open(path, 'w') as fi:
            fi.write(writer)
    
    @property
    def root(self) -> Node:
        """
        Returns the root Node, assumes a single root shared by all Nodes
        """
        anynode = next(iter(self.values()))
        return Lineage(anynode)[-1]
        
    def __repr__(self):
        return f"{set(self.values())}"


def load(path: str) -> Taxonomy:
    """
    Load a Taxonomy from a previously exported json file.
    
    Parameters
    ----------
    path:
        Path of file to load
    
    See Also
    --------
    Taxonomy.write
    """
    return Taxonomy.from_json(path)


def _parse_dump(filepath: str) -> Iterator:
    """
    Dump file line iterator, returns a yields of fields
    """
    with open(filepath, 'r') as dmp:
        for line in dmp:
            yield [item.strip() for item in line.split("|")]


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
    
    Notes:
    ------
    Assumes that the Taxonomy has bee purged of non wanted 
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