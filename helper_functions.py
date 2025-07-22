from azure.kusto.data import KustoClient
from utils import Utils
import os
from openai import AzureOpenAI

CONFIG_FILE_NAME = "config.json"

def generate_kusto_query_from_nl(prompt: str) -> str:
    """
    Placeholder function to generate Kusto query from natural language prompt.
    
    Args:
        prompt (str): Natural language description of the query
        
    Returns:
        str: Generated Kusto query
    """
    # TODO: Implement AI/LLM integration to convert natural language to Kusto
    # This could integrate with Azure OpenAI, OpenAI API, or other language models
    # For now, return a placeholder query with the prompt
    
    logging.info(f"Generating Kusto query for prompt: {prompt}")
    
    # Placeholder implementation - return a sample query
    placeholder_query = f"""
// Generated from prompt: {prompt}
// TODO: Replace with actual query generation logic
GetTenantVersions
| summarize count() by version
| order by version desc
"""
    
    return placeholder_query.strip()

def get_prompt_from_request(req: func.HttpRequest) -> str:
    """
    Extracts the 'prompt' parameter from the HTTP request.
    
    Args:
        req (func.HttpRequest): The HTTP request object
        
    Returns:
        str: The prompt string if found, otherwise None
    """
    prompt = req.params.get('prompt')
    if not prompt:
        try:
            req_body = req.get_json()
            if req_body:
                prompt = req_body.get('prompt')
        except ValueError as e:
            logging.error(f"Failed to parse JSON body: {e}")
            return None
    return prompt

def execute_llm_call(prompt: str) -> str:
    if not prompt:
        raise ValueError("Prompt cannot be empty")

    client = AzureOpenAI(
        azure_endpoint=os.environ.get("AZURE_OPENAI_ENDPOINT"),
        api_version="2025-01-01-preview",
        api_key=os.environ.get("AI_FOUNDRY_API_KEY")
    )

    # Call the LLM with the provided prompt
    response = client.chat.completions.create(
        model=os.environ.get("AZURE_OPENAI_DEPLOYMENT_NAME"),
        messages=[{"role": "user", "content": prompt}],
    )

    logging.info(f"LLM response: {response.choices[0].message.content}")
    return response.choices[0].message.content

def execute_kusto_query(query: str) -> dict:
    """
    Placeholder function to execute Kusto query against Azure Data Explorer.
    
    Args:
        query (str): Kusto query to execute
        
    Returns:
        dict: Query results and metadata
    """
    # TODO: Implement actual Kusto query execution
    # This should connect to Azure Data Explorer using:
    # - Azure SDK for Python (azure-kusto-data)
    # - Managed Identity for authentication
    # - Proper error handling and retry logic

    config_dict = Utils.load_configs(CONFIG_FILE_NAME)
    kusto_uri = config_dict["kustoUri"]
    database_name = config_dict["databaseName"]
    authentication_mode = config_dict["authenticationMode"]

    kusto_connection_string = Utils.Authentication.generate_connection_string(kusto_uri, authentication_mode)
    
    #Handle Null here
    if not kusto_connection_string:
        Utils.error_handler("Connection String error. Please validate your configuration file.")
    else:
        with KustoClient(kusto_connection_string) as kusto_client:
            logging.info(f"Executing Kusto query: {query[:100]}...")
            response = kusto_client.execute(database_name, query)
            logging.info("Query executed successfully.")
            logging.debug(f"Query response: {response}")
            # Convert KustoResultTable to list of dicts for JSON serialization
            result_table = response.primary_results[0]
            columns = [col.column_name for col in result_table.columns]
            rows = [dict(zip(columns, row)) for row in result_table.rows]
            return rows
        