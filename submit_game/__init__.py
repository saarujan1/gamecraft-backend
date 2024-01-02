import json
import logging
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
import requests
import uuid
import os

# Initialize Cosmos DB client
cosmos_client = CosmosClient.from_connection_string(os.environ['AzureCosmosDBConnectionString'])
PlayerDBProxy = cosmos_client.get_database_client(os.environ['Database'])
PlayerContainerProxy = PlayerDBProxy.get_container_client(os.environ['PlayerContainer'])
PromptContainerProxy = PlayerDBProxy.get_container_client(os.environ['PromptContainer'])

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing prompt creation request')

    try:
        request_data = req.get_json()

        # Validate player existence
        if not is_player_exists(request_data['username']):
            return func.HttpResponse(json.dumps({"result": False, "msg": "Player does not exist"}))

        # Validate prompt length
        prompt_text = request_data['text']
        if len(request_data['text']) < 15 or len(prompt_text) > 80:
            return func.HttpResponse(json.dumps({"result": False, "msg": "Prompt less than 15 characters or more than 80 characters"}))
        
        # Detect language
        detected_languages = detect_language(prompt_text)
        primary_language = detected_languages[0]  # First reslut = main language
        if primary_language['language'] not in ['en', 'es', 'it', 'sv', 'ru', 'id', 'bg', 'zh-Hans']:
            return func.HttpResponse(json.dumps({"result": False, "msg": "Unsupported language"}))
        if primary_language['score'] < 0.3:
            return func.HttpResponse(json.dumps({"result": False, "msg": "Unsupported language"}))

        # Translate text
        translated_texts = translate_text(prompt_text, primary_language['language'])

        # Insert prompt into Cosmos DB
        create_prompt(request_data['username'], request_data['text'], translated_texts, primary_language['language'])
        return func.HttpResponse(json.dumps({"result": True, "msg": "OK"}))

    except Exception as e:
        return {"result": False, "msg": "BLA"}

# Function to check if player exists
def is_player_exists(username):
    query = "SELECT * FROM player WHERE player.username = @username"
    parameters = [{"name": "@username", "value": username}]
    items = list(PlayerContainerProxy.query_items(query=query, parameters=parameters, enable_cross_partition_query=True))
    return len(items) > 0

def detect_language(text):
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/detect'
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': "0144b604f2354054aef9dbaa784db5d6",
        'Ocp-Apim-Subscription-Region': "uksouth",
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    params = {
        'api-version': '3.0',
    }

    body = [{'text': text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    return response.json()

# Function to translate text
def translate_text(text, from_lang):
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/translate'
    constructed_url = endpoint + path

    # List of target languages for translation
    target_languages = ['en', 'es', 'it', 'sv', 'ru', 'id', 'bg', 'zh-Hans']
    target_languages.remove(from_lang)  # Remove the source language from the list

    params = {
        'api-version': '3.0',
        'from': from_lang,
        'to': target_languages
    }

    headers = {
        'Ocp-Apim-Subscription-Key': "0144b604f2354054aef9dbaa784db5d6",
        'Ocp-Apim-Subscription-Region': "uksouth",
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': text}]

    response = requests.post(constructed_url, params=params, headers=headers, json=body)
    return response.json()


def create_prompt(username, original_text, translated_texts, original_language):
    # Initialize with original text
    texts = [{"language": original_language, "text": original_text}]

    # Add translations, including English if necessary
    for translation in translated_texts:
        for text in translation['translations']:
            if text["to"] != original_language or (original_language != 'en' and text["to"] == 'en'):
                texts.append({"language": text["to"], "text": text["text"]})

    prompt_item = {"username": username, "texts": texts}

    try:
        # Insert into container
        PromptContainerProxy.create_item(prompt_item, enable_automatic_id_generation=True)
    except Exception as e:
        return