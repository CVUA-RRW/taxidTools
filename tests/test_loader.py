import os
import unittest
from .context import taxidTools


current_path = os.path.dirname(__file__)
nodes = os.path.join(current_path, "data", "mininodes.dmp")
rankedlineage = os.path.join(current_path, "data", "minirankedlineage.dmp")


class TestLoader(unittest.TestCase):
    
    def setUp(self):
        self.txd = taxidTools.load_taxdump(nodes, rankedlineage)
    
    def test_loading(self):
        self.assertEqual(self.txd["9913"].parent.taxid, "9903")
        
        ancestry = taxidTools.Lineage(self.txd["9903"])
        self.assertEqual(len(ancestry), 29)
        self.assertEqual(ancestry[-1].taxid, "1")
