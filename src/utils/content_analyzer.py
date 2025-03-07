#!/usr/bin/env python3
"""
Content analyzer for AI4FairEdu
Identifies important elements in learning materials for highlighting
"""

from typing import Dict, List, Any, Optional
import re
from langchain_core.prompts import ChatPromptTemplate
from src.config import SystemConfig
from src.utils.llm_utils import get_llm

class ContentAnalyzer:
    """
    Class for analyzing learning content to identify important elements
    """
    
    def __init__(self, config: Optional[SystemConfig] = None):
        """
        Initialize the content analyzer
        
        Args:
            config: System configuration
        """
        self.config = config or SystemConfig()
        self.llm = get_llm(self.config)
    
    def identify_elements_to_highlight(self, content: str, difficulty_type: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Identify elements in the content that should be highlighted
        
        Args:
            content: The learning content to analyze
            difficulty_type: The user's learning difficulty type (ADHD, Dyslexia, Combined)
        
        Returns:
            Dictionary mapping highlight types to lists of elements to highlight
        """
        # Use LLM to identify important elements
        elements = self._llm_identify_elements(content, difficulty_type)
        
        # Fallback to rule-based identification if LLM fails
        if not elements or sum(len(items) for items in elements.values()) == 0:
            elements = self._rule_based_identify_elements(content)
        
        return elements
    
    def _llm_identify_elements(self, content: str, difficulty_type: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Use LLM to identify important elements in the content
        
        Args:
            content: The learning content to analyze
            difficulty_type: The user's learning difficulty type
        
        Returns:
            Dictionary mapping highlight types to lists of elements to highlight
        """
        # Create prompt based on difficulty type
        if difficulty_type == "ADHD":
            system_prompt = """You are an expert educational content analyzer specializing in supporting students with ADHD.
Your task is to identify elements in learning materials that should be highlighted to help maintain focus and enhance comprehension.

For students with ADHD, highlighting should:
1. Emphasize key concepts and main ideas to help maintain focus
2. Highlight action items and important instructions
3. Mark transitions between topics to help with organization
4. Identify concrete examples that illustrate abstract concepts

Analyze the provided learning content and identify:
1. PRIMARY elements: The most important concepts, terms, or ideas (5-7 items)
2. SECONDARY elements: Supporting details, examples, or explanations (3-5 items)
3. KEY_CONCEPTS: Fundamental concepts that are central to understanding the material (2-3 items)
4. DEFINITIONS: Terms that would benefit from definition tooltips (2-4 items)

Format your response as a JSON object with these categories as keys, each containing an array of objects with "text" and "metadata" fields.
The "metadata" field should include "importance" (high/medium/low) for primary/secondary elements, and "definition" for definition elements.
"""
        elif difficulty_type == "Dyslexia":
            system_prompt = """You are an expert educational content analyzer specializing in supporting students with Dyslexia.
Your task is to identify elements in learning materials that should be highlighted to improve readability and comprehension.

For students with Dyslexia, highlighting should:
1. Focus on difficult vocabulary or technical terms that may be challenging to decode
2. Highlight key concepts to aid in overall comprehension
3. Mark sentence structures that summarize main ideas
4. Identify terms that would benefit from definitions or simplifications

Analyze the provided learning content and identify:
1. PRIMARY elements: Essential vocabulary or terms that may be difficult to decode (3-5 items)
2. SECONDARY elements: Important phrases or sentence fragments that contain main ideas (2-4 items)
3. KEY_CONCEPTS: Fundamental concepts that are central to understanding the material (2-3 items)
4. DEFINITIONS: Terms that would benefit from definition tooltips or simplification (3-6 items)

Format your response as a JSON object with these categories as keys, each containing an array of objects with "text" and "metadata" fields.
The "metadata" field should include "importance" (high/medium/low) for primary/secondary elements, and "definition" for definition elements.
"""
        else:  # Combined or default
            system_prompt = """You are an expert educational content analyzer specializing in supporting students with both ADHD and Dyslexia.
Your task is to identify elements in learning materials that should be highlighted to improve focus, readability, and comprehension.

For students with both ADHD and Dyslexia, highlighting should:
1. Emphasize key concepts and main ideas to help maintain focus
2. Focus on difficult vocabulary or technical terms that may be challenging to decode
3. Mark transitions between topics to help with organization
4. Identify terms that would benefit from definitions or simplifications

Analyze the provided learning content and identify:
1. PRIMARY elements: Essential vocabulary, key concepts, or main ideas (4-6 items)
2. SECONDARY elements: Supporting details or important phrases (3-5 items)
3. KEY_CONCEPTS: Fundamental concepts that are central to understanding the material (2-3 items)
4. DEFINITIONS: Terms that would benefit from definition tooltips or simplification (3-6 items)

Format your response as a JSON object with these categories as keys, each containing an array of objects with "text" and "metadata" fields.
The "metadata" field should include "importance" (high/medium/low) for primary/secondary elements, and "definition" for definition elements.
"""
        
        # Create the prompt template
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "Please analyze the following learning content and identify elements to highlight:\n\n{content}")
        ])
        
        try:
            # Invoke the LLM
            response = self.llm.invoke(prompt.format(content=content))
            
            # Extract the JSON response
            import json
            import re
            
            # Try to extract JSON from the response
            json_match = re.search(r'```json\n(.*?)\n```', response.content, re.DOTALL)
            if json_match:
                json_str = json_match.group(1)
            else:
                json_str = response.content
            
            # Clean up the JSON string
            json_str = re.sub(r'```.*?```', '', json_str, flags=re.DOTALL)
            
            # Parse the JSON
            elements = json.loads(json_str)
            
            # Ensure all required keys exist
            for key in ["primary", "secondary", "key_concepts", "definitions"]:
                if key not in elements:
                    elements[key] = []
            
            return elements
        
        except Exception as e:
            print(f"Error using LLM to identify elements: {str(e)}")
            return {
                "primary": [],
                "secondary": [],
                "key_concepts": [],
                "definitions": []
            }
    
    def _rule_based_identify_elements(self, content: str) -> Dict[str, List[Dict[str, Any]]]:
        """
        Use rule-based approach to identify important elements in the content
        
        Args:
            content: The learning content to analyze
        
        Returns:
            Dictionary mapping highlight types to lists of elements to highlight
        """
        # Initialize result structure
        elements = {
            "primary": [],
            "secondary": [],
            "key_concepts": [],
            "definitions": []
        }
        
        # Split content into sentences
        sentences = re.split(r'(?<=[.!?])\s+', content)
        
        # Identify potential key concepts (capitalized terms, terms in quotes)
        key_concept_pattern = r'\b[A-Z][a-zA-Z]+(?:\s+[A-Z][a-zA-Z]+)*\b'
        quoted_pattern = r'"([^"]+)"'
        
        key_concepts = set()
        for sentence in sentences:
            # Find capitalized terms
            for match in re.finditer(key_concept_pattern, sentence):
                if len(match.group(0).split()) <= 3:  # Limit to 3 words
                    key_concepts.add(match.group(0))
            
            # Find quoted terms
            for match in re.finditer(quoted_pattern, sentence):
                if len(match.group(1).split()) <= 3:  # Limit to 3 words
                    key_concepts.add(match.group(1))
        
        # Add key concepts to the appropriate category
        for concept in list(key_concepts)[:3]:  # Limit to 3 key concepts
            elements["key_concepts"].append({
                "text": concept,
                "metadata": {"importance": "high"}
            })
        
        # Identify potential primary elements (first sentence, sentences with key phrases)
        primary_indicators = ["important", "key", "essential", "fundamental", "critical", "significant"]
        
        if sentences:
            # First sentence often contains main idea
            first_sentence = sentences[0]
            elements["primary"].append({
                "text": first_sentence.strip(),
                "metadata": {"importance": "high"}
            })
            
            # Look for sentences with indicator words
            for sentence in sentences[1:]:
                for indicator in primary_indicators:
                    if indicator in sentence.lower():
                        elements["primary"].append({
                            "text": sentence.strip(),
                            "metadata": {"importance": "high"}
                        })
                        break
        
        # Limit primary elements
        elements["primary"] = elements["primary"][:5]
        
        # Identify potential definitions (sentences with "is", "refers to", "defined as")
        definition_patterns = [
            r'([A-Za-z\s]+)\s+is\s+([^.!?]+)',
            r'([A-Za-z\s]+)\s+refers\s+to\s+([^.!?]+)',
            r'([A-Za-z\s]+)\s+is\s+defined\s+as\s+([^.!?]+)'
        ]
        
        for sentence in sentences:
            for pattern in definition_patterns:
                matches = re.finditer(pattern, sentence)
                for match in matches:
                    term = match.group(1).strip()
                    definition = match.group(2).strip()
                    if len(term.split()) <= 3:  # Limit to 3 words
                        elements["definitions"].append({
                            "text": term,
                            "metadata": {"definition": definition}
                        })
        
        # Limit definitions
        elements["definitions"] = elements["definitions"][:4]
        
        # Add some secondary elements (sentences with examples, explanations)
        secondary_indicators = ["for example", "such as", "e.g.", "i.e.", "in other words", "specifically"]
        
        for sentence in sentences:
            for indicator in secondary_indicators:
                if indicator in sentence.lower():
                    elements["secondary"].append({
                        "text": sentence.strip(),
                        "metadata": {"importance": "medium"}
                    })
                    break
        
        # Limit secondary elements
        elements["secondary"] = elements["secondary"][:3]
        
        return elements


