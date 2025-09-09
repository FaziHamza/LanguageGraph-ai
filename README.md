# LangGraph JSON Rules Validator

A comprehensive JSON validation system built with LangGraph that combines traditional schema validation with AI-powered semantic rule validation using Large Language Models (LLMs).

## Features

- **Dual Validation Approach**: Combines JSON Schema validation with LLM-based semantic validation
- **LangGraph Workflow**: Uses LangGraph to orchestrate the validation process through a structured workflow
- **Flexible Rule System**: Supports custom business rules, technical rules, and semantic validation
- **Multiple Interfaces**: Command-line interface, interactive mode, and programmatic API
- **Comprehensive Testing**: Includes extensive test data and edge cases
- **Detailed Reporting**: Provides detailed validation reports with specific error messages

## Architecture

The system uses a LangGraph workflow with three main nodes:

1. **Schema Validation Node**: Validates JSON structure against JSON Schema
2. **Semantic Validation Node**: Uses LLM to validate against custom business rules
3. **Final Assessment Node**: Generates comprehensive validation report

```
[JSON Input] → [Schema Validation] → [Semantic Validation] → [Final Assessment] → [Report]
                      ↓                        ↓
                [Schema Errors]        [Semantic Errors]
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd LanguageGraph-ai
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Usage

### Command Line Interface

Run the demo:
```bash
python main.py --demo
```

Interactive mode:
```bash
python main.py --interactive
```

Validate a JSON file:
```bash
python main.py --file data.json
```

Show test data examples:
```bash
python main.py --show-test-data
```

### Programmatic Usage

```python
from json_validator import JSONValidator, create_sample_schema
from test_data import get_business_rules

# Initialize validator
validator = JSONValidator()

# Define your JSON data
json_data = {
    "user": {
        "id": 123,
        "name": "John Doe",
        "email": "john@company.com",
        "age": 30,
        "roles": ["admin"]
    },
    "metadata": {
        "created_at": "2024-01-15T10:30:00Z",
        "version": "1.0.0"
    }
}

# Define schema and rules
schema = create_sample_schema()
rules = get_business_rules()

# Validate
result = validator.validate_json(json_data, schema, rules)
print(result)
```

## Validation Rules

The system supports three types of validation rules:

### 1. Business Rules
- User age requirements for roles
- Email domain restrictions
- Name format validation
- Role assignments
- Version format requirements
- Timestamp validation

### 2. Technical Rules
- Data type validation
- Format compliance (RFC standards)
- Range validation
- Uniqueness constraints
- Array validation

### 3. Custom Rules
- User-defined validation logic
- Context-specific requirements
- Domain-specific constraints

## Example Validation Rules

```python
business_rules = [
    "User age must be reasonable for assigned roles (admin requires age >= 18)",
    "Email domain should be from business domains (not gmail, yahoo, etc.)",
    "User name should not contain special characters or numbers",
    "Roles must be from: ['user', 'admin', 'moderator', 'guest']",
    "Version should follow semantic versioning format",
    "Created timestamp should not be in the future"
]
```

## Test Data

The system includes comprehensive test data:

- **Valid Data**: Passes all validations
- **Invalid Schema Data**: Fails structural validation
- **Invalid Semantic Data**: Passes schema but fails business rules
- **Edge Cases**: Boundary conditions and special scenarios

## Configuration

### Environment Variables

- `OPENAI_API_KEY`: Required for LLM-based semantic validation
- `ANTHROPIC_API_KEY`: Optional, for Anthropic models
- `GOOGLE_API_KEY`: Optional, for Google models

### Customization

You can customize:

- **JSON Schema**: Define your own structural validation rules
- **Validation Rules**: Create custom business and semantic rules
- **LLM Model**: Change the model used for semantic validation
- **Workflow**: Modify the LangGraph workflow for different validation flows

## API Reference

### JSONValidator Class

#### `__init__(openai_api_key: Optional[str] = None)`
Initialize the validator with optional API key.

#### `validate_json(json_data: Dict, schema: Dict, custom_rules: List[str]) -> Dict`
Validate JSON data against schema and custom rules.

**Parameters:**
- `json_data`: The JSON data to validate
- `schema`: JSON schema for structural validation
- `custom_rules`: List of custom semantic rules

**Returns:**
- Validation report dictionary with detailed results

### Validation Report Structure

```python
{
    "overall_valid": bool,
    "schema_validation": {
        "passed": bool,
        "errors": List[str]
    },
    "semantic_validation": {
        "passed": bool,
        "errors": List[str]
    },
    "summary": str
}
```

## Examples

### Valid JSON Example

```json
{
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
```

### Invalid JSON Example (Semantic Issues)

```json
{
    "user": {
        "id": 456,
        "name": "User123!@#",
        "email": "user@gmail.com",
        "age": 16,
        "roles": ["admin", "invalid_role"]
    },
    "metadata": {
        "created_at": "2025-12-31T23:59:59Z",
        "version": "invalid.version.format"
    }
}
```

## Error Handling

The system provides detailed error messages for:

- Schema validation failures
- Semantic rule violations
- LLM communication errors
- JSON parsing errors
- Configuration issues

## Performance Considerations

- Schema validation is fast and runs first
- Semantic validation uses LLM calls (slower but more intelligent)
- Failed schema validation skips semantic validation for efficiency
- Caching can be implemented for repeated validations

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Dependencies

- `langgraph`: Workflow orchestration
- `langchain`: LLM integration
- `langchain-openai`: OpenAI integration
- `jsonschema`: JSON schema validation
- `pydantic`: Data validation
- `python-dotenv`: Environment variable management

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure `OPENAI_API_KEY` is set in your `.env` file
2. **Import Errors**: Install all dependencies with `pip install -r requirements.txt`
3. **LLM Timeout**: Check your internet connection and API key validity
4. **Schema Errors**: Validate your JSON schema format

### Debug Mode

Enable debug logging by setting environment variable:
```bash
export DEBUG=1
python main.py --demo
```

## Future Enhancements

- Support for additional LLM providers
- Web interface
- Batch validation
- Rule caching
- Performance metrics
- Custom workflow definitions
- Integration with CI/CD pipelines
