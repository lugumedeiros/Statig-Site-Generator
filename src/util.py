import re

def extract_markdown_images(text:str) -> dict[str, str]:
    urls = re.findall(r"!\[[^\]]*\]\((.*?)\)", text)
    alts = re.findall(r"!\[(.*?)\]",  text)
    if len(urls) != len(alts):
        raise Exception("invalid markdown or broken logic")
    return [(alts[i], urls[i]) for i in range(len(urls))]

def extract_markdown_links(text:str) -> dict[str, str]:
    urls = re.findall(r"(?<!!)\[[^\]]*\]\((.*?)\)", text)
    alts = re.findall(r"(?<!!)\[(.*?)\]",  text)
    if len(urls) != len(alts):
        raise Exception("invalid markdown or broken logic")
    return [(alts[i], urls[i]) for i in range(len(urls))]


if __name__ == "__main__":
    text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and [obi wan](https://mytube.com/fJRm4Vk) link"
    print(extract_markdown_images(text))
    # [("rick roll", "https://i.imgur.com/aKaOqIh.gif")] 
    print(extract_markdown_links(text))
    # [("obi wan", "https://mytube.com/fJRm4Vk")]
