import re

from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"Unsupported TextType: {text_node.text_type}")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise Exception("Closing delimiter now found. Invalid markdown syntax.")

        split_nodes_for_current_node = []

        for i in range(len(parts)):
            if i % 2 == 0:
                split_nodes_for_current_node.append(TextNode(parts[i], TextType.TEXT))
            else:
                split_nodes_for_current_node.append(TextNode(parts[i], text_type))

        new_nodes.extend(split_nodes_for_current_node)

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text is None:
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        md = extract_markdown_links(node.text)
        parts = node.text.split(f"![{md[0][0]}]({md[0][1]})", 1)

        split_nodes_for_current_node = []
        split_nodes_for_current_node.append(TextNode(parts[0], TextType.TEXT))
        split_nodes_for_current_node.append(
            TextNode(md[0][0], TextType.IMAGE, md[0][1])
        )
        split_nodes_for_current_node.append(
            TextNode(parts[1].split(f"[{md[1][0]}]({md[1][1]})")[0], TextType.TEXT)
        )
        split_nodes_for_current_node.append(
            TextNode(md[1][0], TextType.IMAGE, md[1][1])
        )

        new_nodes.extend(split_nodes_for_current_node)

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text is None:
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        md = extract_markdown_links(node.text)
        parts = node.text.split(f"[{md[0][0]}]({md[0][1]})", 1)

        split_nodes_for_current_node = []
        split_nodes_for_current_node.append(TextNode(parts[0], TextType.TEXT))
        split_nodes_for_current_node.append(TextNode(md[0][0], TextType.LINK, md[0][1]))
        split_nodes_for_current_node.append(
            TextNode(parts[1].split(f"[{md[1][0]}]({md[1][1]})")[0], TextType.TEXT)
        )
        split_nodes_for_current_node.append(TextNode(md[1][0], TextType.LINK, md[1][1]))

        new_nodes.extend(split_nodes_for_current_node)

    return new_nodes


if __name__ == "__main__":
    node = TextNode(
        "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        TextType.TEXT,
    )
    new_nodes = split_nodes_link([node])
    print(new_nodes)
