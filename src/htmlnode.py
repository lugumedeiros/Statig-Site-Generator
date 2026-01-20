from enum import Enum

class HTMLTags(Enum):
    TAG = 0

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
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
    
if __name__ == "__main__":
    x = HTMLNode("a", "test", ["is"], {"run":"ning"})
    print(x)
    print(x.props_to_html(), 'sa')