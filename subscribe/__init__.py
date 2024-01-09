import json
import logging
import os
import azure.functions as func
from azure.cosmos import CosmosClient

# Initialize Cosmos client
MyCosmos = CosmosClient.from_connection_string(
    os.environ['AzureCosmosDBConnectionString'])
PlayerDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
game_db_proxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
UserContainerProxy = PlayerDBProxy.get_container_client(
    os.environ['UserContainer'])
GameContainerProxy = game_db_proxy.get_container_client(
    os.environ['GameContainer'])


def subscribe_user(username, game_id):
    # Retrieve user document from Cosmos DB
    user_query = f"SELECT * FROM c WHERE c.username = '{username}'"
    user_results = list(UserContainerProxy.query_items(
        query=user_query, enable_cross_partition_query=True))

    if not user_results:
        return {"result": False, "msg": f"User '{username}' not found."}

    user = user_results[0]

    # Check if the game is already subscribed
    if 'subscribed_games' in user and game_id in user['subscribed_games']:
        return {"result": False, "msg": f"User '{username}' is already subscribed to the game '{game_id}'."}

    # Update the game document with the subscriber information
    game_query = f"SELECT * FROM c WHERE c.game_id = '{game_id}'"
    game_results = list(GameContainerProxy.query_items(
        query=game_query, enable_cross_partition_query=True))

    if game_results:
        game = game_results[0]
        if 'subscribers' not in game:
            game['subscribers'] = []
        game['subscribers'].append(username)
        GameContainerProxy.upsert_item(game)

    # Add the game to the list of subscribed games in the user document
    if 'subscribed_games' not in user:
        user['subscribed_games'] = []
    user['subscribed_games'].append(game_id)

    # Update the user document in Cosmos DB
    UserContainerProxy.upsert_item(user)

    return {"result": True, "msg": "OK"}


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
        return func.HttpResponse("An error occurred while processing the request.", status_code=500)
