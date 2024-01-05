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

#takes an image, uploads it to the blob storage, returns the id of the blob storage
def main(req: func.HttpRequest) -> func.HttpResponse:

    logging.info('Uploading image')

    image = req.get_body()

    blob_name = str(uuid.uuid4())

    blob_client = ServiceClient.get_blob_client("items", blob_name)

    stream = io.BytesIO(image)

    try:
        blob_client.upload_blob(stream)
        return func.HttpResponse(json.dumps({"result": True, "name": blob_name}))
    except Exception as e:
        return func.HttpResponse(json.dumps({"result": False, "msg": "Image upload failed"}))


