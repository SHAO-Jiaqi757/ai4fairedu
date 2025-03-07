#!/usr/bin/env python3
"""
Demonstration script for the highlighting functionality with AI agents
"""

import os
import json
import argparse
from datetime import datetime
from typing import Dict, List, Any, Optional

from src.config import SystemConfig
from src.utils.llm_utils import get_llm
from src.utils.text_highlighter import TextHighlighter, get_highlighter_for_user
from src.utils.content_analyzer import get_elements_to_highlight, ContentAnalyzer
from src.adhd_support import micro_content_divider
from src.dyslexia_support import syntax_simplifier
from src.user_profile import analyze_user_profile

# Initialize configuration
config = SystemConfig()

def load_sample_questionnaire(sample_type: str = "adhd") -> Dict[str, Any]:
    """
    Load a sample questionnaire response with highlighting preferences
    
    Args:
        sample_type: Type of sample to load ("adhd", "dyslexia", or "combined")
    
    Returns:
        Dictionary containing sample questionnaire data
    """
    # Base questionnaire data
    base_data = {
        "personal_info": {
            "age": 19,
            "education_level": "undergraduate",
            "subject_interests": ["computer science", "mathematics", "psychology"]
        },
        "learning_preferences": {
            "modality_preference": {
                "visual": 0.7,
                "auditory": 0.4,
                "kinesthetic": 0.6
            },
            "feedback_preference": "immediate",
            "group_vs_individual": "individual",
            "technology_comfort": "very comfortable"
        }
    }
    
    # ADHD-specific data with highlighting preference
    if sample_type == "adhd":
        return {
            **base_data,
            "learning_difficulties": {
                "diagnosed_conditions": ["ADHD"],
                "self_reported_challenges": ["maintaining focus", "organizing thoughts", "time management"]
            },
            "attention_patterns": {
                "average_focus_duration_minutes": 15,
                "best_focus_time_of_day": ["morning", "late evening"],
                "distraction_triggers": ["notifications", "background noise", "complex text"],
                "hyperfocus_activities": ["programming", "gaming", "problem-solving"]
            },
            "reading_patterns": {
                "reading_speed": "average",
                "difficult_text_features": ["long paragraphs", "dense content", "monotonous presentation"],
                "preferred_text_format": {
                    "font": "Arial",
                    "size": "normal",
                    "spacing": "normal",
                    "background": "white"
                },
                "comprehension_aids": ["highlighting", "summarization", "visual aids"]
            },
            "previous_strategies": {
                "task_breakdown": {
                    "effectiveness": 4,
                    "notes": "Breaking tasks into smaller steps helps a lot"
                },
                "pomodoro_technique": {
                    "effectiveness": 5,
                    "notes": "Works very well for maintaining focus"
                },
                "concept_mapping": {
                    "effectiveness": 4,
                    "notes": "Visual organization of ideas is very helpful"
                }
            }
        }
    
    # Dyslexia-specific data with highlighting preference
    elif sample_type == "dyslexia":
        return {
            **base_data,
            "learning_difficulties": {
                "diagnosed_conditions": ["Dyslexia"],
                "self_reported_challenges": ["reading comprehension", "spelling", "processing text"]
            },
            "attention_patterns": {
                "average_focus_duration_minutes": 30,
                "best_focus_time_of_day": ["morning", "afternoon"],
                "distraction_triggers": ["complex vocabulary", "dense text", "small fonts"],
                "hyperfocus_activities": ["drawing", "hands-on projects", "discussions"]
            },
            "reading_patterns": {
                "reading_speed": "slower than average",
                "difficult_text_features": ["complex sentences", "technical jargon", "small fonts"],
                "preferred_text_format": {
                    "font": "OpenDyslexic",
                    "size": "larger",
                    "spacing": "increased",
                    "background": "light cream"
                },
                "comprehension_aids": ["highlighting", "text-to-speech", "simplified vocabulary", "visual aids"]
            },
            "previous_strategies": {
                "text_to_speech": {
                    "effectiveness": 5,
                    "notes": "Very helpful for understanding complex text"
                },
                "vocabulary_simplification": {
                    "effectiveness": 4,
                    "notes": "Makes technical content much more accessible"
                },
                "concept_mapping": {
                    "effectiveness": 3,
                    "notes": "Helpful for organizing ideas"
                }
            }
        }
    
    # Combined ADHD and Dyslexia data with highlighting preference
    elif sample_type == "combined":
        return {
            **base_data,
            "learning_difficulties": {
                "diagnosed_conditions": ["ADHD", "Dyslexia"],
                "self_reported_challenges": ["maintaining focus", "reading comprehension", "organizing thoughts", "processing text"]
            },
            "attention_patterns": {
                "average_focus_duration_minutes": 10,
                "best_focus_time_of_day": ["morning"],
                "distraction_triggers": ["notifications", "complex vocabulary", "dense text", "background noise"],
                "hyperfocus_activities": ["programming", "hands-on projects", "problem-solving"]
            },
            "reading_patterns": {
                "reading_speed": "much slower than average",
                "difficult_text_features": ["complex sentences", "long paragraphs", "technical jargon", "small fonts"],
                "preferred_text_format": {
                    "font": "OpenDyslexic",
                    "size": "larger",
                    "spacing": "increased",
                    "background": "light cream"
                },
                "comprehension_aids": ["highlighting", "text-to-speech", "summarization", "visual aids"]
            },
            "previous_strategies": {
                "task_breakdown": {
                    "effectiveness": 5,
                    "notes": "Essential for completing complex tasks"
                },
                "pomodoro_technique": {
                    "effectiveness": 4,
                    "notes": "Helps with focus but needs shorter intervals"
                },
                "text_to_speech": {
                    "effectiveness": 5,
                    "notes": "Critical for processing text efficiently"
                },
                "concept_mapping": {
                    "effectiveness": 4,
                    "notes": "Visual organization helps overcome both challenges"
                }
            }
        }
    
    # Default to ADHD if an invalid type is provided
    else:
        return load_sample_questionnaire("adhd")


