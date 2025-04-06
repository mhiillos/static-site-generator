import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_parent_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected_result = (
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )
        self.assertEqual(node.to_html(), expected_result)

        # Node with a nested parent, including some props
        node2 = ParentNode(
            "p",
            [
                ParentNode(
                    "p",
                    [LeafNode("b", "Bold text"), LeafNode("i", "Italic text")],
                ),
                LeafNode("b", "Bold text", {"href": "https://www.google.com"}),
            ],
            {"href": "https://localhost:8080"},
        )

        expected_result2 = '<p href="https://localhost:8080"><p><b>Bold text</b><i>Italic text</i></p><b href="https://www.google.com">Bold text</b></p>'
        self.assertEqual(node2.to_html(), expected_result2)

    def test_parent_node_no_tag(self):
        with self.assertRaises(ValueError) as context:
            ParentNode(None, [LeafNode("b", "text")]).to_html()
        self.assertTrue("ParentNode missing tag" in str(context.exception))

    def test_parent_node_no_children(self):
        with self.assertRaises(ValueError) as context:
            ParentNode("b", []).to_html()
        self.assertTrue(
            "ParentNode must have at least one child" in str(context.exception)
        )


if __name__ == "__main__":
    unittest.main()
