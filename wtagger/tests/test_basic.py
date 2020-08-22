import os
import unittest

from wtagger.app import create_app
from wtagger.config import TestConfig
from wtagger.extensions import db

TEST_DB = 'test.db'
 

class BasicTests(unittest.TestCase):
 
    ############################
    #### setup and teardown ####
    ############################
 
    # executed prior to each test
    def setUp(self):
        app = create_app(TestConfig) 
        self.app = app.test_client()
        db.init_app(app)
        with app.app_context():
            db.drop_all()
            db.create_all()
 
        # Disable sending emails during unit testing
        # mail.init_app(app)
        self.assertEqual(app.debug, False)
 
    # executed after each test
    def tearDown(self):
        pass
 
 
###############
#### tests ####
###############
 
    def test_main_page(self):
        response = self.app.get('/api/company-name-candi', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
 
 
if __name__ == "__main__":
    unittest.main()
