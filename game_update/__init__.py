import json
import logging
import azure.functions as func
from azure.cosmos import exceptions, CosmosClient, PartitionKey
import os

# Initialize Cosmos DB client
cosmos_client = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
game_db_proxy = cosmos_client.get_database_client(os.environ['DatabaseName'])
game_container_proxy = game_db_proxy.get_container_client(os.environ['GameContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Updating game')

    game = req.get_json()

    return func.HttpResponse(status_code=200)

    try:

        # Query to get selected game
        query = "SELECT * from games where id = " + str(game['id'])

        old_game = list(game_container_proxy.query_items(query=query, enable_cross_partition_query=True))

        # if the updated json doesn't have the same keys then it won't work
        if old_game[0].keys() == game.keys():
            # replace game with updated data
            game_container_proxy.replace_item(item=old_game[0], body=game)

            return func.HttpResponse(json.dumps(game, ensure_ascii=False, status_code=200))
        else:
            raise Exception("Updated game in wrong format")

    except Exception as e:
        logging.error(f"Exception: {e}")
        return func.HttpResponse(json.dumps({"error": "An error occurred"}), status_code=500)
