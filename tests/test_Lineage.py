import unittest
import taxidTools

class TestLineage(unittest.TestCase):
    
    def setUp(self):
        self.parent = taxidTools.Node(taxid = 0, name = "root", rank = "root", parent = None)
        self.rank1 = taxidTools.Node(taxid = 1, name = "node1", rank = "rank1", parent = self.parent)
    
    def test_init(self):
        # From Node
        self.lin = taxidTools.Lineage(self.rank1)
        self.linrev = taxidTools.Lineage(self.rank1, ascending = False)
        self.assertEqual(len(self.lin), 2)
        self.assertEqual(self.lin[0].taxid, "1")
        self.assertEqual(self.lin[1].taxid, "0")
        self.assertEqual(len(self.linrev), 2)
        self.assertEqual(self.linrev[0].taxid, "0")
        self.assertEqual(self.linrev[1].taxid, "1")
    
    def test_filter(self):
        self.rank2 = taxidTools.Node(taxid = 2, name = "node2", rank = "rank2", parent = self.rank1)
        self.rank3 = taxidTools.Node(taxid = 3, name = "node3", rank = "rank3", parent = self.rank2)
        
        self.lin2 = taxidTools.Lineage(self.rank3)
        fil= self.lin2.filter(["rank1", "rank3"])
        self.assertEqual(len(fil), 2)
        self.assertEqual(fil[0], self.rank3)
        
        