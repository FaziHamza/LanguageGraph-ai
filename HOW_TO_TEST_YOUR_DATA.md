# How to Test Your Own Data with LangGraph JSON Validator

## 🚀 Quick Start - Testing Sample Files

I've created several sample files for you to test with:

### 1. Test with Valid Data
```bash
python main.py --file my_valid_data.json
```

### 2. Test with Invalid Semantic Data
```bash
python main.py --file my_invalid_data.json
```

### 3. Test with Schema Invalid Data
```bash
python main.py --file my_schema_invalid_data.json
```

## 📝 Sample Data Files Created

### `my_valid_data.json` - Should Pass All Validations
- Valid user with business email
- Proper age for admin role
- Correct version format
- Valid timestamp

### `my_invalid_data.json` - Should Fail Semantic Validation
- Name contains numbers and special characters
- Personal email (gmail.com)
- Age too young for admin role (15 years old)
- Future timestamp
- Invalid version format

### `my_schema_invalid_data.json` - Should Fail Schema Validation
- ID is string instead of number
- Empty name
- Invalid email format
- Negative age
- Empty roles array
- Missing required version field

## 🔧 Ways to Test Your Own Data

### Method 1: File Validation (Recommended)
1. Create a JSON file with your data
2. Run: `python main.py --file your_file.json`

### Method 2: Interactive Mode
1. Run: `python main.py --interactive`
2. Choose option 1 (Validate custom JSON)
3. Paste your JSON data
4. Select rule set to validate against

### Method 3: Show Test Data Examples
```bash
python main.py --show-test-data
```

### Method 4: Run Demo with All Test Cases
```bash
python main.py --demo
```

## 📋 JSON Schema Requirements

Your JSON data must follow this structure:

```json
{
  "user": {
    "id": 123,                    // Required: positive integer
    "name": "John Doe",           // Required: non-empty string
    "email": "john@company.com",  // Required: valid email format
    "age": 25,                    // Required: 0-150
    "roles": ["user", "admin"]    // Required: non-empty array of strings
  },
  "metadata": {
    "created_at": "2024-01-15T10:30:00Z",  // Required: ISO datetime
    "version": "1.2.0"                     // Required: string
  }
}
```

## 🎯 Business Rules Validated

The system checks these semantic rules:

1. **Age vs Role**: Admin role requires age >= 18
2. **Email Domain**: Should be business domain (not gmail, yahoo, etc.)
3. **Name Format**: Should not contain numbers or special characters
4. **Valid Roles**: Must be from ['user', 'admin', 'moderator', 'guest']
5. **Version Format**: Should follow semantic versioning (e.g., 1.2.0)
6. **Timestamp**: Should not be in the future

## 🔑 API Key Setup (For Full Validation)

To use the LLM-based semantic validation:

1. Get OpenAI API key from https://platform.openai.com/
2. Edit `.env` file:
   ```
   OPENAI_API_KEY=your_actual_api_key_here
   ```
3. Without API key, only schema validation works

## 🧪 Testing Examples

### Test Valid Data:
```bash
python main.py --file my_valid_data.json
```
Expected: ✅ Both schema and semantic validation pass

### Test Invalid Semantic Data:
```bash
python main.py --file my_invalid_data.json
```
Expected: ✅ Schema passes, ❌ Semantic validation fails

### Test Schema Invalid Data:
```bash
python main.py --file my_schema_invalid_data.json
```
Expected: ❌ Schema validation fails, semantic validation skipped

## 📊 Understanding Results

The validator returns a detailed report:

```json
{
  "overall_valid": false,
  "schema_validation": {
    "passed": true,
    "errors": []
  },
  "semantic_validation": {
    "passed": false,
    "errors": [
      "User age (15) is too young for admin role",
      "Email should be from business domain",
      "Name contains invalid characters"
    ]
  },
  "summary": "JSON data is invalid. Issues found: ..."
}
```

## 🎨 Create Your Own Test Data

1. Copy one of the sample files
2. Modify the values to test different scenarios
3. Run validation to see results

### Example Custom Data:
```json
{
  "user": {
    "id": 999,
    "name": "Your Name",
    "email": "your.email@yourcompany.com",
    "age": 30,
    "roles": ["user"]
  },
  "metadata": {
    "created_at": "2024-01-01T12:00:00Z",
    "version": "1.0.0"
  }
}
```

Save this as `my_custom_data.json` and test with:
```bash
python main.py --file my_custom_data.json
```

## 🔍 Troubleshooting

- **Import Errors**: Run `pip install -r requirements.txt`
- **API Key Issues**: Check `.env` file format
- **JSON Format Errors**: Validate JSON syntax first
- **File Not Found**: Ensure file path is correct

Happy testing! 🎉
