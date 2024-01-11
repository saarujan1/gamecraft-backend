import json
import azure.functions as func
from azure.cosmos import CosmosClient
import os

# Setup CosmosDB client
MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
GameContainerProxy = PlayerDBProxy.get_container_client(os.environ['GameContainer'])

def vote_game(req: func.HttpRequest) -> func.HttpResponse:

    try:
        request_body = req.get_json()
        game_id = request_body['game_id']
        vote_type = request_body['vote_type']

        game_item = GameContainerProxy.read_item(item=game_id, partition_key=game_id)
        
        if vote_type == 'upvote':
            game_item['game_votes']['upvotes'] += 1
        elif vote_type == 'downvote':
            game_item['game_votes']['downvotes'] += 1

        GameContainerProxy.replace_item(item=game_item, body=game_item)
        return func.HttpResponse(body=json.dumps({"result": True, "msg": "Vote updated successfully"}))

    except Exception as e:
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Failed to process vote"}))
