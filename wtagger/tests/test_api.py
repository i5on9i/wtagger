# for debug
# import os, sys
# BASE_DIR = os.path.join(os.path.dirname(__file__), '..', '..')
# if BASE_DIR not in sys.path:
#     sys.path.append(BASE_DIR)

import json
import unittest
from wtagger.models.company import Company
from wtagger.extensions import db
from wtagger.config import TestConfig
from wtagger.app import create_app


class TestApi(unittest.TestCase):
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

    def test_companyNameCandi(self):

        self.app.post(
            "/api/add-company",
            data={"company_name_ko": "teste"},
            follow_redirects=True,
        )
        self.app.post(
            "/api/add-company",
            data={
                "company_name_jp": "teste",
                "company_name_ko": "kr-teste",
                "company_tag_jp": "whatdet|dvsdet",
            },
            follow_redirects=True,
        )

        response = self.app.get(
            "/api/company-name-candi?company_name=tes", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(jdata["result"]))
        self.assertListEqual(sorted(["teste", "kr-teste"]), sorted(jdata["result"]))

    def test_addCompany(self):

        response = self.app.post(
            "/api/add-company",
            data={"company_name_kr": "teste"},
            follow_redirects=True,
        )

        self.assertEqual(200, response.status_code)
        self.assertEqual(
            json.dumps({"result": "success"}), response.data.decode("utf8").strip(),
        )

        response = self.app.post(
            "/api/add-company",
            data={
                "company_name_jp": "teste",
                "company_name_ko": "kr-teste",
                "company_tag_jp": "whatdet|dvsdet",
            },
            follow_redirects=True,
        )
        self.assertEqual(200, response.status_code)


if __name__ == "__main__":
    unittest.main()
