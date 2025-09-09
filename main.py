"""
Main application for LangGraph JSON Rules Validator

This script provides a command-line interface and demonstration of the
JSON validation system using LangGraph workflows.
"""

import json
import sys
import argparse
from typing import Dict, Any, List, Optional

from json_validator import JSONValidator, create_sample_schema, create_sample_rules
from test_data import (
    get_valid_test_data,
    get_invalid_schema_data,
    get_invalid_semantic_data,
    get_edge_case_data,
    get_business_rules,
    get_strict_business_rules,
    get_technical_rules
)

def print_separator(title: str = ""):
    """Print a formatted separator"""
    if title:
        print(f"\n{'='*20} {title} {'='*20}")
    else:
        print("="*60)

def print_validation_result(result: Dict[str, Any], title: str = "Validation Result"):
    """Print formatted validation results"""
    print_separator(title)
    print(f"Overall Valid: {result['overall_valid']}")
    print(f"Schema Validation: {'✓ PASSED' if result['schema_validation']['passed'] else '✗ FAILED'}")
    print(f"Semantic Validation: {'✓ PASSED' if result['semantic_validation']['passed'] else '✗ FAILED'}")
    
    if result['schema_validation']['errors']:
        print("\nSchema Errors:")
        for error in result['schema_validation']['errors']:
            print(f"  - {error}")
    
    if result['semantic_validation']['errors']:
        print("\nSemantic Errors:")
        for error in result['semantic_validation']['errors']:
            print(f"  - {error}")
    
    print(f"\nSummary: {result['summary']}")

def run_demo():
    """Run a comprehensive demonstration of the JSON validator"""
    print("LangGraph JSON Rules Validator - Demo")
    print_separator()
    
    # Initialize validator
    try:
        validator = JSONValidator()
        print("✓ JSON Validator initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize validator: {e}")
        print("Make sure you have set your OPENAI_API_KEY in a .env file")
        return
    
    # Get schema and rules
    schema = create_sample_schema()
    rules = get_business_rules()
    
    print(f"\nUsing {len(rules)} business rules for validation:")
    for i, rule in enumerate(rules, 1):
        print(f"  {i}. {rule}")
    
    # Test cases
    test_cases = [
        ("Valid Data", get_valid_test_data()),
        ("Invalid Schema Data", get_invalid_schema_data()),
        ("Invalid Semantic Data", get_invalid_semantic_data()),
    ]
    
    # Add edge cases
    edge_cases = get_edge_case_data()
    for i, case in enumerate(edge_cases, 1):
        test_cases.append((f"Edge Case {i}", case))
    
    # Run validations
    for test_name, test_data in test_cases:
        print_separator(f"Testing: {test_name}")
        print("JSON Data:")
        print(json.dumps(test_data, indent=2))
        
        try:
            result = validator.validate_json(test_data, schema, rules)
            print_validation_result(result)
        except Exception as e:
            print(f"✗ Validation failed with error: {e}")
        
        print()

def run_interactive_mode():
    """Run interactive mode for custom JSON validation"""
    print("LangGraph JSON Rules Validator - Interactive Mode")
    print_separator()
    
    # Initialize validator
    try:
        validator = JSONValidator()
        print("✓ JSON Validator initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize validator: {e}")
        return
    
    while True:
        print("\nOptions:")
        print("1. Validate custom JSON")
        print("2. Use predefined test data")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "3":
            print("Goodbye!")
            break
        elif choice == "1":
            validate_custom_json(validator)
        elif choice == "2":
            validate_predefined_data(validator)
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def validate_custom_json(validator: JSONValidator):
    """Handle custom JSON validation"""
    print("\nCustom JSON Validation")
    print("-" * 30)
    
    # Get JSON data
    print("Enter your JSON data (press Enter twice when done):")
    json_lines = []
    while True:
        line = input()
        if line == "" and json_lines and json_lines[-1] == "":
            break
        json_lines.append(line)
    
    json_text = "\n".join(json_lines[:-1])  # Remove last empty line
    
    try:
        json_data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON format: {e}")
        return
    
    # Choose rule set
    print("\nSelect rule set:")
    print("1. Business rules")
    print("2. Strict business rules")
    print("3. Technical rules")
    print("4. Custom rules")
    
    rule_choice = input("Enter choice (1-4): ").strip()
    
    if rule_choice == "1":
        rules = get_business_rules()
    elif rule_choice == "2":
        rules = get_strict_business_rules()
    elif rule_choice == "3":
        rules = get_technical_rules()
    elif rule_choice == "4":
        print("Enter custom rules (one per line, press Enter twice when done):")
        rules = []
        while True:
            rule = input()
            if rule == "":
                break
            rules.append(rule)
    else:
        print("Invalid choice, using business rules")
        rules = get_business_rules()
    
    # Use sample schema (in real app, this could be customizable too)
    schema = create_sample_schema()
    
    # Validate
    try:
        result = validator.validate_json(json_data, schema, rules)
        print_validation_result(result, "Custom JSON Validation")
    except Exception as e:
        print(f"✗ Validation failed: {e}")

