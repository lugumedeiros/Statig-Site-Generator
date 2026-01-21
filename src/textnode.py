from enum import Enum
from htmlnode import *

class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text:str, text_type:TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    @staticmethod
    def text_node_to_html_node(text_node:"TextNode") -> LeafNode:
        match text_node.text_type:
            case TextType.TEXT:
                return LeafNode(tag=None, value=text_node.text)
            case TextType.BOLD:
                return LeafNode(tag='b', value=text_node.text)
            case TextType.ITALIC:
                return LeafNode(tag='i', value=text_node.text)
            case TextType.CODE:
                return LeafNode(tag='code', value=text_node.text)
            case TextType.LINK:
                return LeafNode(tag='a', value=text_node.text, props={"href": text_node.url})
            case TextType.IMAGE:
                return LeafNode(tag='img', value=None, props={"src": text_node.url, "alt":text_node.text})

    def __eq__(self, other:"TextNode"):
        check_text = self.text == other.text
        check_type = self.text_type == other.text_type
        check_url = self.url == other.url
        return check_text and check_type and check_url
    
    def __repr__(self):
        strformat = f"TextNode({self.text}, {self.text_type.name}, {self.url})"
        return strformat
    
if __name__ == "__main__":
    node = TextNode("This is a text node", TextType.TEXT)
    html_node = TextNode.text_node_to_html_node(node)
    print(html_node.tag, None)
    print(html_node.value, "This is a text node")