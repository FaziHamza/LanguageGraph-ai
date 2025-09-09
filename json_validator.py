"""
LangGraph JSON Rules Validator

This module implements a LangGraph workflow for validating JSON data against
custom rules using both schema validation and LLM-based semantic validation.
"""

import json
import os
from typing import Dict, Any, List, Optional, TypedDict
from dataclasses import dataclass
from enum import Enum

import jsonschema
from jsonschema import validate, ValidationError
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class ValidationStatus(Enum):
    PENDING = "pending"
    SCHEMA_VALID = "schema_valid"
    SCHEMA_INVALID = "schema_invalid"
    SEMANTIC_VALID = "semantic_valid"
    SEMANTIC_INVALID = "semantic_invalid"
    COMPLETE = "complete"

class ValidationState(TypedDict):
    """State object for the validation workflow"""
    json_data: Dict[str, Any]
    schema: Dict[str, Any]
    custom_rules: List[str]
    status: ValidationStatus
    schema_errors: List[str]
    semantic_errors: List[str]
    is_valid: bool
    validation_report: Dict[str, Any]

@dataclass
class ValidationRule:
    """Custom validation rule definition"""
    name: str
    description: str
    rule_type: str  # "schema", "semantic", "business"
    validation_logic: str

class JSONValidator:
    """Main JSON validator using LangGraph workflow"""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        self.llm = ChatOpenAI(
            api_key=openai_api_key or os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo",
            temperature=0
        )
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph workflow for JSON validation"""
        
        def schema_validation_node(state: ValidationState) -> ValidationState:
            """Validate JSON against schema"""
            try:
                validate(instance=state["json_data"], schema=state["schema"])
                state["status"] = ValidationStatus.SCHEMA_VALID
                state["schema_errors"] = []
            except ValidationError as e:
                state["status"] = ValidationStatus.SCHEMA_INVALID
                state["schema_errors"] = [str(e)]
            except Exception as e:
                state["status"] = ValidationStatus.SCHEMA_INVALID
                state["schema_errors"] = [f"Schema validation error: {str(e)}"]
            
            return state
        
        def semantic_validation_node(state: ValidationState) -> ValidationState:
            """Validate JSON using LLM for semantic rules"""
            if state["status"] == ValidationStatus.SCHEMA_INVALID:
                # Skip semantic validation if schema validation failed
                state["semantic_errors"] = ["Skipped due to schema validation failure"]
                return state
            
            try:
                # Prepare prompt for LLM
                system_prompt = """You are a JSON validation expert. Analyze the provided JSON data against the custom rules and determine if it's valid.

Rules to validate:
{rules}

Respond with a JSON object containing:
- "is_valid": boolean
- "errors": list of error messages (empty if valid)
- "warnings": list of warning messages (optional)

Be thorough and check each rule carefully."""

                human_prompt = f"""JSON Data to validate:
{json.dumps(state['json_data'], indent=2)}

Custom Rules:
{chr(10).join(f'- {rule}' for rule in state['custom_rules'])}

