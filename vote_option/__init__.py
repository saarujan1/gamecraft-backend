import json
import azure.functions as func
from azure.cosmos import CosmosClient
import os

# Setup CosmosDB client
MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
GameContainerProxy = PlayerDBProxy.get_container_client(os.environ['GameContainer'])

def vote_option(req: func.HttpRequest) -> func.HttpResponse:

    try:
        request_body = req.get_json()
        game_id = request_body['game_id']
        option_index = request_body['option_index']  # Assuming this is the index of the option
        vote_type = request_body['vote_type']

        game_item = GameContainerProxy.read_item(item=game_id, partition_key=game_id)
        
        if 0 <= option_index < len(game_item['options']):
            if vote_type == 'upvote':
                game_item['option_votes'][option_index]['upvotes'] += 1
            elif vote_type == 'downvote':
                game_item['option_votes'][option_index]['downvotes'] += 1
        else:
            return func.HttpResponse(body=json.dumps({"result": False, "msg": "Invalid option index"}))

        GameContainerProxy.replace_item(item=game_item, body=game_item)
        return func.HttpResponse(body=json.dumps({"result": True, "msg": "Option vote updated successfully"}))

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Failed to process option vote"}))
