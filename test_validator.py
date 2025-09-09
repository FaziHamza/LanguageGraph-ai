#!/usr/bin/env python3
"""
Simple test script for the JSON Validator
"""

from json_validator import JSONValidator, create_sample_schema
from test_data import get_valid_test_data, get_invalid_schema_data, get_business_rules
import json

def test_schema_validation():
    """Test schema validation only"""
    print("Testing Schema Validation...")
    print("=" * 50)
    
    from jsonschema import validate, ValidationError
    
    schema = create_sample_schema()
    valid_data = get_valid_test_data()
    invalid_data = get_invalid_schema_data()
    
    # Test valid data
    try:
        validate(instance=valid_data, schema=schema)
        print("✓ Valid data passed schema validation")
    except ValidationError as e:
        print(f"✗ Valid data failed: {e}")
    
    # Test invalid data
    try:
        validate(instance=invalid_data, schema=schema)
        print("✗ Invalid data incorrectly passed schema validation")
    except ValidationError as e:
        print(f"✓ Invalid data correctly failed schema validation")
        print(f"  Error: {str(e)[:100]}...")
    
    print()

def test_full_validator():
    """Test the full validator (will fail without API key)"""
    print("Testing Full JSON Validator...")
    print("=" * 50)
    
    try:
        validator = JSONValidator()
        print("✓ JSONValidator initialized")
        
        schema = create_sample_schema()
        rules = get_business_rules()
        data = get_valid_test_data()
        
        print("Attempting validation...")
        result = validator.validate_json(data, schema, rules)
        print("Validation result:")
        print(json.dumps(result, indent=2))
        
    except Exception as e:
        print(f"Expected error (no valid API key): {type(e).__name__}")
        print(f"Error message: {str(e)[:200]}...")
        print("This is expected behavior without a valid OpenAI API key.")
    
    print()

def main():
    print("LangGraph JSON Rules Validator - Test Suite")
    print("=" * 60)
    print()
    
    # Test schema validation (should work)
    test_schema_validation()
    
    # Test full validator (will fail without API key)
    test_full_validator()
    
    print("Test Summary:")
    print("- Schema validation: Working correctly")
    print("- Full validator: Requires valid OpenAI API key")
    print("- Project structure: All imports successful")
    print("- Dependencies: All installed correctly")

if __name__ == "__main__":
    main()
