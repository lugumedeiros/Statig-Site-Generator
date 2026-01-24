from textnode import TextNode, TextType
from markdown_blocks import generate_page
from pathlib import Path
import os
import sys

import os
from pathlib import Path
import shutil

PUBLIC_PATH = Path("docs")
STATIC_PATH = Path("static")

def clean_public_dir():
    PUBLIC_PATH.mkdir(parents=True, exist_ok=True)
    if PUBLIC_PATH.exists() and PUBLIC_PATH.is_dir():
        for item in PUBLIC_PATH.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                os.remove(item)
            print(f"Removed: {item}")
    else:
        raise Exception("Public dir not found")

def copy_to_public():
    if len(sys.argv) > 1:
        content = Path(sys.argv[1])
    else:
        content = STATIC_PATH

    if content.exists() and content.is_dir():
        clean_public_dir()
        shutil.copytree(STATIC_PATH, PUBLIC_PATH, dirs_exist_ok=True)

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
    if len(sys.argv) > 1:
        content = Path(sys.argv[1])
        print("Using arg path...", sys.argv)
    else:
        content = Path("content")

    copy_to_public()
    all_index_path = get_indexmd(content)
    for index in all_index_path:
        generate_page_from_path(content, index, PUBLIC_PATH)

if __name__ ==  "__main__":
    main()
