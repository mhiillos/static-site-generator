class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag  # None: Render as raw text
        self.value = value  # None: has children
        self.children = children  # None: has value
        self.props = props  # None: no attributes

    # Will be overrided by child classes
    def to_html(self):
        raise NotImplementedError("not implemented")

    def props_to_html(self):
        if self.props:
            return " ".join([f'{k}="{v}"' for k, v in self.props.items()])
        return ""

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
