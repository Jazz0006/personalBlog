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
        self.assertIn(b'<h2>Blog Index</h2>', data)

    def test_creat_bad_blog(self):
        response = self.client.post("/blogs/", data={"blog_title": ""})
        self.assertEqual(response.status_code, 400)