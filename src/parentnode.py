from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("ParentNode missing tag")
        if not self.children:
            raise ValueError("ParentNode must have at least one child")

        props_html = HTMLNode.props_to_html(self)
        props_str = f" {props_html}" if props_html else ""
        res_str = f"<{self.tag}{props_str}>"
        # Add child(ren) to result HTML string
        for child in self.children:
            res_str += f"{child.to_html()}"
        res_str += f"</{self.tag}>"
        return res_str

    def __repr__(self):
        return f"ParentNode({self.tag}, {self.value}, {self.children}, {self.props})"
