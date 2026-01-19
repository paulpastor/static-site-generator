import unittest

from htmlnode import LeafNode, ParentNode


class ParentNodeTestCase(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_props(self):
        child = LeafNode("span", "child")
        parent = ParentNode("div", [child], {"class": "box", "id": "main"})
        self.assertEqual(
            parent.to_html(),
            '<div class="box" id="main"><span>child</span></div>',
        )

    def test_to_html_multiple_children(self):
        children = [
            LeafNode("b", "bold"),
            LeafNode(None, " text "),
            LeafNode("i", "italic"),
        ]
        parent = ParentNode("p", children)
        self.assertEqual(
            parent.to_html(),
            "<p><b>bold</b> text <i>italic</i></p>",
        )

    def test_to_html_missing_tag_raises(self):
        parent = ParentNode("div", [LeafNode("span", "x")])
        parent.tag = None
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_children_none_raises(self):
        parent = ParentNode("div", [LeafNode("span", "x")])
        parent.children = None
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_children_empty_raises(self):
        parent = ParentNode("div", [])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_to_html_deep_nesting(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [LeafNode("span", "deep")],
                )
            ],
        )
        self.assertEqual(node.to_html(), "<div><p><span>deep</span></p></div>")


if __name__ == "__main__":
    unittest.main()
