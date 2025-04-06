import unittest

from textnode import (
    TextNode,
    TextType,
    text_node_to_html_node,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a italic text node", TextType.ITALIC)
        node4 = TextNode("This is another text node", TextType.BOLD)
        node5 = TextNode("This is a URL node", TextType.LINK, "https://localhost:8080")
        node6 = TextNode("This is a URL node", TextType.LINK, "https://localhost:8080")
        node7 = TextNode("This is a text node", TextType.BOLD, "https://localhost:8080")
        self.assertEqual(node, node2)
        self.assertEqual(node5, node6)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node, node7)

    def test_node_to_html(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        node2 = TextNode("This is a bold node", TextType.BOLD)
        html_node2 = text_node_to_html_node(node2)
        self.assertEqual(html_node2.tag, "b")
        self.assertEqual(html_node2.value, "This is a bold node")

        node3 = TextNode("This is an italic node", TextType.ITALIC)
        html_node3 = text_node_to_html_node(node3)
        self.assertEqual(html_node3.tag, "i")
        self.assertEqual(html_node3.value, "This is an italic node")

        node4 = TextNode("This is a code node", TextType.CODE)
        html_node4 = text_node_to_html_node(node4)
        self.assertEqual(html_node4.tag, "code")
        self.assertEqual(html_node4.value, "This is a code node")

        node5 = TextNode("This is a link node", TextType.LINK, "https://localhost:8080")
        html_node5 = text_node_to_html_node(node5)
        self.assertEqual(html_node5.tag, "a")
        self.assertEqual(html_node5.props, {"href": "https://localhost:8080"})

        node6 = TextNode("This is an image node", TextType.IMAGE, "/path/to/image")
        html_node6 = text_node_to_html_node(node6)
        self.assertEqual(html_node6.tag, "img")
        self.assertEqual(
            html_node6.props, {"src": "/path/to/image", "alt": "This is an image node"}
        )
        self.assertEqual(html_node6.value, "")

    def test_split_delimited_nodes(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected_result)

        node2 = TextNode("This is text with a `code` two `block` word", TextType.TEXT)
        new_nodes2 = split_nodes_delimiter([node2], "`", TextType.CODE)
        expected_result2 = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" two ", TextType.TEXT),
            TextNode("block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
        self.assertEqual(new_nodes2, expected_result2)

        new_nodes3 = split_nodes_delimiter([node, node2], "`", TextType.CODE)
        expected_result3 = expected_result + expected_result2
        self.assertEqual(new_nodes3, expected_result3)

        node4 = TextNode("This is a faulty `code block", TextType.TEXT)
        with self.assertRaises(ValueError) as context:
            split_nodes_delimiter([node4], "`", TextType.CODE)
        self.assertTrue("Delimiter is not paired" in str(context.exception))

        node5 = TextNode(
            "This is a `code block` with different TextType", TextType.BOLD
        )
        new_node5 = split_nodes_delimiter([node5], "`", TextType.CODE)
        self.assertEqual([node5], new_node5)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a [LINK!](https://i.imgur.com/)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [
                TextNode(
                    "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and a ",
                    TextType.TEXT,
                ),
                TextNode("LINK!", TextType.LINK, "https://i.imgur.com/"),
            ],
            new_nodes,
        )

    def test_text_to_nodes(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(input)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image",
                    TextType.IMAGE,
                    "https://i.imgur.com/fJRm4Vk.jpeg",
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
