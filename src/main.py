from textnode import TextNode, TextType
from markdown_blocks import generate_page
from pathlib import Path
import os

def get_indexmd(path_target:str|Path, found=None):
    if found is None:
        found = []

    target = Path(path_target)
    if target.is_file() and target.suffix == ".md":
        found.append(target)
    elif target.is_dir():
        for target_file in target.iterdir():    
            found += get_indexmd(target_file)
    return found

def generate_page_from_path(base:Path, path:Path, target:Path):
    relative = path.relative_to(base)
    target_with_relative = target / relative
    target_to_html = target_with_relative.with_suffix(".html")
    print(path, target_to_html)
    generate_page(path, "template.html", target_to_html)

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node)
    content = Path("content")
    all_index_path = get_indexmd(content)
    for index in all_index_path:
        generate_page_from_path(content, index, Path("public"))

if __name__ ==  "__main__":
    main()