def load_sample_material() -> Dict[str, Any]:
    """Load a sample learning material for testing"""
    return {
        "title": "Introduction to Neural Networks",
        "current_content": """
Neural networks are a set of algorithms, modeled loosely after the human brain, that are designed to recognize patterns. They interpret sensory data through a kind of machine perception, labeling or clustering raw input. The patterns they recognize are numerical, contained in vectors, into which all real-world data, be it images, sound, text or time series, must be translated.

Neural networks help us cluster and classify. You can think of them as a clustering and classification layer on top of the data you store and manage. They help to group unlabeled data according to similarities among the example inputs, and they classify data when they have a labeled dataset to train on.

The building block of a neural network is the neuron, a mathematical function that takes several inputs and produces a single output. When we have multiple neurons arranged in layers, we call it a neural network. The first layer receives the raw input, and the final layer produces the output. In between, there can be multiple "hidden layers" that transform the data in complex ways.

Each connection between neurons has a weight, which adjusts as the network learns. The learning process involves adjusting these weights to minimize the difference between the actual output and the expected output. This is done through a process called backpropagation, which calculates the gradient of the loss function with respect to the weights of the network.

Training a neural network requires a large amount of labeled data and computational resources. However, once trained, the network can make predictions or classifications with new data very quickly. This makes neural networks suitable for real-time applications.

Neural networks have been successfully applied to a wide range of problems, including image and speech recognition, natural language processing, and game playing. They are a key technology in the field of artificial intelligence and continue to drive advances in machine learning.
        """,
        "type": "text",
        "difficulty_level": "intermediate",
        "estimated_reading_time_minutes": 5
    }