# Example usage with few-shot learning samples
FEW_SHOT_SAMPLES = [
    {
        "content": """
Neural networks are a set of algorithms, modeled loosely after the human brain, that are designed to recognize patterns. They interpret sensory data through a kind of machine perception, labeling or clustering raw input. The patterns they recognize are numerical, contained in vectors, into which all real-world data, be it images, sound, text or time series, must be translated.
        """,
        "difficulty_type": "ADHD",
        "elements": {
            "primary": [
                {"text": "Neural networks", "metadata": {"importance": "high"}},
                {"text": "recognize patterns", "metadata": {"importance": "high"}},
                {"text": "interpret sensory data", "metadata": {"importance": "medium"}}
            ],
            "secondary": [
                {"text": "modeled loosely after the human brain", "metadata": {"importance": "medium"}},
                {"text": "numerical, contained in vectors", "metadata": {"importance": "medium"}}
            ],
            "key_concepts": [
                {"text": "Neural networks", "metadata": {"importance": "high"}},
                {"text": "patterns", "metadata": {"importance": "high"}}
            ],
            "definitions": [
                {"text": "Neural networks", "metadata": {"definition": "A set of algorithms designed to recognize patterns"}}
            ]
        }
    },
    {
        "content": """
The building block of a neural network is the neuron, a mathematical function that takes several inputs and produces a single output. When we have multiple neurons arranged in layers, we call it a neural network. The first layer receives the raw input, and the final layer produces the output.
        """,
        "difficulty_type": "Dyslexia",
        "elements": {
            "primary": [
                {"text": "neuron", "metadata": {"importance": "high"}},
                {"text": "layers", "metadata": {"importance": "high"}}
            ],
            "secondary": [
                {"text": "takes several inputs and produces a single output", "metadata": {"importance": "medium"}}
            ],
            "key_concepts": [
                {"text": "neuron", "metadata": {"importance": "high"}},
                {"text": "neural network", "metadata": {"importance": "high"}}
            ],
            "definitions": [
                {"text": "neuron", "metadata": {"definition": "A mathematical function that takes several inputs and produces a single output"}},
                {"text": "neural network", "metadata": {"definition": "Multiple neurons arranged in layers"}}
            ]
        }
    },
    {
        "content": """
Training a neural network requires a large amount of labeled data and computational resources. However, once trained, the network can make predictions or classifications with new data very quickly. This makes neural networks suitable for real-time applications.
        """,
        "difficulty_type": "Combined",
        "elements": {
            "primary": [
                {"text": "Training", "metadata": {"importance": "high"}},
                {"text": "make predictions or classifications", "metadata": {"importance": "high"}}
            ],
            "secondary": [
                {"text": "suitable for real-time applications", "metadata": {"importance": "medium"}}
            ],
            "key_concepts": [
                {"text": "Training", "metadata": {"importance": "high"}}
            ],
            "definitions": [
                {"text": "labeled data", "metadata": {"definition": "Data with known correct outputs"}},
                {"text": "computational resources", "metadata": {"definition": "Computing power and memory needed for processing"}}
            ]
        }
    }
]


