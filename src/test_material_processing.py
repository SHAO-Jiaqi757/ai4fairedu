#!/usr/bin/env python3
"""
Test script for demonstrating how AI agents process learning materials
based on user questionnaire results and dashboard analysis.
"""

import os
import json
import argparse
from datetime import datetime
from typing import Dict, Any, List
import time
import pytest
import requests
from flask import Flask, session
from unittest.mock import patch, MagicMock

# Import the necessary modules
from src.user_profile import analyze_user_profile
from src.adhd_support import micro_content_divider
from src.dyslexia_support import syntax_simplifier
from src.content_generator import content_generator
from src.dashboard_analyzer import analyze_dashboard_data
from src.config import SystemConfig

# Import the app and necessary functions
from frontend.app import app as flask_app
from src.architecture import build_support_system

# Initialize configuration
config = SystemConfig()

def load_sample_questionnaire(sample_type: str = "adhd") -> Dict[str, Any]:
    """
    Load a sample questionnaire response for testing
    
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
    
    # ADHD-specific data
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
    
    # Dyslexia-specific data
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
                "comprehension_aids": ["text-to-speech", "simplified vocabulary", "visual aids"]
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
    
    # Combined ADHD and Dyslexia data
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
                "comprehension_aids": ["text-to-speech", "highlighting", "summarization", "visual aids"]
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

def test_material_processing(output_dir: str = None, verbose: bool = False, sample_type: str = "adhd"):
    """
    Test the material processing pipeline with sample data
    
    Args:
        output_dir: Directory to save the processing results
        verbose: Whether to print detailed processing information
        sample_type: Type of sample to use ("adhd", "dyslexia", or "combined")
    """
    print(f"Starting AI agent material processing test with {sample_type.upper()} sample...")
    
    # Create output directory if specified
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    
    # Step 1: Load sample data
    questionnaire_data = load_sample_questionnaire(sample_type)
    material_data = load_sample_material()
    
    if verbose:
        print("\n=== Sample Questionnaire Data ===")
        print(f"Age: {questionnaire_data['personal_info']['age']}")
        print(f"Education: {questionnaire_data['personal_info']['education_level']}")
        print(f"Diagnosed conditions: {', '.join(questionnaire_data['learning_difficulties']['diagnosed_conditions'])}")
        print(f"Average focus duration: {questionnaire_data['attention_patterns']['average_focus_duration_minutes']} minutes")
        
        print("\n=== Sample Learning Material ===")
        print(f"Title: {material_data['title']}")
        print(f"Type: {material_data['type']}")
        print(f"Difficulty: {material_data['difficulty_level']}")
        print(f"Estimated reading time: {material_data['estimated_reading_time_minutes']} minutes")
    
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
        profile_start_time = datetime.now()
        state = analyze_user_profile(state)
        profile_end_time = datetime.now()
        profile_duration = (profile_end_time - profile_start_time).total_seconds()
        
        print(f"✅ Profile analysis completed in {profile_duration:.2f} seconds")
        if verbose:
            print(f"Identified difficulty type: {state['user_profile']['analysis'].get('difficulty_type', 'Unknown')}")
            print(f"Severity level: {state['user_profile']['analysis'].get('severity_level', 'Unknown')}")
            
            # Extract recommended strategies
            strategies = state['user_profile'].get('support_strategies', {})
            if strategies:
                print("\nRecommended strategies:")
                for category, strats in strategies.items():
                    print(f"- {category.replace('_', ' ').title()}:")
                    for strat in strats[:2]:  # Show just a couple of strategies
                        print(f"  • {strat['name']}: {strat['description'][:50]}...")
    except Exception as e:
        print(f"❌ Error in profile analysis: {str(e)}")
    
    # Step 4: Focus Enhancer - Apply ADHD support if needed
    difficulty_type = state['user_profile'].get('analysis', {}).get('difficulty_type', 'Unknown')
    
    if difficulty_type == "ADHD" or difficulty_type == "Combined":
        print("\n🎯 Focus Enhancer is creating micro-content units...")
        try:
            adhd_start_time = datetime.now()
            state = micro_content_divider(state)
            adhd_end_time = datetime.now()
            adhd_duration = (adhd_end_time - adhd_start_time).total_seconds()
            
            micro_units = state['processed_content'].get('micro_units', [])
            print(f"✅ ADHD support processing completed in {adhd_duration:.2f} seconds")
            print(f"Created {len(micro_units)} micro-content units")
            
            if verbose and micro_units:
                print("\nMicro-content units:")
                for i, unit in enumerate(micro_units[:2], 1):  # Show just a couple of units
                    print(f"- Unit {i}:")
                    print(f"  • Estimated time: {unit.get('estimated_time_minutes', 'N/A')} minutes")
                    if 'key_points' in unit and unit['key_points']:
                        print(f"  • Key points: {len(unit['key_points'])}")
                    print(f"  • Content length: {len(unit.get('content', ''))}")
        except Exception as e:
            print(f"❌ Error in ADHD support processing: {str(e)}")
    
    # Step 5: Text Transformer - Apply Dyslexia support if needed
    if difficulty_type == "Dyslexia" or difficulty_type == "Combined":
        print("\n📝 Text Transformer is simplifying text...")
        try:
            dyslexia_start_time = datetime.now()
            state = syntax_simplifier(state)
            dyslexia_end_time = datetime.now()
            dyslexia_duration = (dyslexia_end_time - dyslexia_start_time).total_seconds()
            
            simplified_text = state['processed_content'].get('simplified_text', {})
            print(f"✅ Dyslexia support processing completed in {dyslexia_duration:.2f} seconds")
            
            if verbose and simplified_text:
                print("\nSimplified text:")
                print(f"- Content length: {len(simplified_text.get('content', ''))}")
                vocabulary = simplified_text.get('vocabulary', {})
                print(f"- Vocabulary assistance: {len(vocabulary)} terms")
                if vocabulary:
                    print("- Sample vocabulary terms:")
                    for term, definition in list(vocabulary.items())[:3]:  # Show just a few terms
                        print(f"  • {term}: {definition[:50]}...")
        except Exception as e:
            print(f"❌ Error in Dyslexia support processing: {str(e)}")
    
    # Step 6: Content Generator - Generate detailed content for each unit
    print("\n📚 Content Generator is creating detailed learning content...")
    try:
        content_gen_start_time = datetime.now()
        state = content_generator(state)
        content_gen_end_time = datetime.now()
        content_gen_duration = (content_gen_end_time - content_gen_start_time).total_seconds()
        
        detailed_units = state['processed_content'].get('detailed_units', [])
        print(f"✅ Content generation completed in {content_gen_duration:.2f} seconds")
        print(f"Generated detailed content for {len(detailed_units)} units")
        
        if verbose and detailed_units:
            print("\nDetailed content units:")
            for i, unit in enumerate(detailed_units[:2], 1):  # Show just a couple of units
                print(f"- Unit {i}:")
                print(f"  • Unit number: {unit.get('unit_number', 'N/A')}")
                print(f"  • Estimated time: {unit.get('estimated_time_minutes', 'N/A')} minutes")
                print(f"  • Content length: {len(unit.get('detailed_content', ''))}")
                # Print a snippet of the detailed content
                content_snippet = unit.get('detailed_content', '')[:100] + '...' if len(unit.get('detailed_content', '')) > 100 else unit.get('detailed_content', '')
                print(f"  • Content snippet: {content_snippet}")
    except Exception as e:
        print(f"❌ Error in content generation: {str(e)}")
    
    # Step 7: Insight Generator - Generate learning insights
    print("\n💡 Insight Generator is analyzing learning patterns...")
    try:
        insight_start_time = datetime.now()
        
        # Prepare data for dashboard analyzer
        dashboard_data = {
            "user_profile": state['user_profile'],
            "learning_history": [
                {
                    "material_id": "sample_material",
                    "title": material_data['title'],
                    "type": material_data['type'],
                    "difficulty_level": material_data['difficulty_level'],
                    "processed_content": state['processed_content'],
                    "timestamp": datetime.now().isoformat()
                }
            ]
        }
        
        # Analyze dashboard data
        insights = analyze_dashboard_data(dashboard_data)
        insight_end_time = datetime.now()
        insight_duration = (insight_end_time - insight_start_time).total_seconds()
        
        print(f"✅ Insight generation completed in {insight_duration:.2f} seconds")
        
        if verbose and insights:
            print("\nLearning insights:")
            for category, insight_list in insights.items():
                print(f"- {category.replace('_', ' ').title()}:")
                for insight in insight_list[:2]:  # Show just a couple of insights
                    print(f"  • {insight[:80]}...")
    except Exception as e:
        print(f"❌ Error in insight generation: {str(e)}")
    
    # Step 8: Save results if output directory is specified
    if output_dir:
        result_file = os.path.join(output_dir, f"material_processing_test_{sample_type}_{datetime.now().strftime('%Y%m%d%H%M%S')}.json")
        try:
            with open(result_file, 'w') as f:
                json.dump({
                    "sample_type": sample_type,
                    "user_profile": state["user_profile"],
                    "learning_materials": state["learning_materials"],
                    "processed_content": state["processed_content"],
                    "interaction_history": state["interaction_history"],
                    "timestamp": datetime.now().isoformat()
                }, f, indent=2)
            print(f"\n✅ Test results saved to {result_file}")
        except Exception as e:
            print(f"\n❌ Error saving test results: {str(e)}")
    
    print("\n🎉 Material processing test completed!")
    return state

def test_process_material_route():
    """
    Test the process_material route with a sample paragraph.
    This test verifies that:
    1. The material is correctly saved to a file
    2. The workflow is triggered with the correct initial state
    3. The processing status is updated correctly
    4. The final results contain the expected processed content structure
    """
    # Sample paragraph for testing
    sample_paragraph = """
    Artificial intelligence (AI) is intelligence demonstrated by machines, as opposed to natural intelligence displayed by animals including humans. 
    AI research has been defined as the field of study of intelligent agents, which refers to any system that perceives its environment and takes actions that maximize its chance of achieving its goals.
    The term "artificial intelligence" had previously been used to describe machines that mimic and display "human" cognitive skills that are associated with the human mind, such as "learning" and "problem-solving".
    This definition has since been rejected by major AI researchers who now describe AI in terms of rationality and acting rationally, which does not limit how intelligence can be articulated.
    """
    
    # Sample user profile for testing
    sample_user_profile = {
        "questionnaire_answers": {
            "learning_difficulties": {
                "diagnosed_conditions": ["ADHD"],
                "severity": 3
            },
            "reading_patterns": {
                "reading_speed": "slow",
                "comprehension_aids": ["highlighting", "summaries"]
            },
            "learning_preferences": {
                "preferred_formats": ["visual", "interactive"],
                "attention_span": "medium"
            }
        },
        "analysis": {
            "difficulty_type": "ADHD",
            "severity_level": 3,
            "attention_span_minutes": 15,
            "support_level": "moderate"
        }
    }
    
    # Mock the build_support_system function to avoid actual LLM calls
    with patch('src.architecture.build_support_system') as mock_build_system:
        # Create a mock workflow that returns a predefined result
        mock_workflow = MagicMock()
        mock_workflow.invoke.return_value = create_mock_processed_content(sample_paragraph)
        mock_build_system.return_value = mock_workflow
        
        # Configure Flask app for testing
        flask_app.config['TESTING'] = True
        flask_app.config['SECRET_KEY'] = 'test_key'
        flask_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        
        # Create a test client
        with flask_app.test_client() as client:
            # Set up session data
            with client.session_transaction() as sess:
                sess['user_id'] = "test_user_123"
                sess['questionnaire_answers'] = sample_user_profile["questionnaire_answers"]
                sess['user_analysis'] = sample_user_profile["analysis"]
            
            # Submit the material
            response = client.post('/process-material', data={
                'material_text': sample_paragraph,
                'material_title': 'Test AI Paragraph'
            }, follow_redirects=False)
            
            # Print response details for debugging
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.data.decode('utf-8')[:200]}...")  # Print first 200 chars
            
            # Check that we're redirected to the processing page
            assert response.status_code == 302
            assert '/material-processing' in response.location
            
            # Get the material_id from the session
            with client.session_transaction() as sess:
                material_id = sess.get('current_material', {}).get('id')
                user_id = sess.get('user_id')
            
            assert material_id is not None
            assert user_id is not None
            
            # Check that the material file was created
            material_dir = os.path.join(config.get("storage.learning_materials_path"))
            material_file_path = os.path.join(material_dir, f"{user_id}_{material_id}.txt")
            assert os.path.exists(material_file_path)
            
            # Read the saved material to verify content
            with open(material_file_path, 'r') as f:
                saved_content = f.read()
            assert sample_paragraph in saved_content
            
            # Check that the processing status file was created
            processing_dir = os.path.join(config.get("storage.results_path"), "processing")
            status_file = os.path.join(processing_dir, f"{user_id}_{material_id}_status.json")
            assert os.path.exists(status_file)
            
            # Verify the workflow was called with the correct initial state
            calls = mock_workflow.invoke.call_args_list
            assert len(calls) == 1
            initial_state = calls[0][0][0]  # First argument of the first call
            
            # Check key elements of the initial state
            assert initial_state["user_profile"]["analysis"]["difficulty_type"] == "ADHD"
            assert initial_state["learning_materials"]["title"] == "Test AI Paragraph"
            assert sample_paragraph in initial_state["learning_materials"]["current_content"]
            
            # Check the results file
            results_dir = os.path.join(config.get("storage.results_path"))
            results_file = os.path.join(results_dir, f"{user_id}_{material_id}_results.json")
            
            # Since processing happens in a background thread, we need to wait for it
            # In a real test, you might want to mock the threading or use a synchronous version
            max_wait = 5  # seconds
            start_time = time.time()
            while not os.path.exists(results_file) and time.time() - start_time < max_wait:
                time.sleep(0.1)
            
            assert os.path.exists(results_file), "Results file was not created within the timeout period"
            
            # Read the results file
            with open(results_file, 'r') as f:
                results = json.load(f)
            
            # Verify the structure of the processed content
            assert "processed_content" in results
            processed_content = results["processed_content"]
            
            # Check for sections in the processed content
            assert "sections" in processed_content
            assert len(processed_content["sections"]) > 0
            
            # Check the first section
            first_section = processed_content["sections"][0]
            assert "title" in first_section
            assert "content" in first_section
            assert "micro_units" in first_section  # For ADHD support
            assert "detailed_units" in first_section  # For content generator
            
            # Check detailed units
            assert "detailed_units" in processed_content
            assert len(processed_content["detailed_units"]) > 0
            
            # Check the first detailed unit
            first_detailed_unit = processed_content["detailed_units"][0]
            assert "unit_number" in first_detailed_unit
            assert "estimated_time_minutes" in first_detailed_unit
            assert "summary" in first_detailed_unit
            assert "detailed_content" in first_detailed_unit
            
            # Clean up test files
            if os.path.exists(material_file_path):
                os.remove(material_file_path)
            if os.path.exists(status_file):
                os.remove(status_file)
            if os.path.exists(results_file):
                os.remove(results_file)

def create_mock_processed_content(original_text: str) -> Dict[str, Any]:
    """
    Create a mock processed content structure that mimics what the real workflow would produce.
    This avoids having to call actual LLMs during testing.
    """
    # Split the paragraph into sentences for micro units
    sentences = [s.strip() for s in original_text.split('.') if s.strip()]
    
    # Create micro units (for ADHD support)
    micro_units = []
    for i, sentence in enumerate(sentences[:3]):  # Use first 3 sentences
        micro_units.append({
            "content": f"<p>{sentence}.</p>",
            "unit_number": i + 1,
            "estimated_time_minutes": 2,
            "check_points": [f"What is the main point of this unit?"]
        })
    
    # Create detailed units (for content generator)
    detailed_units = []
    for i, unit in enumerate(micro_units):
        detailed_units.append({
            "unit_number": unit["unit_number"],
            "estimated_time_minutes": unit["estimated_time_minutes"],
            "summary": unit["content"],
            "detailed_content": f"""
