import unittest
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'program'))
from main import create_app, db
from dotenv import load_dotenv
from models.users import User

load_dotenv()

os.environ["FLASK_ENV"] = "testing"

class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    # The test cases to test relationship between tables
    # Todo: Add configuration of DB
    
    # def test_follow(self):
    #     app = create_app()
    #     u1 = User(user_name="star_user", email="fake@email.com", password="1234567")
    #     u2 = User(user_name="fan_user", email="fake2@rmail.com", password="7654321")
    #     db.session.add(u1)
    #     db.session.add(u2)
    #     db.session.commit()
    #     u1.follow(u2)
    #     print(u1.followed)
        

if __name__ == '__main__':
    unittest.main(verbosity=2)