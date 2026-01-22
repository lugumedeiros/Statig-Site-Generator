import unittest

from textnode import *
from textnode import _split_nodes_image, _split_nodes_delimiter, _split_nodes_link

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

        result = _split_nodes_delimiter(nodes, "**", TextType.BOLD)

        self.assertEqual(len(result), 5)

        self.assertEqual(result[0], nodes[0])

        self.assertEqual(result[1].text_type, TextType.BOLD)
        self.assertEqual(result[1].text, "Hell")

        self.assertEqual(result[2].text_type, TextType.TEXT)

        self.assertEqual(result[3].text_type, TextType.BOLD)

        self.assertEqual(result[4].text_type, TextType.TEXT)
        self.assertEqual(result[4].text, "!")

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = _split_nodes_image([node])
        self.assertListEqual([
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),],
            new_nodes,
        )

    def test_text_to_nodes(self):
        text_test = r"This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text_test)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertTrue(len(nodes) == len(expected))
        for i in range(len(nodes)):
            self.assertTrue(expected[i].text == nodes[i].text)
            self.assertTrue(expected[i].text_type == nodes[i].text_type)
            self.assertTrue(expected[i].url == nodes[i].url)

if __name__ == "__main__":
    unittest.main()