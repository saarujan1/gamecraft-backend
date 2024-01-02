import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import os

# Initialize Cosmos DB client
cosmos_client = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
GameDBProxy = cosmos_client.get_database_client(os.environ['Database'])
GameContainerProxy = GameDBProxy.get_container_client(os.environ['GameContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing game submission request')

    try:
        request_data = req.get_json()
        
        #check name is string, devName is string, description is string etc etc

        # If all validations pass, create and insert the game into the Cosmos DB
        create_game(request_data)
        return func.HttpResponse(json.dumps({"result": True, "msg": "Game submitted successfully"}))

    except Exception as e:
        return func.HttpResponse(json.dumps({"result": False, "msg": str(e)}), status_code=500)

def create_game(game_data):
    # Construct the game document from the request data
    # You might want to generate a unique 'gameID' if it's not provided in the request data.
    game_document = {
        # Populate this dictionary with the game data, adhering to your specification.
    }

    # Insert the game document into the Cosmos DB container
    GameContainerProxy.create_item(game_document)