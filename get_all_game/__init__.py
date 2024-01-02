import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import os

# Initialize Cosmos DB client
cosmos_client = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
game_db_proxy = cosmos_client.get_database_client(os.environ['DatabaseName'])
game_container_proxy = game_db_proxy.get_container_client(os.environ['GameContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing get all games request')
    
    try:
        # Query to select all games from the Cosmos DB
        query = "SELECT * FROM c"
        
        # Fetch all game data
        games_data = list(game_container_proxy.query_items(query=query, enable_cross_partition_query=True))

        # Format the response as needed
        formatted_games = [format_game_data(game) for game in games_data]

        return func.HttpResponse(json.dumps(formatted_games, ensure_ascii=False))

    except Exception as e:
        logging.error(f"Exception: {e}")
        return func.HttpResponse(json.dumps({"error": "An error occurred"}), status_code=500)

def format_game_data(game):
    # Here you can format the game data or extract only the necessary fields
    # For now, we'll return the game as is
    return game