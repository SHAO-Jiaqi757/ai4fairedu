#!/usr/bin/env python
"""
Script to run dashboard analysis in a separate process.
This avoids the issue of accessing Flask session from a background thread.
"""

import os
import sys
import json
import argparse
from typing import Dict, Any

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dashboard_analyzer import analyze_dashboard_data
from src.config import SystemConfig

def run_analysis(user_id: str, language: str = "en") -> None:
    """Run the dashboard analysis for a user"""
    # Initialize configuration
    config = SystemConfig()
    
    # Set up paths
    analysis_dir = os.path.join(config.get("storage.results_path"), "analysis")
    questionnaire_file = os.path.join(analysis_dir, f"{user_id}_questionnaire.json")
    analysis_file = os.path.join(analysis_dir, f"{user_id}_dashboard_analysis.json")
    in_progress_file = os.path.join(analysis_dir, f"{user_id}_analysis_in_progress")
    
    try:
        # Load questionnaire data
        with open(questionnaire_file, 'r') as f:
            questionnaire_data = json.load(f)
        
        # Run the analysis
        dashboard_data = analyze_dashboard_data(questionnaire_data, language)
        
        # Save the results to the file (for backward compatibility)
        with open(analysis_file, 'w') as f:
            json.dump(dashboard_data, f, indent=2)
        
        # Save the results to the database-like structure
        config.save_user_analysis(user_id, dashboard_data, language)
        
        # Clean up
        if os.path.exists(questionnaire_file):
            os.remove(questionnaire_file)
    except Exception as e:
        # Log the error
        with open(os.path.join(analysis_dir, f"{user_id}_analysis_error.log"), 'w') as f:
            f.write(f"Error running analysis: {str(e)}")
    finally:
        # Remove the in-progress file
        if os.path.exists(in_progress_file):
            os.remove(in_progress_file)

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='Run dashboard analysis')
    parser.add_argument('--user_id', required=True, help='User ID')
    parser.add_argument('--language', default='en', help='Language (en or zh)')
    
    args = parser.parse_args()
    run_analysis(args.user_id, args.language)

if __name__ == "__main__":
    main() 