import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import os

# Initialize Cosmos DB client
cosmos_client = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
GameDBProxy = cosmos_client.get_database_client(os.environ['DatabaseName'])
GameContainerProxy = GameDBProxy.get_container_client(os.environ['GameContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing game submission request')

    game = req.get_json()

    name = game['name']
    devName = game['devName']
    description = game['description']
    image = game['image']
    options = game['options']
    roadmap = game['roadmap']
    sharePrice = game['sharePrice']
    minThreshold = game['minThreshold']
    revenueSharing = game['revenueSharing']

    try:

    # VALIDATIONS NEED TO BE DONE FOR DATA TYPE 
        
        
        
        game_document = {
            "name" : name, 
            "devName" : devName, 
            "description": description,
            "image": image,
            "options": options,
            "roadmap": roadmap,
            "options": options,
            "roadmap": roadmap,
            "sharePrice" : sharePrice,
            "minThreshold" : minThreshold,
            "revenueSharing" : revenueSharing
        }

        # Insert the game document into the Cosmos DB container
        GameContainerProxy.create_item(game_document, enable_automatic_id_generation=True)
        return func.HttpResponse(json.dumps({"result": True, "msg": "Game submitted successfully"}))
    
    except:
        return