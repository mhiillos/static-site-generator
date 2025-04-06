import unittest
from markdown_formatting import (
    BlockType,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
)


class testMarkDownFormatting(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("link", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches,
        )

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

        md2 = """
        Here is a very isolated paragraph




        H
         e
          l
           l
            o

        W
         o
          r
           l
            d
             !
        
        """

        blocks2 = markdown_to_blocks(md2)
        self.assertEqual(
            blocks2,
            ["Here is a very isolated paragraph", "H\ne\nl\nl\no", "W\no\nr\nl\nd\n!"],
        )

    def test_block_to_block_type(self):
        block = markdown_to_blocks("# This is a heading")[0]
        block2 = markdown_to_blocks("This # is NOT a heading")[0]
        block3 = markdown_to_blocks(
            """
            ```
            This text is in code block
            ```
        """
        )[0]
        block4 = markdown_to_blocks(
            """
        1. This
        2. is
        3. ordered
        """
        )[0]
        block5 = markdown_to_blocks(
            """
        1. This
        3. isn't
        """
        )[0]
        block6 = markdown_to_blocks(
            """
        - Unordered
        - list
        """
        )[0]

        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block3), BlockType.CODE)
        self.assertEqual(block_to_block_type(block4), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block5), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block6), BlockType.UNORDERED_LIST)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_list(self):
        md = """
        1. This is 
        2. a proper list
        3. With inline

        - Here is another list, but this one is
        - unordered.
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>This is</li><li>a proper list</li><li>With inline</li></ol><ul><li>Here is another list, but this one is</li><li>unordered.</li></ul></div>",
        )

    def test_heading(self):
        md = """
        # This is first heading

        ## This is second heading

        ##### This is even more heading
        """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is first heading</h1><h2>This is second heading</h2><h5>This is even more heading</h5></div>",
        )


if __name__ == "__main__":
    unittest.main()
