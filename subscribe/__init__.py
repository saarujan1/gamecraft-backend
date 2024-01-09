import json
import logging
import os
import azure.functions as func
from azure.cosmos import CosmosClient

config = {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "AzureCosmosDBConnectionString": "AccountEndpoint=https://gamecraftdb.documents.azure.com:443/;AccountKey=g5pNMi2ICWXUuIpGAcSAwI9rRkxNHxQ9lgKa0ifSvAJR6QSl6t6C4GFRqwG5ogyXJyDSRzvQDFwbACDbvzlF0g==;",
    "DatabaseName": "gamecraftdata",
    "UserContainer": "users",
    "GameContainer": "games",
    "DeploymentURL": "https://gamecraftfunc.azurewebsites.net",
    "FunctionAppKey": "3LQBt84tTmZSvy-0SeVb6PbHH3a8-KudnjrvBebmysaSAzFutO8Gkg==",
    "BlobConnectionString": "DefaultEndpointsProtocol=https;AccountName=gamecraftstore;AccountKey=dONK8M0EDA1Jnw6124xIjvxlu8CO1f3oN9l6TbiAmMgksmlpeH86nR6G8ZIJwEoTepnJ75NuZ6R1+AStgwgetQ==;EndpointSuffix=core.windows.net"
}

# Initialize Cosmos client
MyCosmos = CosmosClient.from_connection_string(
    config['AzureCosmosDBConnectionString'])
PlayerDBProxy = MyCosmos.get_database_client(config['DatabaseName'])
game_db_proxy = MyCosmos.get_database_client(config['DatabaseName'])
UserContainerProxy = PlayerDBProxy.get_container_client(
    config['UserContainer'])
GameContainerProxy = game_db_proxy.get_container_client(
    config['GameContainer'])


def subscribe_user(username, game_id):
    user_query = f"SELECT * FROM c WHERE c.username = '{username}'"
    user_results = list(UserContainerProxy.query_items(
        query=user_query, enable_cross_partition_query=True))

    if not user_results:
        return {"result": False, "msg": f"User '{username}' not found."}

    # Check if the game ID exists in the game container
    game_query = f"SELECT * FROM c WHERE c.id = '{game_id}'"
    game_results = list(GameContainerProxy.query_items(
        query=game_query, enable_cross_partition_query=True))

    if not game_results:
        return {"result": False, "msg": f"Game ID '{game_id}' not found."}

    # return {"result": True, "msg": "User and Game ID exist."}

    game_document = game_results[0]
    subscribers = game_document.get('subscribers', [])

    if username not in subscribers:
        subscribers.append(username)
        game_document['subscribers'] = subscribers

        # Update the document in the game container
        GameContainerProxy.replace_item(item=game_document, body=game_document)

        return {"result": True, "msg": f"User '{username}' subscribed to Game ID '{game_id}'."}
    else:
        return {"result": False, "msg": f"User '{username}' is already subscribed to Game ID '{game_id}'."}


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        req_body = req.get_json()
        username = req_body.get('username')
        game_id = req_body.get('game_id')

        if not username or not game_id:
            raise ValueError(
                "Both 'username' and 'game_id' must be provided in the request body.")

        result = subscribe_user(username, game_id)

        return func.HttpResponse(json.dumps(result), status_code=200, mimetype='application/json')

    except ValueError as e:
        return func.HttpResponse(str(e), status_code=400)
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(str(e), status_code=500)
