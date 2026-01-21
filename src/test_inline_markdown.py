import unittest

from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text_only(self):
        text = "Just some plain text."
        expected = [TextNode("Just some plain text.", TextType.TEXT)]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_bold_only(self):
        text = "This is **bold**."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_italic_only(self):
        text = "This is _italic_."
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_code_only(self):
        text = "Some `code` here."
        expected = [
            TextNode("Some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_image_only(self):
        text = "An image: ![alt](https://example.com/img.png)"
        expected = [
            TextNode("An image: ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_link_only(self):
        text = "A [link](https://example.com) here."
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" here.", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_mixed_all_features(self):
        text = (
            "This is **bold** and _italic_ and `code` and "
            "![alt](https://example.com/img.png) and a "
            "[link](https://example.com)."
        )
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "https://example.com/img.png"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_multiple_images_and_links(self):
        text = "Pic1 ![a](url1) middle [l1](u1) end ![b](url2) and [l2](u2)"
        expected = [
            TextNode("Pic1 ", TextType.TEXT),
            TextNode("a", TextType.IMAGE, "url1"),
            TextNode(" middle ", TextType.TEXT),
            TextNode("l1", TextType.LINK, "u1"),
            TextNode(" end ", TextType.TEXT),
            TextNode("b", TextType.IMAGE, "url2"),
            TextNode(" and ", TextType.TEXT),
            TextNode("l2", TextType.LINK, "u2"),
        ]
        self.assertEqual(text_to_textnodes(text), expected)

    def test_unclosed_bold_raises(self):
        text = "This is **not closed"
        with self.assertRaises(ValueError):
            text_to_textnodes(text)


if __name__ == "__main__":
    unittest.main()
