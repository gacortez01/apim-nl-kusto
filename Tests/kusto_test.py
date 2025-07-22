import sys
import os

# Add the parent directory to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

# Now we can import from function_app
from function_app import execute_kusto_query

def test_kusto_query():
    """Test the execute_kusto_query function"""
    try:
        print("Testing execute_kusto_query with 'GetTenantVersions'...")
        result = execute_kusto_query("GetTenantVersions")
        
        print(f"Query executed successfully. Found {len(result)} rows.")
        for i, row in enumerate(result):
            print(f"Row {i + 1}: {row}")
            
    except Exception as e:
        print(f"Error executing query: {e}")

if __name__ == "__main__":
    test_kusto_query()