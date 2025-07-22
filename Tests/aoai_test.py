import sys
import os
import json

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Load environment variables from local.settings.json
def load_local_settings():
    """Load environment variables from local.settings.json"""
    settings_path = os.path.join(parent_dir, "local.settings.json")
    if os.path.exists(settings_path):
        with open(settings_path, 'r') as f:
            settings = json.load(f)
            for key, value in settings.get("Values", {}).items():
                os.environ[key] = value
        print("Loaded environment variables from local.settings.json")
    else:
        print("local.settings.json not found")

# Load settings before importing function_app
load_local_settings()

# Now we can import from function_app
from function_app import execute_llm_call

def test_llm_call():
    """Test the execute_llm_call function"""
    try:
        prompt = "What is the capital of France?"
        print("Testing execute_llm_call with a sample prompt...")
        print(f"Prompt: {prompt}")
        result = execute_llm_call(prompt)
        print("LLM call executed successfully.")
        print(f"Response: {result}")
    except Exception as e:
        print(f"Error executing LLM call: {e}")
            
    except Exception as e:
        print(f"Error executing query: {e}")

if __name__ == "__main__":
    test_llm_call()