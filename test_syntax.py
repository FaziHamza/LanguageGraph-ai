"""
Simple syntax validation test for the JSON validator
"""

import ast
import sys

def check_syntax(filename):
    """Check if a Python file has valid syntax"""
    try:
        with open(filename, 'r') as f:
            source = f.read()
        
        # Parse the AST to check syntax
        ast.parse(source)
        print(f"✓ {filename}: Syntax is valid")
        return True
    except SyntaxError as e:
        print(f"✗ {filename}: Syntax error at line {e.lineno}: {e.msg}")
        return False
    except Exception as e:
        print(f"✗ {filename}: Error reading file: {e}")
        return False

def main():
    """Test all Python files for syntax validity"""
    files_to_check = [
        'json_validator.py',
        'test_data.py',
        'main.py'
    ]
    
    print("LangGraph JSON Validator - Syntax Check")
    print("=" * 50)
    
    all_valid = True
    for filename in files_to_check:
        if not check_syntax(filename):
            all_valid = False
    
    print("\n" + "=" * 50)
    if all_valid:
        print("✓ All files have valid Python syntax!")
        print("\nTo run the application:")
        print("1. Install Python 3.8+ from https://python.org")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Set up your .env file with OPENAI_API_KEY")
        print("4. Run: python main.py --demo")
    else:
        print("✗ Some files have syntax errors that need to be fixed")
    
    return 0 if all_valid else 1

if __name__ == "__main__":
    sys.exit(main())
