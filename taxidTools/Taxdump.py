"""
Taxdump object definition
"""


from __future__ import annotations
from typing import List, Union, Iterator
from collections import UserDict, Counter
from .Node import Node
from .Lineage import Lineage


class Taxdump(UserDict):
    """
    Store Taxdump nodes
    """
   
    def _addNode(self, node: Node) -> None:
        self[node.taxid] = node
    
    def getName(self, taxid: Union[str,int]) -> str:
        """
        Get taxid name
        
        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        
        Returns
        -------
        str
            node name
        """
        return self[str(taxid)].name
    
    def getRank(self, taxid: Union[str,int]) -> str:
        """
        Get taxid rank
        
        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        
        Returns
        -------
        str
            node rank
        """
        return self[str(taxid)].rank
    
    def getParent(self, taxid: Union[str,int]) -> str:
        """
        Retrieve parent taxid
        
        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        
        Returns
        -------
        str
            Parent taxid
        """
        return self[str(taxid)].parent
    
    def getAncestry(self, taxid: Union[str,int]) -> Lineage:
        """
        Retrieve the ancestry of the given taxid
        
        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        
        Returns
        -------
        Lineage
            List of ancestors (from the lowest to the highest node)
        """
        return Lineage(self[str(taxid)])
    
    def isAncestorOf(self, taxid: Union[str,int], child: Union[str,int]) -> bool:
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
        taxid: str or int
            Taxonomic identification number
        
        parent: str or int
            Taxonomic identification number
        
        Returns
        -------
        bool
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
        taxid_list: list
            list of taxonomic identification numbers
        min_consensus: float
            minimal consensus level, between 0.5 and 1.
            Note that a minimal consensus of 1 will return the same result as `lastCommonNode()`
        
        Returns
        -------
        str
            Consensus taxid
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
        taxid_list: list
            list of taxonomic identification numbers
        Returns
        -------
        str
            Lowest common taxid
        """
        return self.consensus(taxid_list, 1)
    
    def distance(self, taxid1: Union[str,int], taxid2: Union[str,int]) -> int:
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
            Distance value
        """
        lca = self.lca([taxid1, taxid2])
        
        d1 = len(Lineage(self[taxid1])) - 1
        d2 = len(Lineage(self[taxid2])) - 1
        dlca = len(Lineage(self[lca])) - 1
        
        return d1 + d2 - 2 * dlca
    
    def listChildren(self, taxid: Union[str, int]) -> list:
        """
        List all descendant of node
        
        Parameters
        ----------
        taxid: str or int
            Taxonomic identification number
        
        Returns
        -------
        list
            List of all descendant nodes 
        """
        current = self[str(taxid)].children
        next = flatten([child.children for child in current])
        
        all = current
        
        while next:
            all.extend(next)
            current = next
            next = flatten([child.children for child in current])
        
        return all
    
    
    def subtree(self, new_root: Union[str, int]) -> Taxdump:
        """
        Returns a sutree with the given taxid as new root.
        
        Parameters
        ----------
        new_root: int or str
            taxid of the new root
            
        Returns
        -------
        Taxdump
            A new Taxdump object
        """
        new_root_node = self[str(new_root)]
        nodes = self.listChildren(new_root)
        
        new = Taxdump()
        new._addNode(new_root_node)
        
        for node in nodes:
            new._addNode(node)
        
        return new
    

flatten = lambda t: [item for sublist in t for item in sublist]

def load_taxdump(nodes: str, rankedlineage: str) -> Taxdump:
    """
    Parse NCBI taxdump files
    
    Parameters
    ----------
    nodes: str
        Path to the nodes.dmp file
    rankedlineage: str
        Path to the rankedlineage.dmp file
    
    Returns
    -------
    Taxdump
        A taxdump object
    """
    txd = Taxdump()
    parent_dict = {}
    
    # Creating nodes
    for line in _parse_dump(nodes):
        txd._addNode(Node(taxid = line[0], rank = str(line[2])))
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