def validate_predefined_data(validator: JSONValidator):
    """Handle predefined test data validation"""
    print("\nPredefined Test Data Validation")
    print("-" * 35)
    
    test_options = [
        ("Valid test data", get_valid_test_data()),
        ("Invalid schema data", get_invalid_schema_data()),
        ("Invalid semantic data", get_invalid_semantic_data()),
    ]
    
    edge_cases = get_edge_case_data()
    for i, case in enumerate(edge_cases, 1):
        test_options.append((f"Edge case {i}", case))
    
    print("Select test data:")
    for i, (name, _) in enumerate(test_options, 1):
        print(f"{i}. {name}")
    
    try:
        choice = int(input("Enter choice: ")) - 1
        if 0 <= choice < len(test_options):
            name, data = test_options[choice]
            schema = create_sample_schema()
            rules = get_business_rules()
            
            print(f"\nValidating: {name}")
            print("JSON Data:")
            print(json.dumps(data, indent=2))
            
            result = validator.validate_json(data, schema, rules)
            print_validation_result(result)
        else:
            print("Invalid choice")
    except ValueError:
        print("Please enter a valid number")
    except Exception as e:
        print(f"✗ Validation failed: {e}")

def validate_file(file_path: str, validator: JSONValidator):
    """Validate JSON from a file"""
    try:
        with open(file_path, 'r') as f:
            json_data = json.load(f)
        
        schema = create_sample_schema()
        rules = get_business_rules()
        
        print(f"Validating file: {file_path}")
        result = validator.validate_json(json_data, schema, rules)
        print_validation_result(result)
        
    except FileNotFoundError:
        print(f"✗ File not found: {file_path}")
    except json.JSONDecodeError as e:
        print(f"✗ Invalid JSON in file: {e}")
    except Exception as e:
        print(f"✗ Error validating file: {e}")

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description="LangGraph JSON Rules Validator")
    parser.add_argument("--demo", action="store_true", help="Run demonstration mode")
    parser.add_argument("--interactive", action="store_true", help="Run interactive mode")
    parser.add_argument("--file", type=str, help="Validate JSON from file")
    parser.add_argument("--show-test-data", action="store_true", help="Show test data examples")
    
    args = parser.parse_args()
    
    if args.show_test_data:
        print("Test Data Examples")
        print_separator()
        
        print("\n1. Valid Data:")
        print(json.dumps(get_valid_test_data(), indent=2))
        
        print("\n2. Invalid Schema Data:")
        print(json.dumps(get_invalid_schema_data(), indent=2))
        
        print("\n3. Invalid Semantic Data:")
        print(json.dumps(get_invalid_semantic_data(), indent=2))
        
        return
    
    if args.file:
        try:
            validator = JSONValidator()
            validate_file(args.file, validator)
        except Exception as e:
            print(f"✗ Failed to initialize validator: {e}")
        return
    
    if args.demo:
        run_demo()
    elif args.interactive:
        run_interactive_mode()
    else:
        # Default behavior - show help and run demo
        parser.print_help()
        print("\nRunning demo by default...\n")
        run_demo()

if __name__ == "__main__":
    main()
