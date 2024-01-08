import os
import unittest
import json
import requests
from azure.cosmos import CosmosClient

# Define the test class for submitting games


local = True

LOCALHOST = 'http://localhost:7071/'

KEY = "3LQBt84tTmZSvy-0SeVb6PbHH3a8-KudnjrvBebmysaSAzFutO8Gkg=="

test_game1 = {
    'name': 'LuisShooter2345',
    'devName': 'UbiSoft',
    'description': 'shooter that takes place in chicago',
    'image': 'n/a',
    'options': ["fire", "small", "down"],
    'roadmap': 'roadmap',
    'sharePrice': 2,
    'minThreshold': '10 votes',
    'revenueSharing': 12,
}

test_game2 = {
    'name': 'LuisShooter234',
    'devName': 'UbiSof',
    'description': 'shooter that takes place in chicag',
    'image': 'n/',
    'options': ["fire", "small"],
    'roadmap': 'roadma',
    'sharePrice': 1,
    'minThreshold': '12 votes',
    'revenueSharing': 15,
}


class TestUserRegister(unittest.TestCase):
    if local:
        TEST_URL = LOCALHOST + 'user/register'
    else:
        TEST_URL = "https://gamecraftfunc.azurewebsites.net/user/register"

    def test_user_register(self):
        payload = {
            'username': 'saarujan555',
            'password': 'password123',
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Functions-Key': KEY
        }
        json_payload = json.dumps(payload)
        response = requests.get(self.TEST_URL, data=json_payload, headers=headers)  # Use POST for login
        print(response.json())
        self.assertEqual(response.status_code, 200)

        # More assertions can be added here based on the expected response


class TestUserLogin(unittest.TestCase):
    if local:
        TEST_URL = LOCALHOST + 'user/login'
    else:
        TEST_URL = "https://gamecraftfunc.azurewebsites.net/user/login"

    def test_user_login(self):
        payload = {
            'username': 'saarujan',
            'password': 'password123',
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Functions-Key': KEY
        }
        json_payload = json.dumps(payload)
        response = requests.get(self.TEST_URL, data=json_payload, headers=headers)  # Use POST for login
        self.assertEqual(response.status_code, 200)


# Define the test class for submitting games
class TestSubmitGame(unittest.TestCase):
    if local:
        TEST_URL = LOCALHOST + 'game/submit'
    else:
        TEST_URL = "https://gamecraftfunc.azurewebsites.net/game/submit"

    def test_submit_game(self):
        payload = test_game1
        json_payload = json.dumps(payload)
        response = requests.post(self.TEST_URL, data=json_payload)
        self.assertEqual(200, response.status_code)
        # More assertions can be added here based on the expected response


# test wierd cuz of id
class TestUpdateGame(unittest.TestCase):
    if local:
        TEST_URL = LOCALHOST + 'game/update'
    else:
        TEST_URL = "https://gamecraftfunc.azurewebsites.net/game/update"

    def test_update_game(self):

        r = requests.get(LOCALHOST + "game/getall")
        payload = r.json()['data'][0]
        payload.update(test_game2)
        json_payload = json.dumps(payload)
        print(payload)
        response = requests.put(self.TEST_URL, data=json_payload)

        self.assertEqual(200, response.status_code)
        # More assertions can be added here based on the expected response


# Define the test class for getting games
# currently only tests the first game but tbh why would the rest not work?
class TestGetGames(unittest.TestCase):
    if local:
        TEST_URL = LOCALHOST + 'game/getall'
    else:
        TEST_URL = "https://gamecraftfunc.azurewebsites.net/game/getall"

    def test_get_games(self):
        response = requests.get(self.TEST_URL)  # Use GET since it's "get_all_games"

        self.assertEqual(response.json()['result'], True)

        game = response.json()['data']
        del game['_etag'], game['_rid'], game['_self'], game['_ts'], game['id'], game['_attachments']

        self.assertEqual(game, test_game1)
        # More assertions can be added here based on the expected response


class TestStoreImage(unittest.TestCase):
    if local:
        TEST_URL = LOCALHOST + 'image/store'
    else:
        TEST_URL = "https://gamecraftfunc.azurewebsites.net/image/store"

    files = {'file': open('test.png', 'rb')}


    def test_store_image(self):

        response = requests.post(self.TEST_URL, files=self.files)
        print(response.json())

        return 0


class TestGetImage(unittest.TestCase):
    if local:
        TEST_URL = LOCALHOST + 'image/get'
    else:
        TEST_URL = "https://gamecraftfunc.azurewebsites.net/image/get"

    def test_get_image(self):

        payload = {
            'id': 'test.png'
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Functions-Key': KEY
        }
        json_payload = json.dumps(payload)
        response = requests.get(self.TEST_URL, data=json_payload, headers=headers)

        return 0


class TestSubscribe(unittest.TestCase):
    if local:
        TEST_URL = LOCALHOST + 'subscribe'
    else:
        TEST_URL = "https://gamecraftfunc.azurewebsites.net/subscribe"

    def test_subscribe(self):

        payload = {
            'username': 'saarujan555',
            'game_id': 'b38b929c-37f4-4367-be4c-8c48d9bcc159'
        }
        headers = {
            'Content-Type': 'application/json',
            'X-Functions-Key': KEY
        }

        response = requests.post(self.TEST_URL, data=json.dumps(payload), headers=headers)
        print(response.json())


# Create a test suite combining all tests
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestUserRegister))
    # suite.addTest(unittest.makeSuite(TestGetGames))
    return suite


# Run the test suite
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())
