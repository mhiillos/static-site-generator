from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("missing value")
        if not self.tag:
            return self.value
        props_html = HTMLNode.props_to_html(self)

        # Only add whitespace before props if props exist
        props_str = f" {props_html}" if props_html else ""
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.children}, {self.props})"
