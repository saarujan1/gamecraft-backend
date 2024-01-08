import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import os
import uuid

# Initialize Cosmos DB client
cosmos_client = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
GameDBProxy = cosmos_client.get_database_client(os.environ['DatabaseName'])
GameContainerProxy = GameDBProxy.get_container_client(os.environ['GameContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing game submission request')

    game = req.get_json()

    try:
        name = game['name']
        devName = game['devName']
        description = game['description']
        image = game['image']
        options = game['options']
        roadmap = game['roadmap']
        sharePrice = game['sharePrice']
        minThreshold = game['minThreshold']
        revenueSharing = game['revenueSharing']

        # Validations
        if len(description) < 15:
            return func.HttpResponse(json.dumps({"result": False, "msg": "Description should be at least 15 letters long"}), status_code=400)

        if sharePrice <= 0.1:
            return func.HttpResponse(json.dumps({"result": False, "msg": "Share price must be above 0.1"}), status_code=400)

        if revenueSharing <= 10:
            return func.HttpResponse(json.dumps({"result": False, "msg": "Revenue sharing must be above 10"}), status_code=400)

        if len(set(options)) != len(options):
            return func.HttpResponse(json.dumps({"result": False, "msg": "Options must be unique"}), status_code=400)

        # Check if the game name already exists
        query = "SELECT * FROM c WHERE c.name = @name"
        items = list(GameContainerProxy.query_items(
            query=query,
            parameters=[{"name": "@name", "value": name}],
            enable_cross_partition_query=True
        ))

        if items:
            return func.HttpResponse(json.dumps({"result": False, "msg": "Game name already exists"}), status_code=400)

        game_document = {
            "id": str(uuid.uuid4()),
            "name": name, 
            "devName": devName, 
            "description": description,
            "image": image,
            "subscribers": [],
            "options": options,
            "roadmap": roadmap,
            "sharePrice": sharePrice,
            "minThreshold": minThreshold,
            "revenueSharing": revenueSharing
        }

        # Insert the game document into the Cosmos DB container
        GameContainerProxy.create_item(game_document)
        return func.HttpResponse(json.dumps({"result": True, "msg": "Game submitted successfully"}))

    except Exception as e:
        return func.HttpResponse(json.dumps({"result": False, "msg": str(e)}), status_code=500)
