#!/usr/bin/env python3
"""
Script to run the material processing test
"""

import os
import sys
import argparse
from datetime import datetime
import pytest
from src.test_material_processing import test_process_material_route, test_learning_view_with_processed_content

# Add the parent directory to the path so we can import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.test_material_processing import test_material_processing
from src.config import SystemConfig

# Initialize configuration
config = SystemConfig()

def main():
    """
    Run tests for the material processing functionality.
    """
    parser = argparse.ArgumentParser(description="Test the AI agent material processing pipeline")
    parser.add_argument("--test", "-t", choices=["all", "process", "learning", "workflow"], 
                        default="all", help="Which test to run")
    parser.add_argument("--output", "-o", help="Directory to save the processing results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed processing information")
    parser.add_argument("--sample", "-s", choices=["adhd", "dyslexia", "combined"], 
                        default="adhd", help="Sample type to use for testing")
    args = parser.parse_args()
    
    # Set up output directory
    if args.output:
        os.makedirs(args.output, exist_ok=True)
    
    # Run the selected test
    if args.test == "all" or args.test == "process":
        print("\n=== Testing process_material route ===")
        try:
            test_process_material_route()
            print("✅ process_material route test passed")
        except Exception as e:
            print(f"❌ process_material route test failed: {str(e)}")
            if args.verbose:
                import traceback
                traceback.print_exc()
    
    if args.test == "all" or args.test == "learning":
        print("\n=== Testing learning_view with processed content ===")
        try:
            test_learning_view_with_processed_content()
            print("✅ learning_view test passed")
        except Exception as e:
            print(f"❌ learning_view test failed: {str(e)}")
            if args.verbose:
                import traceback
                traceback.print_exc()
    
    if args.test == "all" or args.test == "workflow":
        print("\n=== Testing full material processing workflow ===")
        try:
            test_material_processing(output_dir=args.output, verbose=args.verbose, sample_type=args.sample)
            print("✅ Material processing workflow test passed")
        except Exception as e:
            print(f"❌ Material processing workflow test failed: {str(e)}")
            if args.verbose:
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    main() 