Please validate this JSON against the rules and provide your assessment."""

                messages = [
                    SystemMessage(content=system_prompt.format(rules='\n'.join(state['custom_rules']))),
                    HumanMessage(content=human_prompt)
                ]
                
                response = self.llm.invoke(messages)
                
                # Parse LLM response
                try:
                    validation_result = json.loads(response.content)
                    if validation_result.get("is_valid", False):
                        state["status"] = ValidationStatus.SEMANTIC_VALID
                        state["semantic_errors"] = []
                    else:
                        state["status"] = ValidationStatus.SEMANTIC_INVALID
                        state["semantic_errors"] = validation_result.get("errors", ["Semantic validation failed"])
                except json.JSONDecodeError:
                    state["status"] = ValidationStatus.SEMANTIC_INVALID
                    state["semantic_errors"] = ["Failed to parse LLM validation response"]
                    
            except Exception as e:
                state["status"] = ValidationStatus.SEMANTIC_INVALID
                state["semantic_errors"] = [f"Semantic validation error: {str(e)}"]
            
            return state
        
        def final_assessment_node(state: ValidationState) -> ValidationState:
            """Final assessment and report generation"""
            # Determine overall validity
            schema_valid = state["status"] in [ValidationStatus.SCHEMA_VALID, ValidationStatus.SEMANTIC_VALID, ValidationStatus.SEMANTIC_INVALID]
            semantic_valid = state["status"] == ValidationStatus.SEMANTIC_VALID
            
            state["is_valid"] = schema_valid and semantic_valid
            state["status"] = ValidationStatus.COMPLETE
            
            # Generate validation report
            state["validation_report"] = {
                "overall_valid": state["is_valid"],
                "schema_validation": {
                    "passed": len(state["schema_errors"]) == 0,
                    "errors": state["schema_errors"]
                },
                "semantic_validation": {
                    "passed": len(state["semantic_errors"]) == 0,
                    "errors": state["semantic_errors"]
                },
                "summary": self._generate_summary(state)
            }
            
            return state
        
        def should_continue_to_semantic(state: ValidationState) -> str:
            """Decide whether to continue to semantic validation"""
            if state["status"] == ValidationStatus.SCHEMA_VALID:
                return "semantic_validation"
            else:
                return "final_assessment"
        
        # Build the graph
        workflow = StateGraph(ValidationState)
        
        # Add nodes
        workflow.add_node("schema_validation", schema_validation_node)
        workflow.add_node("semantic_validation", semantic_validation_node)
        workflow.add_node("final_assessment", final_assessment_node)
        
        # Add edges
        workflow.set_entry_point("schema_validation")
        workflow.add_conditional_edges(
            "schema_validation",
            should_continue_to_semantic,
            {
                "semantic_validation": "semantic_validation",
                "final_assessment": "final_assessment"
            }
        )
        workflow.add_edge("semantic_validation", "final_assessment")
        workflow.add_edge("final_assessment", END)
        
        return workflow.compile()
    
    def _generate_summary(self, state: ValidationState) -> str:
        """Generate a human-readable summary of validation results"""
        if state["is_valid"]:
            return "JSON data is valid according to both schema and semantic rules."
        
        issues = []
        if state["schema_errors"]:
            issues.append(f"Schema validation failed: {'; '.join(state['schema_errors'])}")
        if state["semantic_errors"]:
            issues.append(f"Semantic validation failed: {'; '.join(state['semantic_errors'])}")
        
        return f"JSON data is invalid. Issues found: {' | '.join(issues)}"
    
    def validate_json(
        self,
        json_data: Dict[str, Any],
        schema: Dict[str, Any],
        custom_rules: List[str]
    ) -> Dict[str, Any]:
        """
        Validate JSON data against schema and custom rules
        
        Args:
            json_data: The JSON data to validate
            schema: JSON schema for structural validation
            custom_rules: List of custom semantic rules
            
        Returns:
            Validation report dictionary
        """
        initial_state = ValidationState(
            json_data=json_data,
            schema=schema,
            custom_rules=custom_rules,
            status=ValidationStatus.PENDING,
            schema_errors=[],
            semantic_errors=[],
            is_valid=False,
            validation_report={}
        )
        
        # Run the workflow
        final_state = self.workflow.invoke(initial_state)
        
        return final_state["validation_report"]

def create_sample_schema() -> Dict[str, Any]:
    """Create a sample JSON schema for testing"""
    return {
        "type": "object",
        "properties": {
            "user": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "minimum": 1},
                    "name": {"type": "string", "minLength": 1},
                    "email": {"type": "string", "format": "email"},
                    "age": {"type": "integer", "minimum": 0, "maximum": 150},
                    "roles": {
                        "type": "array",
                        "items": {"type": "string"},
                        "minItems": 1
                    }
                },
                "required": ["id", "name", "email", "age", "roles"]
            },
            "metadata": {
                "type": "object",
                "properties": {
                    "created_at": {"type": "string", "format": "date-time"},
                    "version": {"type": "string"}
                },
                "required": ["created_at", "version"]
            }
        },
        "required": ["user", "metadata"]
    }

def create_sample_rules() -> List[str]:
    """Create sample custom validation rules"""
    return [
        "User age must be reasonable for the assigned roles (e.g., admin role requires age >= 18)",
        "Email domain should be from a business domain (not personal email providers like gmail, yahoo)",
        "User name should not contain special characters or numbers",
        "At least one role must be assigned, and roles should be from: ['user', 'admin', 'moderator', 'guest']",
        "Version should follow semantic versioning format (e.g., 1.0.0)",
        "Created timestamp should not be in the future"
    ]

if __name__ == "__main__":
    # Example usage
    validator = JSONValidator()
    
    # Sample data
    sample_json = {
        "user": {
            "id": 123,
            "name": "John Doe",
            "email": "john.doe@company.com",
            "age": 30,
            "roles": ["admin", "user"]
        },
        "metadata": {
            "created_at": "2024-01-15T10:30:00Z",
            "version": "1.2.0"
        }
    }
    
    schema = create_sample_schema()
    rules = create_sample_rules()
    
    print("JSON Validation Example")
    print("=" * 50)
    print(f"JSON Data: {json.dumps(sample_json, indent=2)}")
    print(f"\nCustom Rules: {rules}")
    
    # Validate
    result = validator.validate_json(sample_json, schema, rules)
    
    print(f"\nValidation Result:")
    print(json.dumps(result, indent=2))
