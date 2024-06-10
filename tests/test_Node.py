import unittest
import taxidTools

class TestNode(unittest.TestCase):

    def setUp(self):
        self.node = taxidTools.Node(taxid = 123456)
        self.midnode = taxidTools.Node(taxid = 2, parent = self.node)
        self.lownode = taxidTools.Node(taxid = 3, parent = self.midnode)

    def test_taxid(self):
        self.assertIsInstance(self.node.taxid, str)
        self.assertEqual(self.node.taxid, "123456")

    def test_name(self):
        name = "TestName"
        self.node.name = name
        self.assertEqual(self.node.name, name)

    def test_rank(self):
        rank = "TestRank"
        self.node.rank = rank
        self.assertEqual(self.node.rank, rank)

    def test_parent(self):
        parent1 = taxidTools.Node(taxid = 789)
        self.node.parent = parent1
        self.assertEqual(self.node.parent.taxid, "789")

    def test_children(self):
        self.assertEqual(self.node.children, {self.midnode})

    def test_ancestry(self):
        self.assertEqual(self.lownode.isDescendantOf(self.node), True)
        self.assertEqual(self.node.isDescendantOf(self.lownode), False)
        self.assertEqual(self.lownode.isAncestorOf(self.node), False)
        self.assertEqual(self.node.isAncestorOf(self.lownode), True)

    def test_dummy_insert(self):
        dummy = taxidTools.DummyNode()
        dummy.insertNode(parent = self.midnode, child = self.lownode)
        self.assertEqual(dummy.parent, self.midnode)
        self.assertEqual(dummy.children, {self.lownode})
        self.assertEqual(self.midnode.children, {dummy})
        self.assertEqual(self.lownode.parent, dummy)

    def test_relink(self):
        self.midnode._relink()
        self.assertEqual(self.lownode.parent, self.node)
        self.assertEqual(len(self.node.children), 1)
        self.assertIn(self.lownode, self.node.children)

    def test_merged(self):
        self.merged = taxidTools.MergedNode(1234, 2)
        self.assertEqual(self.merged.new_node, "2")
        self.assertEqual(self.merged.taxid, "1234")