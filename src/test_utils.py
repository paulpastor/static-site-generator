import unittest

from textnode import TextNode, TextType
from utils import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_node_to_html_node,
)


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_bold(self):
        node = TextNode("This is text with a *bold block* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold block", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_italic(self):
        node = TextNode("This is text with an _italic block_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic block", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_multiple_nodes(self):
        node1 = TextNode("This is text with a `code block` word", TextType.TEXT)
        node2 = TextNode("Another **bold** phrase", TextType.TEXT)
        node3 = TextNode("Just plain text.", TextType.TEXT)
        node4 = TextNode("Already bold", TextType.BOLD)  # This node should not be split

        old_nodes = [node1, node2, node3, node4]

        # First, split for code blocks
        intermediate_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)

        # Then, split for bold phrases on the intermediate nodes
        final_nodes = split_nodes_delimiter(intermediate_nodes, "**", TextType.BOLD)

        expected_nodes = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
            TextNode("Another ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" phrase", TextType.TEXT),
            TextNode("Just plain text.", TextType.TEXT),
            TextNode("Already bold", TextType.BOLD),
        ]

        self.assertListEqual(expected_nodes, final_nodes)


class TextNodeToLeafNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

    def test_italic(self):
        node = TextNode("This is italic", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is italic")

    def test_code(self):
        node = TextNode("print('Hello')", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print('Hello')")

    def test_link(self):
        node = TextNode("Example", TextType.LINK, "https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Example")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_image(self):
        node = TextNode("Alt text", TextType.IMAGE, "https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(
            html_node.props, {"src": "https://example.com/image.png", "alt": "Alt text"}
        )


class ExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)


class ExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_links(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)


class TestSplitNodesImage(unittest.TestCase):
    def test_no_images_returns_same_node(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(result, [node])

    def test_single_image_only(self):
        node = TextNode("![alt](http://img.com/a.png)", TextType.TEXT)
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [TextNode("alt", TextType.IMAGE, "http://img.com/a.png")],
        )

    def test_image_with_surrounding_text(self):
        node = TextNode(
            "Before ![alt](http://img.com/a.png) after",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [
                TextNode("Before ", TextType.TEXT),
                TextNode("alt", TextType.IMAGE, "http://img.com/a.png"),
                TextNode(" after", TextType.TEXT),
            ],
        )

    def test_multiple_images(self):
        node = TextNode(
            "One ![first](http://img.com/1.png) middle ![second](http://img.com/2.png) end",
            TextType.TEXT,
        )
        result = split_nodes_image([node])
        self.assertEqual(
            result,
            [
                TextNode("One ", TextType.TEXT),
                TextNode("first", TextType.IMAGE, "http://img.com/1.png"),
                TextNode(" middle ", TextType.TEXT),
                TextNode("second", TextType.IMAGE, "http://img.com/2.png"),
                TextNode(" end", TextType.TEXT),
            ],
        )

    def test_non_text_nodes_unchanged(self):
        node = TextNode("alt", TextType.IMAGE, "http://img.com/a.png")
        result = split_nodes_image([node])
        self.assertEqual(result, [node])


class TestSplitNodesLink(unittest.TestCase):
    def test_no_links_returns_same_node(self):
        node = TextNode("Just plain text", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_single_link_only(self):
        node = TextNode("[boot](https://boot.dev)", TextType.TEXT)
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [TextNode("boot", TextType.LINK, "https://boot.dev")],
        )

    def test_link_with_surrounding_text(self):
        node = TextNode(
            "Go to [boot](https://boot.dev) now",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [
                TextNode("Go to ", TextType.TEXT),
                TextNode("boot", TextType.LINK, "https://boot.dev"),
                TextNode(" now", TextType.TEXT),
            ],
        )

    def test_multiple_links(self):
        node = TextNode(
            "Links: [one](https://one.com) and [two](https://two.com).",
            TextType.TEXT,
        )
        result = split_nodes_link([node])
        self.assertEqual(
            result,
            [
                TextNode("Links: ", TextType.TEXT),
                TextNode("one", TextType.LINK, "https://one.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("two", TextType.LINK, "https://two.com"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_non_text_nodes_unchanged(self):
        node = TextNode("boot", TextType.LINK, "https://boot.dev")
        result = split_nodes_link([node])
        self.assertEqual(result, [node])

    def test_mixed_nodes_list(self):
        nodes = [
            TextNode("Hello [boot](https://boot.dev)", TextType.TEXT),
            TextNode("world", TextType.BOLD),
        ]
        result = split_nodes_link(nodes)
        self.assertEqual(
            result,
            [
                TextNode("Hello ", TextType.TEXT),
                TextNode("boot", TextType.LINK, "https://boot.dev"),
                TextNode("world", TextType.BOLD),
            ],
        )


if __name__ == "__main__":
    unittest.main()
