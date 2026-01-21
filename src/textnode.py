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


def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    def is_plain_text(node:TextNode) -> bool:
        return node.text_type == TextType.TEXT


    def get_pieces(text:str, mark:str) -> tuple[str|None, str|None, str|None]:
        if mark in text:
            pieces = text.split(mark)
            if len(pieces) > 2:
                inner = pieces[1]
                left = pieces[0]
                right = mark.join(pieces[2:])
                return left, inner, right
        return None, None, None
    
    def get_node(text, text_type, url=None) -> TextNode:
        return TextNode(text, text_type)

    new_nodes = []
    for node in old_nodes:
        if is_plain_text(node):
            text = node.text
            while True:
                left, inner, right = get_pieces(text, delimiter)
                if left is None:
                    new_nodes.append(get_node(text, TextType.TEXT))
                    break
                else:
                    if len(left) > 0:
                        new_nodes.append(get_node(left, TextType.TEXT))
                    if len(inner) > 0:
                        new_nodes.append(get_node(inner, text_type))
                    text = right

        else:
            new_nodes.append(node)
    return new_nodes


if __name__ == "__main__":
    # node = TextNode("This is a text node", TextType.TEXT)
    # html_node = TextNode.text_node_to_html_node(node)
    # print(html_node.tag, None)
    # print(html_node.value, "This is a text node")

    ############

    nodes = [TextNode("IM BOLD", TextType.BOLD), TextNode("**Hell**o **world**!", TextType.TEXT)]

    result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    print(len(result), 5)
    print(result[0] == nodes[0])
    print(result[1].text_type, TextType.BOLD)
    print(result[1].text, "Hell")
    print(result[2].text_type, TextType.TEXT)
    print(result[3].text_type, TextType.BOLD)
    print(result[4].text_type, TextType.TEXT)
    print(result[4].text, "!")