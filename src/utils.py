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
        # leave non-text nodes as-is
        if node.text_type is not TextType.TEXT or node.text is None:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(text)

        # if no images, keep the node as-is
        if not matches:
            new_nodes.append(node)
            continue

        # walk through the matches one by one
        curr_text = text
        for image_text, image_url in matches:
            # split once on this specific markdown
            markdown = f"![{image_text}]({image_url})"
            before, sep, after = curr_text.partition(markdown)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(image_text, TextType.IMAGE, image_url))

            curr_text = after

        # any trailing text after the last image
        if curr_text:
            new_nodes.append(TextNode(curr_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        # leave non-text nodes as-is
        if node.text_type is not TextType.TEXT or node.text is None:
            new_nodes.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(text)

        # if no links, keep the node as-is
        if not matches:
            new_nodes.append(node)
            continue

        # walk through the matches one by one
        curr_text = text
        for link_text, link_url in matches:
            # split once on this specific markdown
            markdown = f"[{link_text}]({link_url})"
            before, sep, after = curr_text.partition(markdown)

            if before:
                new_nodes.append(TextNode(before, TextType.TEXT))

            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))

            curr_text = after

        # any trailing text after the last link
        if curr_text:
            new_nodes.append(TextNode(curr_text, TextType.TEXT))

    return new_nodes
