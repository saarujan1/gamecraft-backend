import io
import json
import logging
import os
import uuid

import azure.functions as func
from azure.cosmos import CosmosClient
from azure.storage.blob import BlobServiceClient

# Initialize Cosmos DB client
cosmos_client = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
GameDBProxy = cosmos_client.get_database_client(os.environ['DatabaseName'])
GameContainerProxy = GameDBProxy.get_container_client(os.environ['GameContainer'])
ServiceClient = BlobServiceClient.from_connection_string(os.environ['BlobConnectionString'])

# takes an image, uploads it to the blob storage, returns the id of the blob storage
def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Uploading image')

    image = req.files['file']

    blob_name = str(uuid.uuid4())

    blob_client = ServiceClient.get_blob_client("images", blob_name)




    try:
        blob_client.upload_blob(image)
        return func.HttpResponse(json.dumps({"result": True, "uri": blob_client.url}))
    except Exception as e:
        return func.HttpResponse(json.dumps({"result": False, "msg": "Image upload failed"}))


