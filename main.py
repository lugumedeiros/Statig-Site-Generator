import os
from pathlib import Path
import shutil

PUBLIC_PATH = Path("docs")
STATIC_PATH = Path("static")

def clean_public_dir():
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
    if STATIC_PATH.exists() and STATIC_PATH.is_dir():
        clean_public_dir()
        shutil.copytree(STATIC_PATH, PUBLIC_PATH, dirs_exist_ok=True)


def main():
    print("Hello from static-site-generator!")
    copy_to_public()


if __name__ == "__main__":
    main()
