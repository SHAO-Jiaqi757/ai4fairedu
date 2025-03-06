#!/usr/bin/env python
import json
import os
import sys
from typing import Dict, Any

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dashboard_analyzer import analyze_dashboard_data, create_dashboard_analyzer_prompt
from src.config import SystemConfig

# Mock questionnaire data
mock_questionnaire = {
    "personal_info": {
        "age": 16,
        "education_level": "high",
        "subject_interests": ["Science", "History", "Art"]
    },
    "learning_difficulties": {
        "diagnosed_conditions": ["ADHD", "Mild Dyslexia"],
        "self_reported_challenges": [
            "Difficulty maintaining focus on lengthy materials",
            "Reading fatigue with long texts",
            "Complex sentence comprehension difficulties",
            "Easily distracted by environment",
            "Task organization and planning difficulties"
        ]
    },
    "attention_patterns": {
        "average_focus_duration_minutes": 15,
        "best_focus_time_of_day": ["Morning", "Evening"],
        "distraction_triggers": ["Noise", "Visual clutter", "Phone notifications"],
        "hyperfocus_activities": ["Drawing", "Solving interesting problems", "Video games"]
    },
    "reading_patterns": {
        "reading_speed": "slow",
        "difficult_text_features": ["Long sentences", "Uncommon words", "Dense paragraphs"],
        "preferred_text_format": {
            "font": "Arial",
            "size": "large",
            "spacing": "wide",
            "background": "cream"
        },
        "comprehension_aids": ["Charts", "Concept maps", "Pre-reading questions"]
    },
    "learning_preferences": {
        "modality_preference": {
            "visual": 0.7,
            "auditory": 0.4,
            "kinesthetic": 0.8
        },
        "feedback_preference": "immediate",
        "group_vs_individual": "somewhat_individual",
        "technology_comfort": "very_comfortable"
    },
    "previous_strategies": {
        "task_breakdown": {
            "effectiveness": 4,
            "notes": "Breaking down large tasks into smaller steps is helpful"
        },
        "pomodoro_technique": {
            "effectiveness": 3,
            "notes": "25 minutes is too long, 15 minutes works better"
        },
        "text_to_speech": {
            "effectiveness": 4,
            "notes": "Combining listening and reading improves comprehension"
        },
        "concept_mapping": {
            "effectiveness": 5,
            "notes": "Visual organization of information is very effective"
        }
    }
}

def print_formatted_json(data: Dict[str, Any]) -> None:
    """Print formatted JSON data"""
    print(json.dumps(data, indent=2, ensure_ascii=False))

def test_dashboard_analyzer() -> None:
    """Test the dashboard analyzer with mock questionnaire data"""
    print("Testing dashboard analyzer with mock questionnaire data...")
    
    # Test English analysis
    print("\n=== ENGLISH ANALYSIS ===")
    result_en = analyze_dashboard_data(mock_questionnaire, language="en")
    print_formatted_json(result_en)
    
    # Test Chinese analysis
    print("\n=== CHINESE ANALYSIS ===")
    result_zh = analyze_dashboard_data(mock_questionnaire, language="zh")
    print_formatted_json(result_zh)

def print_system_prompt() -> None:
    """Print the system prompt for review"""
    print("\n=== CURRENT SYSTEM PROMPT (ENGLISH) ===")
    prompt_template = create_dashboard_analyzer_prompt(language="en")
    
    # The structure of the prompt template is different than expected
    # Let's print the raw prompt template to see its structure
    try:
        # Try to access the system message directly from the prompt template
        system_message = prompt_template.messages[0]
        print(system_message.prompt.template)
    except Exception as e:
        print(f"Error accessing system message: {e}")
        print("Printing raw prompt template structure:")
        print(prompt_template)

if __name__ == "__main__":
    # Print the current system prompt
    print_system_prompt()
    
    # Run the test
    test_dashboard_analyzer()
