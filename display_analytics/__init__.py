import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import os

# Initialize Cosmos DB client
cosmos_client = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
player_db_proxy = cosmos_client.get_database_client(os.environ['DatabaseName'])
player_container_proxy = player_db_proxy.get_container_client(os.environ['PlayerContainer'])
prompt_container_proxy = player_db_proxy.get_container_client(os.environ['PromptContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing get prompts request')
    
    try:
        request_data = req.get_json()
        players = request_data.get('players', [])
        language = request_data.get('language', '')

        if not players:
            return func.HttpResponse(json.dumps([])) # Returns empty list if no players provided

        # Construct the query to handle multiple players
        query = "SELECT c.id, c.username, t.text FROM c JOIN t IN c.texts WHERE ARRAY_CONTAINS(@players, c.username) AND t.language = @language"
        parameters = [{"name": "@players", "value": players}, {"name": "@language", "value": language}]
        
        # Fetch prompts
        prompts = list(prompt_container_proxy.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))

        # Format the response
        formatted_prompts = []
        for prompt in prompts:
            formatted_prompts.append({"id": prompt['id'], "text": prompt['text'], "username": prompt['username']})

        return func.HttpResponse(json.dumps(formatted_prompts, ensure_ascii=False))

    except Exception as e:
        return
