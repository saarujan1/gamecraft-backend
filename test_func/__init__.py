import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import os

# Initialize Cosmos client
MyCosmos = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDBProxy = MyCosmos.get_database_client(os.environ['DatabaseName'])
UserContainerProxy = PlayerDBProxy.get_container_client(os.environ['UserContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:

        return func.HttpResponse(body="hello world")
