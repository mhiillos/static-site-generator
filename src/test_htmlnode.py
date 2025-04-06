import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(
            None, None, None, {"href": "https://www.google.com", "target": "_blank"}
        )
        expectedResult = 'href="https://www.google.com" target="_blank"'
        node2 = HTMLNode(None, None, None, {})
        self.assertEqual(node.props_to_html(), expectedResult)
        self.assertEqual(node2.props_to_html(), "")


if __name__ == "__main__":
    unittest.main()
