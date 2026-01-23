import unittest

from block_markdown import markdown_to_blocks
from blocktype import BlockType, block_to_block_type


class TestMarkDownToBlocks(unittest.TestCase):
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

    def test_single_paragraph_no_trailing_newline(self):
        md = "Just a simple paragraph with **bold** text."
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Just a simple paragraph with **bold** text."])

    def test_leading_and_trailing_blank_lines(self):
        md = """

    First paragraph

    Second paragraph

    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First paragraph",
                "Second paragraph",
            ],
        )

    def test_multiple_blank_lines_between_blocks(self):
        md = """First

        

    Second"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "First",
                "Second",
            ],
        )

    def test_multiline_list_block(self):
        md = """- item one
    - item two
    - item three"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "- item one\n- item two\n- item three",
            ],
        )

    def test_indented_lines_are_stripped(self):
        md = """Paragraph line one
        Paragraph line two
            Paragraph line three"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Paragraph line one\nParagraph line two\nParagraph line three",
            ],
        )


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks_basic(self):
        md = "Line 1\n\nLine 2\n\nLine 3"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["Line 1", "Line 2", "Line 3"])

    def test_paragraph_block(self):
        block = "This is just a normal paragraph.\nStill the same paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_levels(self):
        self.assertEqual(block_to_block_type("# Head"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Head"), BlockType.HEADING)
        # not a heading: no space
        self.assertEqual(block_to_block_type("######Head"), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nprint('hello')\nprint('world')\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote_block_valid(self):
        block = "> quote line 1\n> quote line 2"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_block_invalid(self):
        block = "> quote line 1\nnot quoted"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_valid(self):
        block = "- item 1\n- item 2\n- item 3"
        self.assertEqual(block_to_block_type(block), BlockType.ULIST)

    def test_unordered_list_invalid(self):
        block = "- item 1\nnot a list item"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_valid(self):
        block = "1. first\n2. second\n3. third"
        self.assertEqual(block_to_block_type(block), BlockType.OLIST)

    def test_ordered_list_invalid_start_not_one(self):
        block = "2. wrong start\n3. next"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_invalid_wrong_increment(self):
        block = "1. first\n3. skipped two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
