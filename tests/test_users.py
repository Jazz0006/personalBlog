import unittest
import sys, os
from main import create_app
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'program'))
from dotenv import load_dotenv

load_dotenv()

os.environ["FLASK_ENV"] = "testing"

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_signup(self):
        # register a user and login
        response = self.client.post("/users/signup/", data=dict(
            user_name = "test register",
            email = "test@fakemail.com",
            password = "1234567"),
            follow_redirects=True,
            headers = {"Content-Type":"application/x-www-form-urlencoded"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'User Index', response.data)
        response = self.client.post("/users/delete/")
        self.assertIn(b'View Blogs', response.data)

    def test_follow(self):
        # Register the first user
        self.client.post("/users/signup/", data=dict(
            user_name = "star user",
            email = "star@fakemail.com",
            password = "1234567"),
            follow_redirects=True,
            headers = {"Content-Type":"application/x-www-form-urlencoded"}
        )


        # Register the second user
        self.client.post("/users/signup/", data=dict(
            user_name = "fan user",
            email = "fan@fakemail.com",
            password = "1234567"),
            follow_redirects=True,
            headers = {"Content-Type":"application/x-www-form-urlencoded"}
        )

        # Todo: gain access to db, and adding relationship