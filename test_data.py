"""
Test data and examples for JSON validation
"""

import json
from typing import Dict, Any, List

def get_valid_test_data() -> Dict[str, Any]:
    """Returns valid JSON data that should pass all validations"""
    return {
        "user": {
            "id": 123,
            "name": "John Smith",
            "email": "john.smith@company.com",
            "age": 28,
            "roles": ["admin", "user"]
        },
        "metadata": {
            "created_at": "2024-01-15T10:30:00Z",
            "version": "1.2.0"
        }
    }

def get_invalid_schema_data() -> Dict[str, Any]:
    """Returns JSON data that fails schema validation"""
    return {
        "user": {
            "id": "not_a_number",  # Should be integer
            "name": "",  # Empty string, violates minLength
            "email": "invalid-email",  # Invalid email format
            "age": -5,  # Negative age
            "roles": []  # Empty array, violates minItems
        },
        "metadata": {
            "created_at": "invalid-date",  # Invalid date format
            # Missing required "version" field
        }
    }

def get_invalid_semantic_data() -> Dict[str, Any]:
    """Returns JSON data that passes schema but fails semantic rules"""
    return {
        "user": {
            "id": 456,
            "name": "User123!@#",  # Contains special characters and numbers
            "email": "user@gmail.com",  # Personal email domain
            "age": 16,  # Too young for admin role
            "roles": ["admin", "invalid_role"]  # Contains invalid role
        },
        "metadata": {
            "created_at": "2025-12-31T23:59:59Z",  # Future date
            "version": "invalid.version.format"  # Invalid semantic versioning
        }
    }

def get_edge_case_data() -> List[Dict[str, Any]]:
    """Returns various edge cases for testing"""
    return [
        # Minimum valid age with guest role
        {
            "user": {
                "id": 1,
                "name": "Young User",
                "email": "young@company.com",
                "age": 0,
                "roles": ["guest"]
            },
            "metadata": {
                "created_at": "2024-01-01T00:00:00Z",
                "version": "0.1.0"
            }
        },
        # Maximum valid age
        {
            "user": {
                "id": 2,
                "name": "Senior User",
                "email": "senior@enterprise.org",
                "age": 150,
                "roles": ["user"]
            },
            "metadata": {
                "created_at": "2024-06-15T12:00:00Z",
                "version": "10.0.0"
            }
        },
        # Multiple roles
        {
            "user": {
                "id": 3,
                "name": "Multi Role User",
                "email": "multi@business.net",
                "age": 35,
                "roles": ["admin", "moderator", "user"]
            },
            "metadata": {
                "created_at": "2024-03-20T08:30:00Z",
                "version": "2.1.3"
            }
        }
    ]

def get_business_rules() -> List[str]:
    """Returns business-specific validation rules"""
    return [
        "User age must be reasonable for the assigned roles (e.g., admin role requires age >= 18)",
        "Email domain should be from a business domain (not personal email providers like gmail, yahoo, hotmail)",
        "User name should not contain special characters or numbers",
        "At least one role must be assigned, and roles should be from: ['user', 'admin', 'moderator', 'guest']",
        "Version should follow semantic versioning format (e.g., 1.0.0)",
        "Created timestamp should not be in the future"
    ]

def get_strict_business_rules() -> List[str]:
    """Returns stricter business validation rules"""
    return [
        "Admin users must be at least 21 years old",
        "Moderator users must be at least 18 years old",
        "Email domain must be from approved corporate domains: ['company.com', 'enterprise.org', 'business.net']",
        "User names must be between 2 and 50 characters and contain only letters and spaces",
        "Users can have maximum 3 roles assigned",
        "Version must be a stable release (no pre-release identifiers like alpha, beta, rc)",
        "Created timestamp must be within the last 2 years"
    ]

def get_technical_rules() -> List[str]:
    """Returns technical validation rules"""
    return [
        "User ID must be a positive integer and unique within the system",
        "Email must be a valid RFC 5322 compliant email address",
        "Age must be between 0 and 150 years",
        "Roles array must not contain duplicates",
        "Version must follow semantic versioning specification (semver.org)",
        "Created timestamp must be in ISO 8601 format with UTC timezone"
    ]

if __name__ == "__main__":
    print("Test Data Examples")
    print("=" * 50)
    
    print("\n1. Valid Data:")
    print(json.dumps(get_valid_test_data(), indent=2))
    
    print("\n2. Invalid Schema Data:")
    print(json.dumps(get_invalid_schema_data(), indent=2))
    
    print("\n3. Invalid Semantic Data:")
    print(json.dumps(get_invalid_semantic_data(), indent=2))
    
    print("\n4. Edge Cases:")
    for i, data in enumerate(get_edge_case_data(), 1):
        print(f"\nEdge Case {i}:")
        print(json.dumps(data, indent=2))
    
    print("\n5. Business Rules:")
    for rule in get_business_rules():
        print(f"- {rule}")
