import logging
import azure.functions as func
from function_app import execute_kusto_query

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    command = "GetTenantVersions |distinct serviceName"
    result = execute_kusto_query(command)

    for i, row in enumerate(result["primary_result"]):
         logging.info(f"Row {i + 1}: {row}")