def demonstrate_highlighting(sample_type: str = "adhd", output_dir: str = None, verbose: bool = False):
    """
    Demonstrate the highlighting functionality with AI agents
    
    Args:
        sample_type: Type of sample to use ("adhd", "dyslexia", or "combined")
        output_dir: Directory to save the results
        verbose: Whether to print detailed information
    """
    print(f"Starting highlighting demonstration with {sample_type.upper()} sample...")
    
    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Load sample data
    questionnaire_data = load_sample_questionnaire(sample_type)
    material_data = load_sample_material()
    
    if verbose:
        print("\n=== Sample Questionnaire Data ===")
        print(f"Diagnosed conditions: {', '.join(questionnaire_data['learning_difficulties']['diagnosed_conditions'])}")
        print(f"Comprehension aids: {', '.join(questionnaire_data['reading_patterns']['comprehension_aids'])}")
        
        print("\n=== Sample Learning Material ===")
        print(f"Title: {material_data['title']}")
        # print(f"First paragraph: {material_data['current_content'].strip().split('\\n\\n')[0]}")
    
    # Step 2: Initialize the processing state
    state = {
        "user_profile": {
            "questionnaire_answers": questionnaire_data,
            "analysis": {}
        },
        "learning_materials": material_data,
        "processed_content": {},
        "interaction_history": [],
        "current_focus": "start",
        "metadata": {},
        "iteration_count": 0
    }
    
    # Step 3: Profile Analyzer - Analyze user profile
    print("\n🧠 Profile Analyzer is analyzing user profile...")
    try:
        state = analyze_user_profile(state)
        difficulty_type = state['user_profile']['analysis'].get('difficulty_type', 'Unknown')
        print(f"✅ Profile analysis completed. Identified difficulty type: {difficulty_type}")
    except Exception as e:
        print(f"❌ Error in profile analysis: {str(e)}")
        difficulty_type = sample_type.upper()
    
    # Step 4: Process content based on difficulty type
    if difficulty_type == "ADHD" or difficulty_type == "Combined":
        print("\n🎯 Focus Enhancer is creating micro-content units with highlighting...")
        try:
            # Process with ADHD support
            state = micro_content_divider(state)
            micro_units = state['processed_content'].get('micro_units', [])
            print(f"✅ Created {len(micro_units)} micro-content units with highlighting")
            
            # Save the first micro unit as an HTML file for demonstration
            if micro_units and output_dir:
                html_content = "<html><head><title>Highlighted Micro Unit 1</title></head><body>" + micro_units[0]['content'] + "</body></html>"
                with open(os.path.join(output_dir, f"adhd_highlighted_unit_1.html"), 'w') as f:
                    f.write(html_content)
                print(f"✅ Saved highlighted micro unit to {os.path.join(output_dir, 'adhd_highlighted_unit_1.html')}")
        except Exception as e:
            print(f"❌ Error in ADHD support processing: {str(e)}")
    
    if difficulty_type == "Dyslexia" or difficulty_type == "Combined":
        print("\n📝 Text Transformer is simplifying text with highlighting...")
        try:
            # Process with Dyslexia support
            state = syntax_simplifier(state)
            simplified_text = state['processed_content'].get('simplified_text', {})
            print(f"✅ Created simplified text with highlighting")
            
            # Save the simplified text as an HTML file for demonstration
            if simplified_text and output_dir:
                html_content = "<html><head><title>Highlighted Simplified Text</title></head><body>" + simplified_text.get('content', '') + "</body></html>"
                with open(os.path.join(output_dir, f"dyslexia_highlighted_text.html"), 'w') as f:
                    f.write(html_content)
                print(f"✅ Saved highlighted simplified text to {os.path.join(output_dir, 'dyslexia_highlighted_text.html')}")
        except Exception as e:
            print(f"❌ Error in Dyslexia support processing: {str(e)}")
    
    # Step 5: Demonstrate direct highlighting without AI agent processing
    print("\n🔍 Demonstrating direct highlighting without AI agent processing...")
    try:
        # Get user's highlighter
        highlighter = get_highlighter_for_user(questionnaire_data)
        
        # Identify elements to highlight
        content_analyzer = ContentAnalyzer()
        elements_to_highlight = content_analyzer.identify_elements_to_highlight(
            material_data['current_content'], 
            difficulty_type
        )
        
        # Apply highlighting
        highlighted_content = material_data['current_content']
        for highlight_type, elements in elements_to_highlight.items():
            highlighted_content = highlighter.highlight_text(highlighted_content, highlight_type, elements)
        
        # Add CSS styles
        highlighted_content = "<style>" + highlighter.get_css() + "</style>\n" + highlighted_content
        
        # Save the directly highlighted content as an HTML file
        if output_dir:
            html_content = "<html><head><title>Directly Highlighted Content</title></head><body>" + highlighted_content + "</body></html>"
            with open(os.path.join(output_dir, "direct_highlighted_content.html"), 'w') as f:
                f.write(html_content)
            print(f"✅ Saved directly highlighted content to {os.path.join(output_dir, 'direct_highlighted_content.html')}")
        
        # Print highlighting statistics
        print(f"✅ Direct highlighting applied:")
        for highlight_type, elements in elements_to_highlight.items():
            print(f"  • {highlight_type.title()}: {len(elements)} elements")
    except Exception as e:
        print(f"❌ Error in direct highlighting: {str(e)}")
    
    # Step 6: Save the complete state if output directory is specified
    if output_dir:
        result_file = os.path.join(output_dir, f"highlighting_demo_{sample_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
        try:
            with open(result_file, 'w') as f:
                json.dump({
                    "sample_type": sample_type,
                    "user_profile": state["user_profile"],
                    "processed_content": state["processed_content"],
                    "timestamp": datetime.now().isoformat()
                }, f, indent=2)
            print(f"\n✅ Demo results saved to {result_file}")
        except Exception as e:
            print(f"\n❌ Error saving demo results: {str(e)}")
    
    print("\n🎉 Highlighting demonstration completed!")
    return state


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Demonstrate the highlighting functionality with AI agents")
    parser.add_argument("--sample", "-s", choices=["adhd", "dyslexia", "combined"], default="adhd",
                        help="Sample type to use for demonstration")
    parser.add_argument("--output", "-o", default="./highlighting_demo_results",
                        help="Directory to save the demonstration results")
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Print detailed information")
    args = parser.parse_args()
    
    demonstrate_highlighting(sample_type=args.sample, output_dir=args.output, verbose=args.verbose) 