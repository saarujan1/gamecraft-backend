import unittest
import json
import requests
from azure.cosmos import CosmosClient

# Define the test class for submitting games
class TestUserRegister(unittest.TestCase):
    TEST_URL = "https://gamecraft-backend.azurewebsites.net/user_register?code=LB8AZj2jaF-kvYrWcqpm9ibnAANp_DIdVhFnWd4dhQ7aAzFutcScfw=="

    def test_user_register(self):
        payload = {
            'username': 'saarujan123',
            'password' : 'password123',
            'usertype' : 'dev'

        }
        json_payload = json.dumps(payload)
        response = requests.post(self.TEST_URL, data=json_payload)
        self.assertEqual(response.status_code, 200)
        # More assertions can be added here based on the expected response

# Define the test class for submitting games
class TestUserLogin(unittest.TestCase):
    TEST_URL = "https://gamecraft-backend.azurewebsites.net/user_login?code=Yg9fPNSO6evj2mooNDCwJ7vr4nGv_xmX40Pd-PuUmMW4AzFuOZHwuQ=="

    def test_user_register(self):
        payload = {
            'username': 'saarujan123',
            'password' : 'password123',
        }
        json_payload = json.dumps(payload)
        response = requests.post(self.TEST_URL, data=json_payload)
        self.assertEqual(response.status_code, 200)
        # More assertions can be added here based on the expected response

# Define the test class for submitting games
class TestSubmitGame(unittest.TestCase):
    TEST_URL = "https://gamecraft-backend.azurewebsites.net/submit_game?code=cPs-op-r7rAFOF_eKXg08jmTiwjRyN1s6gA_dOBKfp5lAzFuM4CODQ=="

    def test_submit_game(self):
        payload = {
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
        json_payload = json.dumps(payload)
        response = requests.post(self.TEST_URL, data=json_payload)
        self.assertEqual(response.status_code, 200)
        # More assertions can be added here based on the expected response

# Define the test class for getting games
class TestGetGames(unittest.TestCase):
    TEST_URL = "https://gamecraft-backend.azurewebsites.net/get_all_games?code=AYy_xEePSR3Dqo6GxoHaOmV0bIHG4gm0hJyb4SP6UvaRAzFu6YaOLw=="

    def test_get_games(self):
        response = requests.get(self.TEST_URL)  # Use GET since it's "get_all_games"
        self.assertEqual(response.status_code, 200)
        # More assertions can be added here based on the expected response

# Create a test suite combining all tests
def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestSubmitGame))
    suite.addTest(unittest.makeSuite(TestGetGames))
    return suite

# Run the test suite
if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(suite())