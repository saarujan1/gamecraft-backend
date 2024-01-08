import io
import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import uuid

# Initialize Cosmos DB client
cosmos_client = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
GameDBProxy = cosmos_client.get_database_client(os.environ['DatabaseName'])
GameContainerProxy = GameDBProxy.get_container_client(os.environ['GameContainer'])
ServiceClient = BlobServiceClient.from_connection_string(os.environ['BlobConnectionString'])


# returns and image uri + sas token
def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Getting image url')



    blob_client = ServiceClient.get_blob_client("images", '5')



    try:
        image = blob_client.download_blob()
        return func.HttpResponse(body=image.read(), status_code=200)
    except Exception as e:
        return func.HttpResponse(json.dumps({"result": False, "msg": "Image upload failed"}), status_code=400)


