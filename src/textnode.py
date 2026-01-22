from enum import Enum
from htmlnode import *
import util

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


def _is_plain_text(node:TextNode) -> bool:
    return node.text_type == TextType.TEXT

def _get_markdown_pieces(text:str, mark:str) -> tuple[str|None, str|None, str|None]:
    if mark in text:
        pieces = text.split(mark)
        if len(pieces) > 2:
            inner = pieces[1]
            left = pieces[0]
            right = mark.join(pieces[2:])
            return left, inner, right
        if len(pieces) == 2:
            return pieces[0], mark, pieces[1]
        if len(pieces) == 1:
            return pieces[0], None, None

    return None, None, None

def _get_node(text, text_type, url=None) -> TextNode:
    if text_type is TextType.IMAGE:
        text, url = util.extract_markdown_images(text)[0]
    elif text_type is TextType.LINK:
        text, url = util.extract_markdown_links(text)[0]

    return TextNode(text, text_type, url)

def split_nodes_delimiter(old_nodes:list[TextNode], delimiter:str, text_type:TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not _is_plain_text(node):
            new_nodes.append(node)
            continue

        text = node.text
        while True:
            if len(text) == 0:
                break
            left, inner, right = _get_markdown_pieces(text, delimiter)
            if inner is None:
                new_nodes.append(_get_node(text, TextType.TEXT))
                break
            else:
                if len(left) > 0:
                    new_nodes.append(_get_node(left, TextType.TEXT))
                if inner != delimiter:
                    if len(inner) > 0:
                        if text_type is not TextType.IMAGE or text_type is not TextType.LINK:
                            new_nodes.append(_get_node(inner, text_type))
                else:
                    if text_type is TextType.IMAGE or text_type is TextType.LINK:
                        new_nodes.append(_get_node(inner, text_type))

                text = right

    return new_nodes

def _get_embedded(old_nodes:list[TextNode], node_type:TextType) -> list[TextNode]:
    def get_mark(alt, url, ttype):
        return f"![{alt}]({url})" if ttype is TextType.IMAGE else f"[{alt}]({url})"
    
    def is_embedded(node_type):
        return node_type is TextType.IMAGE or node_type is TextType.LINK
    
    if not is_embedded(node_type):
        return old_nodes
    
    new_nodes = []
    for node in old_nodes:
        extracted_marks = util.extract_markdown_images(node.text)
        tmp_nodes = [node]
        for alt, url in extracted_marks:
            mark = get_mark(alt, url, node_type)
            tmp_nodes = split_nodes_delimiter(tmp_nodes, mark, node_type)
        new_nodes += tmp_nodes
    return new_nodes

def split_nodes_image(old_nodes:list[TextNode]) -> list[TextNode]:
    return _get_embedded(old_nodes, TextType.IMAGE)

def split_nodes_link(old_nodes:list[TextNode]) -> list[TextNode]:
    return _get_embedded(old_nodes, TextType.LINK)

if __name__ == "__main__":
    # node = TextNode("This is a text node", TextType.TEXT)
    # html_node = TextNode.text_node_to_html_node(node)
    # print(html_node.tag, None)
    # print(html_node.value, "This is a text node")

    ############

    # nodes = [TextNode("IM BOLD", TextType.BOLD), TextNode("**Hell**o **world**!", TextType.TEXT)]

    # result = split_nodes_delimiter(nodes, "**", TextType.BOLD)

    # print(len(result), 5)
    # print(result[0] == nodes[0])
    # print(result[1].text_type, TextType.BOLD)
    # print(result[1].text, "Hell")
    # print(result[2].text_type, TextType.TEXT)
    # print(result[3].text_type, TextType.BOLD)
    # print(result[4].text_type, TextType.TEXT)
    # print(result[4].text, "!")

    ##########################

    # nodes = [
    #     TextNode(
    #         "Texto antes ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg) texto depois",
    #         TextType.TEXT
    #     )
    # ]

    # result = _get_embedded(nodes, TextType.IMAGE)

    # print(len(result), 3)

    # print(result[0].text_type, TextType.TEXT)
    # print(result[0].text, "Texto antes ")

    # print(result[1].text_type, TextType.IMAGE)
    # print(result[1].text, "obi wan")

    # print(result[2].text_type, TextType.TEXT)
    # print(result[2].text, " texto depois")
    ##########################################
    node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
    new_nodes = split_nodes_image([node])
    x = [
        TextNode("This is text with an ", TextType.TEXT),
        TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        TextNode(" and another ", TextType.TEXT),
        TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")
        ]
    
    print(new_nodes)
    
    pass