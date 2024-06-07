import unittest
import taxidTools

class TestLineage(unittest.TestCase):

    def setUp(self):
        self.parent = taxidTools.Node(taxid = 0, name = "root", rank = "root", parent = None)
        self.rank1 = taxidTools.Node(taxid = 1, name = "node1", rank = "rank1", parent = self.parent)
        self.rank2 = taxidTools.Node(taxid = 2, name = "node2", rank = "rank2", parent = self.rank1)
        self.rank3 = taxidTools.Node(taxid = 3, name = "node3", rank = "rank3", parent = self.rank2)


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
        fil1 = taxidTools.Lineage(self.rank3)
        fil1.filter(["rank3", "rank1"])
        self.assertEqual(len(fil1), 2)

        fil2 = taxidTools.Lineage(self.rank3)
        fil2.filter(["rank3", "norank", "rank1"])
        self.assertEqual(len(fil2), 3)
        self.assertTrue(isinstance(fil2[1], taxidTools.DummyNode))

        fil3 = taxidTools.Lineage(self.rank3)
        fil3.filter(["rank1", "rank3", "rank99", "rank2"])
        self.assertTrue(isinstance(fil3[2], taxidTools.DummyNode))
        self.assertEqual(fil3[0], self.rank1)
        self.assertEqual(fil3[1], self.rank3)
        self.assertEqual(fil3[3], self.rank2)
