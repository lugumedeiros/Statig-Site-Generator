import unittest

from util import *

class TestTextNode(unittest.TestCase):

    def test_extract_markdown(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_links(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://mytube.com/fJRm4Vk) link"
        )
        self.assertListEqual([("obi wan", "https://mytube.com/fJRm4Vk")], matches)

if __name__ == "__main__":
    unittest.main()