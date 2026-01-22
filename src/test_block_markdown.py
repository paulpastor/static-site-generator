import unittest

from block_markdown import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
