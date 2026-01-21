import unittest

from textnode import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a different node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.TEXT)
        node5 = TextNode("This is a text node", TextType.BOLD, "not_in_use.com")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node5)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = TextNode.text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_mixed_nodes_with_bold(self):
        nodes = [
            TextNode("IM BOLD", TextType.BOLD),
            TextNode("**Hell**o **world**!", TextType.TEXT),
        ]

        result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(len(result), 5)

        self.assertEqual(result[0], nodes[0])

        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, "Hell")

        self.assertEqual(result[2].text_type, TextType.TEXT)

        self.assertEqual(result[3].text_type, TextType.BOLD)

        self.assertEqual(result[4].text_type, TextType.TEXT)
        self.assertEqual(result[4].text, "!")

if __name__ == "__main__":
    unittest.main()