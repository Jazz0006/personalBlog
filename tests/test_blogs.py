import unittest
from main import create_app
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["FLASK_ENV"] = "testing"

class TestBlogs(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_blog_index(self):
        response = self.client.get("/blogs/")
        data = response.data
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h2>Timeline', data)

    def test_creat_bad_blog(self):
        ''' Test case for creating a blog with empty title'''
        # First register a user and login
        response = self.client.post("/users/signup/", data=dict(
            user_name = "test user",
            email = "test@fakemail.com",
            password = "1234567"),
            follow_redirects=True,
            headers = {"Content-Type":"application/x-www-form-urlencoded"}
        )

        self.assertEqual(response.status_code, 200)
        response = self.client.post("/blogs/", data={"blog_title": ""})
        self.assertEqual(response.status_code, 400)