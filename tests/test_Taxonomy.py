import os
import unittest
from tempfile import TemporaryDirectory


import taxidTools


current_path = os.path.dirname(__file__)
nodes = os.path.join(current_path, "data", "mininodes.dmp")
rankedlineage = os.path.join(current_path, "data", "minirankedlineage.dmp")
merged = os.path.join(current_path, "data", "minimerged.dmp")


class TestTaxdump(unittest.TestCase):

    def setUp(self):
        self.workdir = TemporaryDirectory()
        self.parent = taxidTools.Node(taxid = 0, name = "root", rank = "root", parent = None)
        self.child = taxidTools.Node(taxid = 1, name = "child", rank = "child", parent = self.parent)
        self.txd = taxidTools.Taxonomy({'0': self.parent, '1': self.child})

    def tearDown(self):
        self.workdir.cleanup()

    def test_factory_dict(self):
        self.txd = taxidTools.Taxonomy({'0': self.parent, '1': self.child})
        self.assertEqual(len(self.txd.keys()), 2)

    def test_factory_add_node(self):
        self.txd = taxidTools.Taxonomy()
        self.txd.addNode(self.child)
        self.txd.addNode(self.parent)
        self.assertEqual(len(self.txd.keys()), 2)

    def test_factory_list(self):
        self.txd = taxidTools.Taxonomy.from_list([self.parent, self.child])
        self.assertEqual(len(self.txd.keys()), 2)

    def test_factory_taxdump(self):
        self.txd = taxidTools.read_taxdump(nodes, rankedlineage, merged)
        self.assertEqual(self.txd["9913"].parent.taxid, "9903")

        ancestry = taxidTools.Lineage(self.txd["9903"])
        self.assertEqual(len(ancestry), 29)
        self.assertEqual(ancestry[-1].taxid, "1")

        self.assertEqual(self.txd["999999"], self.txd["9103"])

    def test_IO_json(self):
        self.txd = taxidTools.read_taxdump(nodes, rankedlineage, merged)
        self.txd.write(os.path.join(self.workdir.name, "test.json"))
        self.reload = taxidTools.read_json(os.path.join(self.workdir.name, "test.json"))

        self.assertEqual(self.txd["999999"], self.txd["9103"])

        ancestry = taxidTools.Lineage(self.reload["9903"])
        self.assertEqual(len(ancestry), 29)
        self.assertEqual(ancestry[-1].taxid, "1")

        self.txd.filterRanks(['genus', 'none'])
        self.txd.write(os.path.join(self.workdir.name, "test2.json"))
        test2 = taxidTools.read_json(os.path.join(self.workdir.name, "test2.json"))
        ancestry = taxidTools.Lineage(test2["9903"])
        self.assertIsInstance(ancestry[1], taxidTools.DummyNode)

    def test_getters(self):
        self.assertEqual(self.txd.getName(1), "child")
        self.assertEqual(self.txd.getRank(1), "child")
        self.assertEqual(self.txd.getParent(1).taxid, "0")

    def test_getAncestry(self):
        lin = self.txd.getAncestry(1)
        self.assertEqual(len(lin), 2)
        self.assertEqual(lin[0].taxid, "1")
        self.assertEqual(lin[1].taxid, "0")

    def test_ancestry_tests(self):
        self.assertTrue(self.txd.isAncestorOf(0,1))
        self.assertFalse(self.txd.isAncestorOf(1,0))
        self.assertFalse(self.txd.isAncestorOf(1,1))

        self.assertTrue(self.txd.isDescendantOf(1,0))
        self.assertFalse(self.txd.isDescendantOf(0,1))
        self.assertFalse(self.txd.isDescendantOf(1,1))

    def test_copy(self):
        self.new = self.txd.copy()
        self.txd.data = {}
        with self.assertRaises(taxidTools.InvalidNodeError):
            _ = self.txd[0]
        self.assertIsNotNone(self.new.get('0', None))

    def test_InvalidNodeError(self):
        self.assertRaises(taxidTools.InvalidNodeError, self.txd.__getitem__, "notataxid")
    
    def test_MergedNnode(self):
        self.merged = taxidTools.MergedNode(10, 1)
        self.txd = taxidTools.Taxonomy.from_list([self.parent, self.child, self.merged])
        self.assertEqual(self.txd['1'], self.txd['10'])
        # assign a non-existing node and raise anerror
        self.merged = taxidTools.MergedNode(11, 99)
        self.assertRaises(taxidTools.InvalidNodeError, self.txd.__getitem__, "11")
