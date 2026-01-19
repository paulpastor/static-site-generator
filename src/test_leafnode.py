import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_eq(self):
        node = LeafNode("p", "This is a paragraph", {"class": "text"})
        node2 = LeafNode("p", "This is a paragraph", {"class": "text"})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = LeafNode("p", "This is a paragraph", {"class": "text"})
        node2 = LeafNode("p", "This is a different paragraph", {"class": "text"})
        self.assertNotEqual(node, node2)

        def test_leaf_to_html_p(self):
            node = LeafNode("p", "Hello, world!")
            self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

        def test_leaf_to_html_with_props(self):
            node = LeafNode("a", "Click me", {"href": "https://example.com"})
            self.assertEqual(
                node.to_html(),
                '<a href="https://example.com">Click me</a>',
            )

        def test_leaf_to_html_no_tag(self):
            node = LeafNode(None, "Just text")
            self.assertEqual(node.to_html(), "Just text")

        def test_leaf_to_html_raises_on_empty_value(self):
            node = LeafNode("p", None)
            with self.assertRaises(ValueError):
                node.to_html()


if __name__ == "__main__":
    unittest.main()
