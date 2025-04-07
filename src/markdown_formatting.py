import re
from enum import Enum
from htmlnode import HTMLNode
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node, text_to_textnodes


# Markdown block types
class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


# This function uses a regexpr to find images in markdown text
def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)


# This function uses a regexpr to find links in markdown text
def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[(.*?)\]\((.*?)\)", text)


# This function takes a raw markdown string and returns the document in a list of blocks.
def markdown_to_blocks(markdown):
    return [
        "\n".join(line.strip() for line in p.split("\n") if line.strip())
        for p in markdown.strip("\n").split("\n\n")
        if p.strip()
    ]


# This function takes a block of markdown text as input and returns a BlockType enum.
def block_to_block_type(block):
    if re.search(r"^#+ ", block):
        return BlockType.HEADING
    elif (
        block.split("\n")[0].strip() == "```" and block.split("\n")[-1].strip() == "```"
    ):
        return BlockType.CODE
    elif all(re.match(r"^>($|\s)", line) for line in block.splitlines()):
        return BlockType.QUOTE
    elif all(re.match(r"^- ", line) for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(block):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def is_ordered_list(block):
    lines = block.splitlines()
    for i, line in enumerate(lines):
        if not re.match(f"^{i+1}\\. ", line):
            return False
    return True and len(lines) > 0


# This function converts raw markdown text to a HTMLNode object
def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)

    all_children = []
    for block in blocks:
        block_type = block_to_block_type(block)

        # Handle special case, code blocks
        if block_type == BlockType.CODE:
            raw_text_node = TextNode(
                ("\n".join(block.split("\n")[1:-1]) + "\n"), TextType.CODE
            )
            code_node = text_node_to_html_node(raw_text_node)
            block_parent = ParentNode("pre", [code_node])

        # Handle other block types
        else:
            # Get the parent and child tags
            html_tag = block_type_to_html_tag(block, block_type)
            block_rows = block.split("\n")

            block_parent = block_rows_to_parents(block_rows, html_tag[1], html_tag[0])
        all_children.append(block_parent)

    parent = ParentNode("div", all_children)
    return parent


# Returns parent tag and child tag if applicable
def block_type_to_html_tag(block, block_type):
    match block_type:
        case BlockType.PARAGRAPH:
            return ("p", None)
        case BlockType.HEADING:
            num = len(block.split(" ")[0])
            return (f"h{num}", None)
        case BlockType.QUOTE:
            return ("blockquote", None)
        case BlockType.UNORDERED_LIST:
            return ("ul", "li")
        case BlockType.ORDERED_LIST:
            return ("ol", "li")
        case _:
            raise ValueError(f"{block_type} not a valid type")


def block_rows_to_parents(block_rows, child_tag, parent_tag):
    block_children = []
    is_paragraph = True if parent_tag == "p" else False
    if is_paragraph:
        block_rows = [" ".join(block_rows)]
    if parent_tag == "blockquote":
        block_rows = ["> " + "".join(block_rows).replace(">", "").strip()]
    for row in block_rows:
        row_children = text_to_children(row, is_paragraph)

        # If there is no child tag, don't create a nested ParentNode
        if not child_tag:
            block_children.extend(row_children)

        else:
            block_children.append(ParentNode(child_tag, row_children))
    return ParentNode(parent_tag, block_children)


# This function parses a row of raw text, strips the characters at the beginning of string, and returns the text nodes parsed from the text
def text_to_children(text, is_paragraph):
    children = []
    if not is_paragraph:
        # Remove the identifier from the row
        text = " ".join(text.split(" ")[1:])
    text_nodes = text_to_textnodes(text)
    for node in text_nodes:
        children.append(text_node_to_html_node(node))
    return children


# Extracts the h1 header text
def extract_title(markdown):
    header_row = next(line for line in markdown.split("\n") if line).strip()
    if not header_row.split(" ")[0] == "#":
        raise Exception("markdown text does not start with a header")
    return " ".join(header_row.split(" ")[1:])
