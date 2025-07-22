
from function_app import execute_kusto_query

result = execute_kusto_query("GetTenantVersions")

for row in result[0]:
    print(row)