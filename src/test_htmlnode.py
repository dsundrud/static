import unittest
from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_empty(self):
        # Test with no props
        node = HTMLNode("div", "Hello", None, {})
        self.assertEqual(node.props_to_html(), "")
        
    def test_props_to_html_single_prop(self):
        # Test with a single prop
        node = HTMLNode("a", "Click me", None, {"href": "https://example.com"})
        self.assertEqual(node.props_to_html(), ' href="https://example.com"')
        
    def test_props_to_html_multiple_props(self):
        # Test with multiple props
        node = HTMLNode(
            "a", 
            "Click me", 
            None, 
            {"href": "https://example.com", "target": "_blank"}
        )
        # Note: order might vary, so you might need to adjust this test
        self.assertTrue(' href="https://example.com"' in node.props_to_html())
        self.assertTrue(' target="_blank"' in node.props_to_html())
        self.assertEqual(len(node.props_to_html().split()), 2)