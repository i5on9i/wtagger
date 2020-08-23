import json
import unittest

from wtagger.app import create_app
from wtagger.config import TestConfig
from wtagger.extensions import db

# for debug
# import os
# import sys
# BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..')
# if BASE_DIR not in sys.path:
#     sys.path.append(BASE_DIR)



class BasicTests(unittest.TestCase):

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
        # db.session.remove()
        # db.drop_all()
        pass

    def test_companyNameCandi(self):
        response = self.app.get(
            "/api/company-name-candi?company_name=wan", follow_redirects=True
        )
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            json.dumps({"company_name_candidates": []}),
            response.data.decode("utf8").strip(),
        )


if __name__ == "__main__":
    unittest.main()
