import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError
import os

MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDBProxy = MyCosmos.get_database_client(os.environ['Database'])
PlayerContainerProxy = PlayerDBProxy.get_container_client(os.environ['PlayerContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Registering player')

    player = req.get_json()
    
    if (len(player["username"]) < 4 or len(player["username"]) > 14):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username less than 4 characters or more than 14 characters"}))
    elif (len(player["password"]) < 10 or len(player["password"]) > 20):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Password less than 10 characters or more than 20 characters"}))
    
    query = "SELECT * FROM player WHERE player.username = @username"
    parameters = [{"name": "@username", "value": player["username"]}]
    items = list(PlayerContainerProxy.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    if items:
        # Check username already exists
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username already exists"}))

    try:
        player['games_played'] = 0
        player['total_score'] = 0
        PlayerContainerProxy.create_item(body=player, enable_automatic_id_generation=True)
        body_json = json.dumps({"result": True, "msg": "OK"})
        return func.HttpResponse(body=body_json)

    except CosmosHttpResponseError as e:
        return
