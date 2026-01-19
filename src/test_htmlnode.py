import unittest

from htmlnode import HTMLNode


class TextHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(tag="div", value="This is a div", props={"class": "container"})
        node2 = HTMLNode(tag="div", value="This is a div", props={"class": "container"})
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode(tag="div", value="This is a div", props={"class": "container"})
        node2 = HTMLNode(
            tag="span", value="This is a span", props={"class": "container"}
        )
        self.assertNotEqual(node, node2)

    def test_eq_diff_props(self):
        node = HTMLNode(tag="div", value="This is a div", props={"class": "container"})
        node2 = HTMLNode(tag="div", value="This is a div", props={"id": "main"})
        self.assertNotEqual(node, node2)

    def test_eq_no_props(self):
        node = HTMLNode(tag="div", value="This is a div")
        node2 = HTMLNode(tag="div", value="This is a div")
        self.assertEqual(node, node2)

    def test_props_to_html(self):
        node = HTMLNode(tag="div", value="This is a div", props={"class": "container"})
        self.assertEqual(node.props_to_html(), ' class="container"')

    def test_props_to_html_empty(self):
        node = HTMLNode(tag="div", value="This is a div", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_none(self):
        node = HTMLNode(tag="div", value="This is a div")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_multiple(self):
        node = HTMLNode(
            tag="a",
            value="link",
            props={"href": "https://www.google.com", "target": "_blank"},
        )
        html = node.props_to_html()
        # Order depends on dict insertion, so either assert exact or use `in` checks:
        self.assertIn(' href="https://www.google.com"', html)
        self.assertIn(' target="_blank"', html)


if __name__ == "__main__":
    unittest.main()
