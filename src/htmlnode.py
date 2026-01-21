from enum import Enum
import textwrap

class HTMLTags(Enum):
    TAG = 0

class HTMLNode:
    def __init__(self, tag=None, value=None, children:list["HTMLNode"]=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        str_props = [f'{key}="{value}"' for key, value in self.props.items()]
        return " ".join(str_props)
    
    def __repr__(self):
        string = f"""-> TAG:
{self.tag}
-> VALUE:
{self.value}
-> CHILDREN:
{self.children}
-> PROPS:
{self.props_to_html()}
"""
        return string
    

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.props is not None:
            props = self.props_to_html()
            string = f"<{self.tag} {props}>{self.value}</{self.tag}>"
        else:
            string = f"<{self.tag}>{self.value}</{self.tag}>"
        return string
        
    def __repr__(self):
        string = f"""
            -> TAG:
            {self.tag}
            -> VALUE:
            {self.value}
            -> PROPS:
            {self.props_to_html()}
            """
        return textwrap.dedent(string).strip()
    
class ParentNode(HTMLNode):
    def __init__(self, tag:str, children:list[HTMLNode], props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        children_strings = "".join([node.to_html() for node in self.children])
        return f"<{self.tag}>{children_strings}</{self.tag}>"

if __name__ == "__main__":
    grandchild_node = LeafNode("b", "grandchild")
    child_node = ParentNode("span", [grandchild_node])
    parent_node = ParentNode("div", [child_node])
    print(parent_node.to_html())