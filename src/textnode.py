from enum import Enum

class TextType(Enum):
    PLAIN = "%s"
    BOLD = "**%s**"
    ITALIC = "_%s_"
    CODE = "`%s`"
    LINK = "[%s](%s)"
    IMAGE = "![%s](%s)"

class TextNode:
    def __init__(self, text:str, text_type:TextType, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, other:"TextNode"):
        check_text = self.text == other.text
        check_type = self.text_type == other.text_type
        check_url = self.url == other.url
        return check_text and check_type and check_url
    
    def __repr__(self):
        strformat = f"TextNode({self.text}, {self.text_type.name}, {self.url})"
        return strformat