import unittest
import taxidTools

class TestComplexTree(unittest.TestCase):
    # Test Tree
    #
    # 0
    # |- 1
    # |  |- 11
    # |  |- 12
    # |      |- 121
    # |      |- 122
    # |-2
    #    |- 21
    #    |- 22
    #    |- 23
    
    def setUp(self):
        self.node0 = taxidTools.Node(taxid = 0, name = "root", rank = "root", parent = None)
        self.node1 = taxidTools.Node(taxid = 1, name = "node1", rank = "rank1", parent = self.node0)
        self.node2 = taxidTools.Node(taxid = 2, name = "node2", rank = "rank1", parent = self.node0)
        self.node11 = taxidTools.Node(taxid = 11, name = "node11", rank = "rank2", parent = self.node1)
        self.node12 = taxidTools.Node(taxid = 12, name = "node12", rank = "rank2", parent = self.node1)
        self.node21 = taxidTools.Node(taxid = 21, name = "node21", rank = "rank2", parent = self.node2)
        self.node22 = taxidTools.Node(taxid = 22, name = "node22", rank = "rank2", parent = self.node2)
        self.node23 = taxidTools.Node(taxid = 23, name = "node23", rank = "rank2", parent = self.node2)
        self.node121 = taxidTools.Node(taxid = 121, name = "node121", rank = "rank3", parent = self.node12)
        self.node122 = taxidTools.Node(taxid = 122, name = "node122", rank = "rank3", parent = self.node12)
        
        nodes = {
            "0" : self.node0,
            "1" : self.node1,
            "2" : self.node2,
            "11" : self.node11,
            "12" : self.node12,
            "21" : self.node21,
            "22" : self.node22,
            "23" : self.node23,
            "121" : self.node121,
            "122" : self.node122
            }
            
        self.txd = taxidTools.Taxonomy(nodes)
        
    
    def test_consens(self):
        self.assertEqual(self.txd.consensus(["11", "12", "21", "22", "23"], 1),
                         "0")
        self.assertEqual(self.txd.consensus(["11", "12", "21", "22", "23"], 0.6), 
                         "2")
        self.assertEqual(self.txd.consensus(["11", "12", "21", "22"], 0.51),
                         "0")
        self.assertEqual(self.txd.consensus(["11", "11", "12", "22"], 0.75),
                         "1")
        self.assertEqual(self.txd.consensus(["11", "11", "11", "22", "12"], 0.51),
                         "11")
        self.assertEqual(self.txd.consensus(["121", "121", "122", "22", "12"], 0.51),
                         "12")
        self.assertEqual(self.txd.consensus(["121", "121", "23", "22", "22"], 0.51),
                         "2")
        self.assertEqual(self.txd.lca(["11", "11", "12", "22"]),
                         "0")
        self.assertEqual(self.txd.lca(["11", "11", "12"]),
                         "1")
    
    def test_dist(self):
        self.assertEqual(self.txd.distance("11", "12"), 2)
        self.assertEqual(self.txd.distance("11", "21"), 4)
        self.assertEqual(self.txd.distance("11", "2"), 3)
        self.assertEqual(self.txd.distance("11", "1"), 1)
        self.assertEqual(self.txd.distance("121", "22"), 5)
    
    def test_listDescendant(self):
        self.assertSetEqual(set(self.txd.listDescendant(1)),
                            set([self.node11, self.node12, self.node121, self.node122]))
        self.assertEqual(self.txd.listDescendant(11), [])
    
    def test_subtree(self):
        subtree = self.txd.subtree(1)
        ids = [node.taxid for node in subtree.values()]
        self.assertSetEqual(set(ids), {"1", "11", "12", "121", "122"})
        
        subtree = self.txd.subtree(11)
        ids = [node.taxid for node in subtree.values()]
        self.assertSetEqual(set(ids), {"11"})