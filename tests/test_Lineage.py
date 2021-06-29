import unittest
import taxidTools

class TestLineage(unittest.TestCase):
    
    def setUp(self):
        self.parent = taxidTools.Node(taxid = 0, name = "root", rank = "root", parent = None)
        self.child = taxidTools.Node(taxid = 1, name = "child", rank = "child", parent = self.parent)
        self.lin = taxidTools.Lineage(self.child)
        self.linrev = taxidTools.Lineage(self.child, ascending = False)
        
    def test_init(self):
        self.assertEqual(len(self.lin), 2)
        self.assertEqual(self.lin[0].taxid, "1")
        self.assertEqual(self.lin[1].taxid, "0")
        self.assertEqual(len(self.linrev), 2)
        self.assertEqual(self.linrev[0].taxid, "0")
        self.assertEqual(self.linrev[1].taxid, "1")
        