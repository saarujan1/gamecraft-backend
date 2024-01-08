import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
from azure.cosmos.exceptions import CosmosHttpResponseError
import os

MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
UserContainerProxy = PlayerDBProxy.get_container_client(os.environ['UserContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Registering user')

    user = req.get_json()

    user['created_games'] = '[]'
    user['subscribed_games'] = '[]'

    print(user)
    
    if (len(user["username"]) < 4 or len(user["username"]) > 14):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username less than 4 characters or more than 14 characters"}))
    elif (len(user["password"]) < 10 or len(user["password"]) > 20):
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Password less than 10 characters or more than 20 characters"}))
    
    query = "SELECT * FROM users WHERE users.username = @username"
    parameters = [{"name": "@username", "value": user["username"]}]
    items = list(UserContainerProxy.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    ))

    if items:
        # Check username already exists
        return func.HttpResponse(body=json.dumps({"result": False, "msg": "Username already exists"}))

    try:
        UserContainerProxy.create_item(body=user, enable_automatic_id_generation=True)
        body_json = json.dumps({"result": True, "msg": "OK"})
        return func.HttpResponse(body=body_json)

    except CosmosHttpResponseError as e:
        return