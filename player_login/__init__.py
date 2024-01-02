import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import os

# Initialize Cosmos client
MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
PlayerContainerProxy = PlayerDBProxy.get_container_client(os.environ['PlayerContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing login request')
    player = req.get_json()

    try:
        # Search using userame and password
        query = "SELECT * FROM player WHERE player.username = @username AND player.password = @password"
        parameters = [
            {"name": "@username", "value": player["username"]},
            {"name": "@password", "value": player["password"]}
        ]
        
        # Run query against the Cosmos DB container
        query_result = list(PlayerContainerProxy.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True
        ))
        
        # Check if any results are returned
        if query_result:
            # Login successful
            return func.HttpResponse(body=json.dumps({"result": True, "msg": "OK"}))
        else:
            # Login failed
            return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username or password incorrect"}))
    except Exception as e:
        return