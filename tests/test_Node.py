import unittest
import taxidTools

class TestNode(unittest.TestCase):
    
    def setUp(self):
        self.node = taxidTools.Node(taxid = 123456)
        
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
        self.child1 = taxidTools.Node(taxid = 2, parent = self.node)
        self.child2 = taxidTools.Node(taxid = 3, parent = self.node)
        
        self.assertEqual(self.node.children, [self.child1, self.child2])

if __name__ == "__main__":
    unittest.main()