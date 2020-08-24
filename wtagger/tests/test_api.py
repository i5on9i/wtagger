# for debug
# import os, sys

# BASE_DIR = os.path.join(os.path.dirname(__file__), "..", "..")
# if BASE_DIR not in sys.path:
#     sys.path.append(BASE_DIR)

import json
import unittest

from wtagger.app import create_app
from wtagger.config import TestConfig
from wtagger.extensions import db
from wtagger.models.company import Company


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

    def test_companyNameCandiWithLang(self):
        # insert test data
        self.app.post(
            "/api/add-company",
            data={"company_name_ko": "teste"},
            follow_redirects=True,
        )
        self.app.post(
            "/api/add-company",
            data={"company_name_ja": "jejej023"},
            follow_redirects=True,
        )
        self.app.post(
            "/api/add-company",
            data={"company_name_en": "engcomp"},
            follow_redirects=True,
        )
        self.app.post(
            "/api/add-company",
            data={
                "company_name_ja": "02343",
                "company_name_ko": "kr-teste",
                "company_tag_ja": "whatdet|dvsdet",
            },
            follow_redirects=True,
        )

        # wrong language
        response = self.app.get(
            "/api/kr/company-name-candi?company_name=tes", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(jdata["result"]), "wrong language character")
        self.assertListEqual(sorted([]), sorted(jdata["result"]))

        # ko
        response = self.app.get(
            "/api/ko/company-name-candi?company_name=tes", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(jdata["result"]))
        self.assertListEqual(sorted(["teste", "kr-teste"]), sorted(jdata["result"]))

        # ja
        response = self.app.get(
            "/api/ja/company-name-candi?company_name=023", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(jdata["result"]))
        self.assertListEqual(sorted(["jejej023", "02343"]), sorted(jdata["result"]))

        # default en
        response = self.app.get(
            "/api/company-name-candi?company_name=mp", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(jdata["result"]), "default language")
        self.assertListEqual(sorted(["engcomp"]), sorted(jdata["result"]))

    def test_companyNameByTag(self):
        # insert test data
        self.app.post(
            "/api/add-company",
            data={
                "company_name_ja": "02343",
                "company_name_ko": "jpteste",
                "company_tag_ja": "jtag1|jtag2",
            },
            follow_redirects=True,
        )
        self.app.post(
            "/api/add-company",
            data={
                "company_name_ja": "1111",
                "company_name_ko": "dkfjlwes",
                "company_tag_ko": "ta소|나나",
            },
            follow_redirects=True,
        )
        self.app.post(
            "/api/add-company",
            data={
                "company_name_ja": "1111",
                "company_name_ko": "krteste",
                "company_tag_ko": "ta소|나나2|sdfsd",
                "company_tag_ja": "jtag11|jtag1",
            },
            follow_redirects=True,
        )
        self.app.post(
            "/api/add-company",
            data={
                "company_name_en": "ebebee",
                "company_tag_en": "en4",
                "company_tag_ja": "jtag1|jtag2",
            },
            follow_redirects=True,
        )

        # not match case - wrong language
        fitem = "ta"
        lang = "kk"
        response = self.app.get(
            f"/api/{lang}/company-name-by-tag?tag={fitem}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(jdata["result"]))
        self.assertListEqual(sorted([]), sorted(jdata["result"]))

        # no matching tag case
        fitem = "ta"
        response = self.app.get(
            f"/api/company-name-by-tag?tag={fitem}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(jdata["result"]))
        self.assertListEqual(sorted([]), sorted(jdata["result"]))

        # match case - default en with empty name
        fitem = "jtag1"
        response = self.app.get(
            f"/api/company-name-by-tag?tag={fitem}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(jdata["result"]), "en language")
        self.assertListEqual(sorted(["ebebee"]), sorted(jdata["result"]))

        # match case
        fitem = "jtag1"
        response = self.app.get(
            f"/api/en/company-name-by-tag?tag={fitem}", follow_redirects=True
        )
        jdata2 = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(jdata["result"]), len(jdata2["result"]))
        self.assertListEqual(sorted(jdata["result"]), sorted(jdata2["result"]))

        # ko
        fitem = "ta소"
        response = self.app.get(
            f"/api/ko/company-name-by-tag?tag={fitem}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(2, len(jdata["result"]), "ko language")
        self.assertListEqual(sorted(["dkfjlwes", "krteste"]), sorted(jdata["result"]))

        # ja, only matching full keyword
        fitem = "jtag11"
        response = self.app.get(
            f"/api/ja/company-name-by-tag?tag={fitem}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(jdata["result"]), "ja language")
        self.assertListEqual(sorted(["1111"]), sorted(jdata["result"]))

    def test_addCompanyTag(self):

        # wrong company id
        response = self.app.patch(
            "/api/add-company-tag",
            data={"id": 1, "tags": ["newtag1", "마이태그3"]},
            follow_redirects=True,
        )

        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {"result": "fail", "message": "wrong company id",}, jdata,
        )

        # add a row
        self.app.post(
            "/api/add-company",
            data={"company_name_ja": "02343", "company_name_ko": "jpteste",},
            follow_redirects=True,
        )
        # add a row
        self.app.post(
            "/api/add-company",
            data={
                "company_name_ja": "102343",
                "company_name_ko": "j2pteste",
                "company_name_en": "engname",
                "company_tag_ko": "jtag21|jtag22",
            },
            follow_redirects=True,
        )
        # add a row
        self.app.post(
            "/api/add-company",
            data={"company_name_en": "en12343", "company_name_ko": "jpteste1",},
            follow_redirects=True,
        )

        # ------------------------
        # no company_name_en
        newtag = "마이태그3"
        response = self.app.patch(
            "/api/add-company-tag",
            data={"id": 1, "tags": ["newtag1", newtag]},
            follow_redirects=True,
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {"result": "success",}, jdata,
        )

        response = self.app.get(
            f"/api/company-name-by-tag?tag={newtag}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(jdata["result"]))
        self.assertListEqual(sorted([]), sorted(jdata["result"]))

        # ------------------------
        # add en tag
        newtag = "마이태그3"
        response = self.app.patch(
            "/api/add-company-tag",
            data={"id": 2, "tags": ["newtag1", newtag]},
            follow_redirects=True,
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {"result": "success",}, jdata,
        )

        response = self.app.get(
            f"/api/company-name-by-tag?tag={newtag}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(jdata["result"]))
        self.assertListEqual(sorted(["engname"]), sorted(jdata["result"]))

        # ------------------------
        # add en tag
        newtag = "마이태그4"
        response = self.app.patch(
            "/api/ko/add-company-tag",
            data={"id": 1, "tags": ["newtag1", newtag]},
            follow_redirects=True,
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {"result": "success",}, jdata,
        )

        response = self.app.get(
            f"/api/ko/company-name-by-tag?tag={newtag}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(jdata["result"]))
        self.assertListEqual(sorted(["jpteste"]), sorted(jdata["result"]))

        # ------------------------
        # tags with the duplicated
        newtag = "mytag5"
        response = self.app.patch(
            "/api/en/add-company-tag",
            data={"id": 3, "tags": [newtag, newtag]},
            follow_redirects=True,
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {"result": "success",}, jdata,
        )

        response = self.app.get(
            f"/api/en/company-tag", follow_redirects=True, data={"id": 3}
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(jdata["result"]))
        self.assertListEqual(sorted([newtag]), sorted(jdata["result"]))

        # ------------------------
        # en solo tag which exists

        # get pre status
        response = self.app.get(
            f"/api/en/company-tag", follow_redirects=True, data={"id": 3}
        )
        preJdata = json.loads(response.data)

        # insert new tag
        newtag = "mytag5"
        response = self.app.patch(
            "/api/en/add-company-tag",
            data={"id": 3, "tags": [newtag]},
            follow_redirects=True,
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {"result": "success",}, jdata,
        )

        # get current tag
        response = self.app.get(
            f"/api/en/company-tag", follow_redirects=True, data={"id": 3}
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(len(preJdata["result"]) + 0, len(jdata["result"]))
        self.assertListEqual(sorted([newtag]), sorted(jdata["result"]))

    def test_removeCompanyTag(self):

        # add a row
        extag = "마이태그"
        self.app.post(
            "/api/add-company",
            data={
                "company_name_ko": "원티드랩",
                "company_name_en": "Wantedlab",
                "company_tag_ko": "태그_4|태그_20|태그_16|마이태3",
                "company_tag_en": f"tag_4|tag_20|tag_16|{extag}",
                "company_tag_ja": "タグ_4|タグ_20|タグ_16",
            },
            follow_redirects=True,
        )

        # ------------------------
        # non-existing tag
        rmtag1 = "마이태그3"

        response = self.app.patch(
            "/api/remove-company-tag",
            data={"id": 1, "tags": [rmtag1]},
            follow_redirects=True,
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {"result": "success",}, jdata,
        )

        response = self.app.get(
            f"/api/company-name-by-tag?tag={extag}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(jdata["result"]))
        self.assertListEqual(sorted(["Wantedlab"]), sorted(jdata["result"]))

        # ------------------------
        # non-existing tag - wrong language
        rmtag1 = "タグ_4"
        response = self.app.patch(
            "/api/remove-company-tag",
            data={"id": 1, "tags": [rmtag1]},
            follow_redirects=True,
        )
        response = self.app.get(
            f"/api/company-name-by-tag?tag={rmtag1}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(jdata["result"]))
        self.assertListEqual(sorted(["Wantedlab"]), sorted(jdata["result"]))

        # ------------------------
        # wrong language
        rmtag1 = "タグ_4"
        response = self.app.patch(
            "/api/jp/remove-company-tag",
            data={"id": 1, "tags": [rmtag1]},
            follow_redirects=True,
        )
        response = self.app.get(
            f"/api/company-name-by-tag?tag={rmtag1}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(1, len(jdata["result"]))
        self.assertListEqual(sorted(["Wantedlab"]), sorted(jdata["result"]))

        # ------------------------
        # remove a tag
        rmtag1 = "タグ_4"
        response = self.app.patch(
            "/api/ja/remove-company-tag",
            data={"id": 1, "tags": [rmtag1]},
            follow_redirects=True,
        )
        response = self.app.get(
            f"/api/company-name-by-tag?tag={rmtag1}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(jdata["result"]))
        self.assertListEqual(sorted([]), sorted(jdata["result"]))
        # restore
        response = self.app.patch(
            "/api/ja/add-company-tag",
            data={"id": 1, "tags": [rmtag1]},
            follow_redirects=True,
        )

        # ------------------------
        # remove tags
        rmtag1 = "タグ_4"
        rmtag2 = "タグ_20"
        response = self.app.patch(
            "/api/ja/remove-company-tag",
            data={"id": 1, "tags": [rmtag1, rmtag2]},
            follow_redirects=True,
        )
        response = self.app.get(
            f"/api/company-name-by-tag?tag={rmtag1}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(jdata["result"]))
        response = self.app.get(
            f"/api/company-name-by-tag?tag={rmtag2}", follow_redirects=True
        )
        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(0, len(jdata["result"]))

    def test_addCompany(self):

        response = self.app.post(
            "/api/add-company",
            data={"company_name_kr": "teste"},
            follow_redirects=True,
        )

        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {"result": "success"}, jdata,
        )

        response = self.app.post(
            "/api/add-company",
            data={
                "company_name_ja": "teste",
                "company_name_ko": "kr-teste",
                "company_tag_ja": "whatdet|dvsdet",
            },
            follow_redirects=True,
        )
        self.assertEqual(200, response.status_code)

    def test_companyTag(self):
        # add row
        response = self.app.post(
            "/api/add-company",
            data={
                "company_name_ja": "teste",
                "company_name_ko": "kr-teste",
                "company_tag_ja": "whatdet|dvsdet",
                "company_tag_en": "en_whatdet|en_dvsdet",
            },
            follow_redirects=True,
        )

        response = self.app.get(
            "/api/company-tag", data={"id": 1}, follow_redirects=True,
        )

        jdata = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertDictEqual(
            {"result": ["en_whatdet", "en_dvsdet"]}, jdata,
        )


if __name__ == "__main__":
    unittest.main()
