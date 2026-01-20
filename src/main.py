from textnode import *

def main():
    text = "This is some anchor text"
    text_type = TextType.LINK
    url = "https://www.boot.dev"
    text_node = TextNode(text, text_type, url )
    print(text_node)

if __name__ == "__main__":
    print("Test Start")
    main()