def get_elements_to_highlight(content: str, difficulty_type: str, config: Optional[SystemConfig] = None) -> Dict[str, List[Dict[str, Any]]]:
    """
    Identify elements in the content that should be highlighted
    
    Args:
        content: The learning content to analyze
        difficulty_type: The user's learning difficulty type
        config: System configuration
    
    Returns:
        Dictionary mapping highlight types to lists of elements to highlight
    """
    analyzer = ContentAnalyzer(config)
    return analyzer.identify_elements_to_highlight(content, difficulty_type)


if __name__ == "__main__":
    # Example usage
    for i, sample in enumerate(FEW_SHOT_SAMPLES, 1):
        print(f"Sample {i} ({sample['difficulty_type']}):")
        print(f"Content: {sample['content'].strip()}")
        
        # Create analyzer
        analyzer = ContentAnalyzer()
        
        # Identify elements
        elements = analyzer.identify_elements_to_highlight(sample['content'], sample['difficulty_type'])
        
        # Print results
        print("\nIdentified elements:")
        for category, items in elements.items():
            print(f"- {category.upper()} ({len(items)} items):")
            for item in items:
                if "definition" in item.get("metadata", {}):
                    print(f"  • {item['text']} - Definition: {item['metadata']['definition']}")
                else:
                    print(f"  • {item['text']} - Importance: {item.get('metadata', {}).get('importance', 'N/A')}")
        
        print("-" * 80) 