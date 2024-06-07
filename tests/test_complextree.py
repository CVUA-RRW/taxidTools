import unittest
import taxidTools
from taxidTools.Taxonomy import _insert_nodes_recc, _insert_dummies

class TestComplexTree(unittest.TestCase):
    # Test Tree
    #
    # 0(-/-  /- 001) for testing filterRanks
    # |- 1
    # |  |- 11
    # |  |- 12
    # |      |- 121
    # |      |- 122
    # |- 2
    #    |- 21
    #    |- 22
    #    |- 23
    # (|-3) for testing _insert_nodes_recc

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

    def test_insertdummy(self):
        dummy = taxidTools.DummyNode(name= 'dummy', rank = 'rank2.5')
        dummy.insertNode(self.node2, self.node21)

        self.assertEqual(self.node21.parent, dummy)
        self.assertEqual(dummy.parent, self.node2)
        self.assertEqual(dummy.children, {self.node21})
        self.assertCountEqual(self.node2.children, {dummy, self.node22, self.node23})
        self.assertEqual(taxidTools.Lineage(self.node21), [self.node21, dummy, self.node2, self.node0])
        self.assertCountEqual(taxidTools.Lineage(self.node22), [self.node22, self.node2, self.node0])

    def test_relink(self):
        self.node2._relink()
        self.assertEqual(self.node21.parent, self.node0)
        self.assertEqual(self.node22.parent, self.node0)
        self.assertEqual(self.node23.parent, self.node0)
        self.assertCountEqual(self.node0.children, {self.node1, self.node21, self.node22, self.node23})
        self.assertCountEqual(taxidTools.Lineage(self.node22), [self.node22,self.node0])
        self.assertCountEqual(taxidTools.Lineage(self.node21), [self.node21,self.node0])
        self.assertCountEqual(taxidTools.Lineage(self.node23), [self.node23,self.node0])

    def test_consens(self):
        self.assertEqual(self.txd.consensus(["11", "12", "21", "22", "23"], 1).taxid,
                         "0")
        self.assertEqual(self.txd.consensus(["11", "12", "21", "22", "23"], 0.6).taxid,
                         "2")
        self.assertEqual(self.txd.consensus(["11", "12", "21", "22"], 0.51).taxid,
                         "0")
        self.assertEqual(self.txd.consensus(["11", "11", "12", "22"], 0.75).taxid,
                         "1")
        self.assertEqual(self.txd.consensus(["11", "11", "11", "22", "12"], 0.51).taxid,
                         "11")
        self.assertEqual(self.txd.consensus(["121", "121", "122", "22", "12"], 0.51).taxid,
                         "12")
        self.assertEqual(self.txd.consensus(["121", "121", "23", "22", "22"], 0.51).taxid,
                         "2")
        self.assertEqual(self.txd.lca(["11", "11", "12", "22"]).taxid,
                         "0")
        self.assertEqual(self.txd.lca(["11", "11", "12"]).taxid,
                         "1")

    def test_consensus_dummynodes(self):
        node0 = taxidTools.Node(0)
        node1 = taxidTools.Node(1, parent = node0)
        dummy1 = taxidTools.DummyNode(parent = node0)
        node2 = taxidTools.Node(2, parent = node1)
        node3 = taxidTools.Node(3, parent = dummy1)
        node4 = taxidTools.Node(4, parent = dummy1)
        tax = taxidTools.Taxonomy.from_list([node0, node1, dummy1, node2, node3, node4])
        cons = tax.consensus(["2", "3", "4"], 0.51)
        self.assertEqual(cons, node0)

    def test_dist(self):
        self.assertEqual(self.txd.distance("11", "12"), 2)
        self.assertEqual(self.txd.distance("11", "21"), 4)
        self.assertEqual(self.txd.distance("11", "2"), 3)
        self.assertEqual(self.txd.distance("11", "1"), 1)
        self.assertEqual(self.txd.distance("121", "22"), 5)

    def test_listDescendant(self):
        self.assertSetEqual(set(self.txd.listDescendant(1)),
                            set([self.node11, self.node12, self.node121, self.node122]))
        self.assertEqual(self.txd.listDescendant(11), set())
        self.assertEqual(set(self.txd.listDescendant(1, ranks=['rank3'])),
                        set([self.node121, self.node122]))

    def test_prune(self):
        self.txd.prune(1)
        ids = [node.taxid for node in self.txd.values()]
        self.assertSetEqual(set(ids), {"0", "1", "11", "12", "121", "122"})
        self.assertEqual(self.node0.children, {self.node1})

        self.new = self.txd.prune(121, inplace=False)
        ids = [node.taxid for node in self.new.values()]
        self.assertSetEqual(set(ids), {"0", "1", "12", "121"})
        ids = [node.taxid for node in self.txd.values()]
        self.assertSetEqual(set(ids), {"0", "1", "11", "12", "121", "122"})

        self.txd.prune(11)
        ids = [node.taxid for node in self.txd.values()]
        self.assertSetEqual(set(ids), {"11", "1", "0"})

    def test_filter(self):
        node001 = taxidTools.Node('001', name = "node001", rank = "rank3", parent = self.node0)
        self.txd.addNode(node001)
        self.txd.filterRanks(ranks=['rank3', 'rank1'])
        self.assertEqual(len(self.txd), 8)
        # test relinking
        self.assertEqual(self.node121.parent, self.node1)
        self.assertIsInstance(node001.parent, taxidTools.DummyNode)

        self.new = self.txd.filterRanks(ranks=["rank1"], inplace=False)
        self.assertEqual(len(self.txd), 8)
        self.assertEqual(len(self.new), 4)

    def test_insert_dummies(self):
        new = _insert_dummies(self.node1, 'newrank')
        self.assertEqual(len(new), 2)
        for node in self.node1.children:
            self.assertIsInstance(node, taxidTools.DummyNode)

    def test_insert_nodes_recc(self):
        node3 = taxidTools.Node('3', name = "node3", rank = "rank1", parent = self.node0)
        self.txd.addNode(node3)
        new_nodes = _insert_nodes_recc(self.node0, ['rank3', 'rank2', 'rank1.5', 'rank1'])
        self.assertEqual(len(new_nodes), 12)

        self.assertRaises(ValueError, _insert_nodes_recc, self.node0, ['root'])
