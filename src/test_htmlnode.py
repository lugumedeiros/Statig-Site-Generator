import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "test", ["is"], {"run":"ning"})
        self.assertEqual(node.props_to_html(), 'run="ning"')

class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("a", "test", {"run":"ning"})
        self.assertEqual(node.to_html(), "<a run=\"ning\">test</a>")

if __name__ == "__main__":
    unittest.main()