# Unit {i+1}: Detailed Content

{sentences[i] if i < len(sentences) else 'Additional content for this unit.'}.

## Key Points
- This is an important concept in this unit
- Here's another key point to understand
- And a third point for completeness

## Examples
Here's an example that illustrates the main concept:
- Example 1: Practical application
- Example 2: Another scenario

## Understanding Check
{unit.get('check_points', ['What did you learn from this unit?'])[0]}

**Answer**: The main point is to understand {sentences[i][:30]}...
"""
        })
    
    # Create a simplified version (for dyslexia support)
    simplified_content = "<p>" + "</p><p>".join([s + "." for s in sentences]) + "</p>"
    
    # Create vocabulary items
    vocabulary = {
        "artificial intelligence": "Intelligence demonstrated by machines rather than humans or animals.",
        "cognitive skills": "Mental abilities that involve thinking, learning, and memory.",
        "rationality": "The quality of being based on reason or logic."
    }
    
    # Create the full processed content structure
    return {
        "user_profile": {
            "questionnaire_answers": {},
            "analysis": {
                "difficulty_type": "ADHD",
                "severity_level": 3,
                "attention_span_minutes": 15,
                "support_level": "moderate"
            }
        },
        "learning_materials": {
            "title": "Test AI Paragraph",
            "current_content": original_text,
            "type": "text",
            "difficulty_level": "intermediate",
            "estimated_reading_time_minutes": 2
        },
        "processed_content": {
            "micro_units": micro_units,
            "simplified_text": {
                "content": simplified_content,
                "vocabulary": vocabulary
            },
            "detailed_units": detailed_units,
            "sections": [
                {
                    "id": "section-1",
                    "title": "Introduction to Artificial Intelligence",
                    "content": original_text,
                    "simplified_content": simplified_content,
                    "micro_units": micro_units,
                    "detailed_units": detailed_units,
                    "key_concepts": ["Artificial Intelligence", "Intelligence", "Cognitive Skills"],
                    "vocabulary": vocabulary,
                    "estimated_time": 5,
                    "difficulty_level": "Intermediate"
                }
            ]
        },
        "interaction_history": [
            {
                "step": "profile_analyzer",
                "memory": ["Analyzed user profile: ADHD with moderate severity"]
            },
            {
                "step": "adhd_support",
                "memory": ["Created micro-content units for ADHD support"]
            },
            {
                "step": "dyslexia_support",
                "memory": ["Applied syntax simplification for dyslexia support"]
            },
            {
                "step": "content_generation_processor",
                "memory": ["Generated detailed content for each micro unit"]
            }
        ],
        "current_focus": "end",
        "metadata": {},
        "iteration_count": 1
    }

def test_learning_view_with_processed_content():
    """
    Test that the learning view correctly displays processed content.
    """
    # Sample processed content
    processed_content = create_mock_processed_content("Sample text for testing the learning view.")
    
    # Configure Flask app for testing
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test_key'
    flask_app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
    
    # Create a test client
    with flask_app.test_client() as client:
        # Set up session data
        with client.session_transaction() as sess:
            sess['user_id'] = "test_user_123"
            sess['current_material'] = {
                'id': 'test_material_123',
                'title': 'Test Material',
                'word_count': 100,
                'estimated_reading_time': 5
            }
            sess['user_analysis'] = processed_content["user_profile"]["analysis"]
            sess['questionnaire_answers'] = {
                "learning_difficulties": {
                    "diagnosed_conditions": ["ADHD"],
                    "severity": 3
                },
                "reading_patterns": {
                    "reading_speed": "slow",
                    "comprehension_aids": ["highlighting", "summaries"]
                },
                "learning_preferences": {
                    "preferred_formats": ["visual", "interactive"],
                    "attention_span": "medium"
                }
            }
        
        # Mock the loading of processed content
        with patch('frontend.app.load_processed_content') as mock_load_content:
            mock_load_content.return_value = (
                processed_content["processed_content"],
                processed_content["learning_materials"]["current_content"]
            )
            
            # Access the learning view
            response = client.get('/learning-view')
            
            # Print response details for debugging
            print(f"Response status code: {response.status_code}")
            print(f"Response data: {response.data.decode('utf-8')[:200]}...")  # Print first 200 chars
            
            # Check that the page loaded successfully
            assert response.status_code == 200
            
            # Check for key elements in the HTML response
            html = response.data.decode('utf-8')
            
            # Check for the material title
            assert 'Test Material' in html
            
            # Check for section title
            assert 'Introduction to Artificial Intelligence' in html
            
            # Check for micro units (ADHD support)
            assert 'micro-unit' in html.lower() or 'micro unit' in html.lower()
            
            # Check for detailed content (Content Generator)
            assert 'detailed content' in html.lower() or 'detailed-content' in html.lower()
            assert 'key points' in html.lower()
            assert 'understanding check' in html.lower()
            
            # Check for simplified content (Dyslexia support)
            assert 'simplified' in html.lower()
            
            # Check for vocabulary
            assert 'vocabulary' in html.lower()
            assert 'artificial intelligence' in html.lower()

if __name__ == "__main__":
    # Run the tests
    pytest.main(["-xvs", __file__]) 