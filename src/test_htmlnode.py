import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("a", "test", ["is"], {"run":"ning"})
        self.assertEqual(node.props_to_html(), 'run="ning"')
if __name__ == "__main__":
    unittest.main()