import unittest
from .context import taxidTools

class TestTaxdump(unittest.TestCase):
    
    def setUp(self):
        self.parent = taxidTools.Node(taxid = 0, name = "root", rank = "root", parent = None)
        self.child = taxidTools.Node(taxid = 1, name = "child", rank = "child", parent = self.parent)
        self.txd = taxidTools.Taxdump()
        self.txd._addNode(self.child)
        self.txd._addNode(self.parent)
    
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

