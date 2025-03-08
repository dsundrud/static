from textnode import TextNode, TextType
import re
def process_text_with_delimiters(text, delimiter, text_type):
    result = []
    
    # Find first delimiter
    start_index = text.find(delimiter)
    if start_index == -1:
        # No delimiter found, return the whole text as a TEXT node
        return [TextNode(text, TextType.TEXT)] if text else []
    
    # Find matching closing delimiter
    end_index = text.find(delimiter, start_index + len(delimiter))
    if end_index == -1:
        # No matching closing delimiter found
        raise ValueError(f"Closing delimiter '{delimiter}' not found")
    
    # Text before the first delimiter
    if start_index > 0:
        result.append(TextNode(text[:start_index], TextType.TEXT))
    
    # Text between delimiters (without the delimiters themselves)
    delimited_text = text[start_index + len(delimiter):end_index]
    result.append(TextNode(delimited_text, text_type))
    
    # Process the remaining text after the second delimiter
    remaining_text = text[end_index + len(delimiter):]
    if remaining_text:
        # Recursively process the rest of the text
        result.extend(process_text_with_delimiters(remaining_text, delimiter, text_type))
    
    return result


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        
        # Use the process_text_with_delimiters function
        split_nodes = process_text_with_delimiters(old_node.text, delimiter, text_type)
        new_nodes.extend(split_nodes)
    
    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches


def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches