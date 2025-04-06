from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text_type == other.text_type
            and self.text == other.text
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("Not a valid text type")


# This function splits a list of TextNodes by a given delimiter and assigns the delimited text a new text type
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        # Check for properly paired delimiters
        if text.count(delimiter) % 2 != 0:
            raise ValueError("Delimiter is not paired")

        start_idx = 0
        result = []  # tuple (text, boolean),
        while start_idx < len(text):
            delim_begin = text.find(delimiter, start_idx)
            # Return the end of the string
            if delim_begin == -1:
                if start_idx < len(text):
                    result.append((text[start_idx:], False))
                break

            # Add text before delimiter
            if delim_begin > start_idx:
                result.append((text[start_idx:delim_begin], False))

            # Find closing delimiter
            delim_end = text.find(delimiter, delim_begin + len(delimiter))

            # Add delimited text
            result.append((text[(delim_begin + len(delimiter)) : delim_end], True))

            # Update start_idx
            start_idx = delim_end + len(delimiter)

        for result_tuple in result:
            new_type = text_type if result_tuple[1] else TextType.TEXT
            new_nodes.append(TextNode(result_tuple[0], new_type))

    return new_nodes


# This function parses through a list of nodes and splits text nodes with an image, assigning it the correct text type
def split_nodes_image(old_nodes):
    from markdown_formatting import extract_markdown_images

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        image_tuples = extract_markdown_images(text)

        if not image_tuples:
            new_nodes.append(node)
            continue

        # For each match, find the start index
        start_idx = 0
        result = []
        for i, image_tuple in enumerate(image_tuples):
            # Reconstruct the link string for finding the pattern
            reconstructed_string = f"![{image_tuple[0]}]({image_tuple[1]})"
            image_begin = text.find(reconstructed_string, start_idx)
            # Add text before image
            if image_begin > start_idx:
                result.append(((text[start_idx:image_begin], None), False))

            # Add the image string
            result.append(((image_tuple[0], image_tuple[1]), True))

            # Update start index to be after the image
            start_idx = image_begin + len(reconstructed_string)

            # If this was the last image string, append the rest
            if i == len(image_tuples) - 1:
                if start_idx < len(text):
                    result.append(
                        (
                            (text[(image_begin + len(reconstructed_string)) :], None),
                            False,
                        )
                    )

        # Create the new nodes
        for result_tuple in result:
            new_type = TextType.IMAGE if result_tuple[1] else TextType.TEXT
            new_nodes.append(TextNode(result_tuple[0][0], new_type, result_tuple[0][1]))

    return new_nodes


# This function parses through a list of nodes and splits text nodes with a link, assigning it the correct text type
def split_nodes_link(old_nodes):
    from markdown_formatting import extract_markdown_links

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        text = node.text
        link_tuples = extract_markdown_links(text)

        if not link_tuples:
            new_nodes.append(node)
            continue

        # For each match, find the start index
        start_idx = 0
        result = []
        for i, link_tuple in enumerate(link_tuples):
            # Reconstruct the link string for finding the pattern
            reconstructed_string = f"[{link_tuple[0]}]({link_tuple[1]})"
            link_begin = text.find(reconstructed_string, start_idx)
            # Add text before link
            if link_begin > start_idx:
                result.append(((text[start_idx:link_begin], None), False))

            # Add the link string
            result.append(((link_tuple[0], link_tuple[1]), True))

            # Update start index to be after the link
            start_idx = link_begin + len(reconstructed_string)

            # If this was the last link string, append the rest
            if i == len(link_tuples) - 1:
                if start_idx < len(text):
                    result.append(
                        (
                            (text[(link_begin + len(reconstructed_string)) :], None),
                            False,
                        )
                    )

        # Create the new nodes
        for result_tuple in result:
            new_type = TextType.LINK if result_tuple[1] else TextType.TEXT
            new_nodes.append(TextNode(result_tuple[0][0], new_type, result_tuple[0][1]))

    return new_nodes


# This function parses raw markdown text into TextNode objects
def text_to_textnodes(text):
    # Transform text into a single node
    nodes = [TextNode(text, TextType.TEXT)]
    # Handle delimiters
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    # Handle links and images
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_image(nodes)
    return nodes
