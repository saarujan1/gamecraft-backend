import unittest
import json
import requests
from azure.cosmos import CosmosClient

class test_submit_game(unittest.TestCase):

    LOCAL_DEV_URL="http://localhost:7071/"
    PUBLIC_URL="https://gamecraft-backend.azurewebsites.net/submit_game?code=cPs-op-r7rAFOF_eKXg08jmTiwjRyN1s6gA_dOBKfp5lAzFuM4CODQ=="
    TEST_URL = PUBLIC_URL

    def test_player_register(self):
        
        payload = {'name': 'Luis', 'devName': 'UbiSoft', 'description': 'shooter', 'image': 'n/a'
                   ,'options': 'fire, down, up', 'roadmap': 'roadmap', 'sharePrice': '$2', 
                   'minThreshold': '10 votes', 'revenueSharing': '$5'
                   , }
        json_payload = json.dumps(payload)
        response = requests.post(self.TEST_URL, data=json_payload)
        print(response.text)

