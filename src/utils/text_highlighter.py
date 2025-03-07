#!/usr/bin/env python3
"""
Text highlighting utility for AI4FairEdu
Provides functions to highlight text in different ways based on user preferences
"""

from typing import Dict, List, Any, Optional, Tuple
import re
import html

class TextHighlighter:
    """
    Class for highlighting text in different ways based on user preferences
    """
    
    # Highlighting styles with HTML/CSS implementations
    HIGHLIGHT_STYLES = {
        "background": {
            "yellow": '<mark class="highlight-yellow">{}</mark>',
            "green": '<mark class="highlight-green">{}</mark>',
            "blue": '<mark class="highlight-blue">{}</mark>',
            "pink": '<mark class="highlight-pink">{}</mark>',
        },
        "text": {
            "bold": '<strong class="highlight-bold">{}</strong>',
            "italic": '<em class="highlight-italic">{}</em>',
            "underline": '<span class="highlight-underline">{}</span>',
            "color": {
                "red": '<span class="highlight-text-red">{}</span>',
                "blue": '<span class="highlight-text-blue">{}</span>',
                "green": '<span class="highlight-text-green">{}</span>',
            }
        },
        "special": {
            "definition": '<span class="highlight-definition" data-tooltip="{}">{}</span>',
            "key_concept": '<span class="highlight-key-concept">{}</span>',
            "example": '<div class="highlight-example">{}</div>',
        }
    }
    
    # CSS styles for the highlighting
    CSS_STYLES = """
    /* Background highlighting styles */
    .highlight-yellow { background-color: #ffffcc; }
    .highlight-green { background-color: #e6ffe6; }
    .highlight-blue { background-color: #e6f2ff; }
    .highlight-pink { background-color: #ffe6f2; }
    
    /* Text highlighting styles */
    .highlight-bold { font-weight: bold; }
    .highlight-italic { font-style: italic; }
    .highlight-underline { text-decoration: underline; }
    .highlight-text-red { color: #cc0000; }
    .highlight-text-blue { color: #0066cc; }
    .highlight-text-green { color: #006600; }
    
    /* Special highlighting styles */
    .highlight-definition {
        border-bottom: 1px dotted #666;
        position: relative;
        cursor: help;
    }
    .highlight-definition:hover::after {
        content: attr(data-tooltip);
        position: absolute;
        bottom: 100%;
        left: 0;
        background-color: #333;
        color: white;
        padding: 5px 10px;
        border-radius: 4px;
        white-space: nowrap;
        z-index: 1;
    }
    .highlight-key-concept {
        font-weight: bold;
        color: #0066cc;
        border-bottom: 1px solid #0066cc;
    }
    .highlight-example {
        background-color: #f9f9f9;
        border-left: 3px solid #0066cc;
        padding: 10px;
        margin: 10px 0;
    }
    """
    
    def __init__(self, user_preferences: Optional[Dict[str, Any]] = None):
        """
        Initialize the text highlighter with user preferences
        
        Args:
            user_preferences: Dictionary containing user highlighting preferences
        """
        self.user_preferences = user_preferences or {}
        
        # Default highlighting preferences if not specified
        if not self.user_preferences.get("highlight_style"):
            self.user_preferences["highlight_style"] = {
                "primary": {"type": "background", "style": "yellow"},
                "secondary": {"type": "text", "style": "bold"},
                "key_concepts": {"type": "special", "style": "key_concept"},
                "definitions": {"type": "special", "style": "definition"}
            }
    
    def get_css(self) -> str:
        """
        Get the CSS styles for the highlighting
        
        Returns:
            CSS styles as a string
        """
        return self.CSS_STYLES
    
    def highlight_text(self, text: str, highlight_type: str, elements: List[Dict[str, Any]]) -> str:
        """
        Highlight elements in the text
        
        Args:
            text: The text to highlight
            highlight_type: The type of highlighting to apply (primary, secondary, key_concepts, definitions)
            elements: List of elements to highlight, each with 'text' and optional 'metadata'
        
        Returns:
            Text with highlighted elements
        """
        # Make a copy of the text to avoid modifying the original
        highlighted_text = text
        
        # Get the highlighting style from user preferences
        highlight_pref = self.user_preferences.get("highlight_style", {}).get(highlight_type)
        if not highlight_pref:
            # Default to yellow background highlighting if preference not found
            highlight_pref = {"type": "background", "style": "yellow"}
        
        # Sort elements by length (descending) to avoid highlighting issues
        sorted_elements = sorted(elements, key=lambda x: len(x.get("text", "")), reverse=True)
        
        for element in sorted_elements:
            element_text = element.get("text", "")
            if not element_text:
                continue
            
            # Escape HTML in the element text for safe highlighting
            escaped_text = html.escape(element_text)
            
            # Get the highlighting template
            if highlight_pref["type"] == "special" and highlight_pref["style"] == "definition":
                # Special case for definitions which need a tooltip
                definition = element.get("metadata", {}).get("definition", "")
                escaped_definition = html.escape(definition)
                highlighted_element = self.HIGHLIGHT_STYLES["special"]["definition"].format(
                    escaped_definition, escaped_text
                )
            elif highlight_pref["type"] == "text" and highlight_pref["style"] in self.HIGHLIGHT_STYLES["text"].get("color", {}):
                # Special case for text color
                color = highlight_pref["style"]
                highlighted_element = self.HIGHLIGHT_STYLES["text"]["color"][color].format(escaped_text)
            else:
                # Standard highlighting
                style_type = highlight_pref["type"]
                style = highlight_pref["style"]
                if style_type in self.HIGHLIGHT_STYLES and style in self.HIGHLIGHT_STYLES[style_type]:
                    highlighted_element = self.HIGHLIGHT_STYLES[style_type][style].format(escaped_text)
                else:
                    # Fallback to yellow background highlighting
                    highlighted_element = self.HIGHLIGHT_STYLES["background"]["yellow"].format(escaped_text)
            
            # Replace the text with the highlighted version
            # Use regex with word boundaries to avoid partial matches
            pattern = re.compile(r'\b' + re.escape(element_text) + r'\b')
            highlighted_text = pattern.sub(highlighted_element, highlighted_text)
        
        return highlighted_text

    @staticmethod
    def extract_highlight_preferences(questionnaire_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract highlighting preferences from questionnaire data
        
        Args:
            questionnaire_data: User questionnaire data
        
        Returns:
            Dictionary of highlighting preferences
        """
        preferences = {}
        
        # Check if highlighting is mentioned in comprehension aids
        comprehension_aids = questionnaire_data.get("reading_patterns", {}).get("comprehension_aids", [])
        if "highlighting" in comprehension_aids:
            # User has indicated highlighting as a comprehension aid
            preferences["use_highlighting"] = True
            
            # Check for specific highlighting preferences
            learning_preferences = questionnaire_data.get("learning_preferences", {})
            modality_preference = learning_preferences.get("modality_preference", {})
            
            # Determine primary highlighting style based on learning modality
            if modality_preference.get("visual", 0) > 0.6:
                # Visual learners prefer color highlighting
                preferences["highlight_style"] = {
                    "primary": {"type": "background", "style": "yellow"},
                    "secondary": {"type": "background", "style": "blue"},
                    "key_concepts": {"type": "special", "style": "key_concept"},
                    "definitions": {"type": "special", "style": "definition"}
                }
            elif modality_preference.get("kinesthetic", 0) > 0.6:
                # Kinesthetic learners prefer bold and underline
                preferences["highlight_style"] = {
                    "primary": {"type": "text", "style": "bold"},
                    "secondary": {"type": "text", "style": "underline"},
                    "key_concepts": {"type": "special", "style": "key_concept"},
                    "definitions": {"type": "special", "style": "definition"}
                }
            else:
                # Default highlighting style
                preferences["highlight_style"] = {
                    "primary": {"type": "background", "style": "yellow"},
                    "secondary": {"type": "text", "style": "bold"},
                    "key_concepts": {"type": "special", "style": "key_concept"},
                    "definitions": {"type": "special", "style": "definition"}
                }
        else:
            # User has not indicated highlighting as a comprehension aid
            preferences["use_highlighting"] = False
        
        return preferences


# Example usage with few-shot learning samples
FEW_SHOT_SAMPLES = [
    {
        "description": "Visual learner with ADHD who benefits from color-coded highlighting",
        "questionnaire": {
            "reading_patterns": {
                "comprehension_aids": ["highlighting", "summarization", "visual aids"]
            },
            "learning_preferences": {
                "modality_preference": {"visual": 0.8, "auditory": 0.4, "kinesthetic": 0.3}
            }
        },
        "highlight_preferences": {
            "use_highlighting": True,
            "highlight_style": {
                "primary": {"type": "background", "style": "yellow"},
                "secondary": {"type": "background", "style": "green"},
                "key_concepts": {"type": "special", "style": "key_concept"},
                "definitions": {"type": "special", "style": "definition"}
            }
        },
        "sample_text": "Neural networks are a set of algorithms, modeled loosely after the human brain, that are designed to recognize patterns.",
        "elements_to_highlight": [
            {"text": "Neural networks", "metadata": {"importance": "high"}},
            {"text": "human brain", "metadata": {"importance": "medium"}},
            {"text": "recognize patterns", "metadata": {"importance": "high"}}
        ]
    },
    {
        "description": "Dyslexic learner who benefits from minimal, focused highlighting",
        "questionnaire": {
            "reading_patterns": {
                "comprehension_aids": ["highlighting", "text-to-speech", "simplified vocabulary"]
            },
            "learning_preferences": {
                "modality_preference": {"visual": 0.5, "auditory": 0.7, "kinesthetic": 0.4}
            }
        },
        "highlight_preferences": {
            "use_highlighting": True,
            "highlight_style": {
                "primary": {"type": "text", "style": "bold"},
                "secondary": {"type": "text", "style": "color", "color": "blue"},
                "key_concepts": {"type": "special", "style": "key_concept"},
                "definitions": {"type": "special", "style": "definition"}
            }
        },
        "sample_text": "The building block of a neural network is the neuron, a mathematical function that takes several inputs and produces a single output.",
        "elements_to_highlight": [
            {"text": "neuron", "metadata": {"definition": "Basic unit of a neural network"}},
            {"text": "inputs", "metadata": {"importance": "medium"}},
            {"text": "output", "metadata": {"importance": "medium"}}
        ]
    },
    {
        "description": "Kinesthetic learner who benefits from interactive highlighting",
        "questionnaire": {
            "reading_patterns": {
                "comprehension_aids": ["highlighting", "concept mapping", "hands-on examples"]
            },
            "learning_preferences": {
                "modality_preference": {"visual": 0.4, "auditory": 0.3, "kinesthetic": 0.8}
            }
        },
        "highlight_preferences": {
            "use_highlighting": True,
            "highlight_style": {
                "primary": {"type": "text", "style": "underline"},
                "secondary": {"type": "text", "style": "bold"},
                "key_concepts": {"type": "special", "style": "key_concept"},
                "definitions": {"type": "special", "style": "definition"}
            }
        },
        "sample_text": "Training a neural network requires a large amount of labeled data and computational resources.",
        "elements_to_highlight": [
            {"text": "Training", "metadata": {"importance": "high"}},
            {"text": "labeled data", "metadata": {"definition": "Data with known correct outputs"}},
            {"text": "computational resources", "metadata": {"importance": "medium"}}
        ]
    }
]


def get_highlighter_for_user(questionnaire_data: Dict[str, Any]) -> TextHighlighter:
    """
    Get a text highlighter configured for a specific user based on questionnaire data
    
    Args:
        questionnaire_data: User questionnaire data
    
    Returns:
        Configured TextHighlighter instance
    """
    # Extract highlighting preferences from questionnaire data
    preferences = TextHighlighter.extract_highlight_preferences(questionnaire_data)
    
    # Create and return a highlighter with these preferences
    return TextHighlighter(preferences)


def apply_highlighting_to_content(content: str, highlighter: TextHighlighter, elements_to_highlight: Dict[str, List[Dict[str, Any]]]) -> str:
    """
    Apply highlighting to content based on elements to highlight
    
    Args:
        content: The content to highlight
        highlighter: TextHighlighter instance
        elements_to_highlight: Dictionary mapping highlight types to lists of elements to highlight
    
    Returns:
        Content with highlighting applied
    """
    highlighted_content = content
    
    # Apply each type of highlighting
    for highlight_type, elements in elements_to_highlight.items():
        highlighted_content = highlighter.highlight_text(highlighted_content, highlight_type, elements)
    
    return highlighted_content


if __name__ == "__main__":
    # Example usage
    for i, sample in enumerate(FEW_SHOT_SAMPLES, 1):
        print(f"Sample {i}: {sample['description']}")
        
        # Create highlighter with sample preferences
        highlighter = TextHighlighter(sample["highlight_preferences"])
        
        # Apply highlighting
        highlighted_text = highlighter.highlight_text(
            sample["sample_text"], 
            "primary", 
            sample["elements_to_highlight"]
        )
        
        print(f"Original: {sample['sample_text']}")
        print(f"Highlighted: {highlighted_text}")
        print("-" * 80) 