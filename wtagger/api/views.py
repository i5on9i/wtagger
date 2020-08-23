# -*- coding: utf-8 -*-

from typing import List

from flask import Blueprint, g, jsonify, request

# from flask_login import login_user, current_user, logout_user
from flask_restful import Api, Resource, reqparse

from wtagger.extensions import db
from wtagger.models.company import Company

# from ..user import User


api = Blueprint("api", __name__, url_prefix="/api")
api_wrap = Api(api)


class CompanyNameCandi(Resource):
    #  curl http://127.0.0.1:5000/api/<lang>/company-name-candi?company_name=round
    def get(self):

        curlang = g.get("current_lang", "en")

        companyNameSeg = self._getArguments()
        candies = Company.searchByName(companyNameSeg, curlang)

        return jsonify(result=candies)

    def _getArguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "company_name", help="company_name is needed", type=str, required=True,
        )
        # parser.add_argument(
        #     "lang", help="language should be selected", type=str, required=True,
        # )
        args = parser.parse_args()
        return args["company_name"]


api_wrap.add_resource(
    CompanyNameCandi, "/company-name-candi", "/<lang>/company-name-candi"
)


class CompanyNameByTag(Resource):
    #  curl http://127.0.0.1:5000/api/company-name-by-tag?tag=round
    def get(self):
        curlang = g.get("current_lang", "en")
        tag = self._getArguments()
        candies = Company.searchByTag(tag, curlang)

        return jsonify(result=candies)

    def _getArguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "tag", help="tag is needed", type=str, required=True,
        )
        args = parser.parse_args()
        return args["tag"]


api_wrap.add_resource(
    CompanyNameByTag, "/company-name-by-tag", "/<lang>/company-name-by-tag"
)


class AddCompanyTag(Resource):
    # curl -X POST -d '{"id": 1, "tags":["마이태그1","마이태2"]} http://127.0.0.1:5000/api/add-company-tag
    def patch(self):
        curlang = g.get("current_lang", "en")

        args = self._getArguments()
        comp = Company.query.get(args["id"])
        if not comp:
            return jsonify(result="fail", message="wrong company id")

        tagCol = f"company_tag_{curlang}"
        if not hasattr(comp, tagCol):
            return jsonify(result="fail", message="wrong language")

        companyTag = getattr(comp, tagCol)
        if companyTag is None:
            companyTag = ""

        if companyTag:
            # not (None or '')
            companyTag += "|"
        companyTag += f"{'|'.join(args['tags'])}"
        setattr(comp, tagCol, companyTag)

        db.session.add(comp)
        db.session.commit()

        return {"result": "success"}

    def _getArguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "id", type=int, required=True,
        )
        parser.add_argument("tags", required=True, action="append")

        args = parser.parse_args()
        return args


api_wrap.add_resource(AddCompanyTag, "/add-company-tag", "/<lang>/add-company-tag")


class AddCompany(Resource):
    # curl -X POST -d '{"company_name_ko":"소소", "company_tag_ko":"멋진|이렇게"}' http://127.0.0.1:5000/api/add-company
    def post(self):
        args = self._getArguments()
        comp = Company(**args)
        db.session.add(comp)
        db.session.commit()

        return {"result": "success"}

    def _getArguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "company_name_ko", type=str, required=False,
        )
        parser.add_argument(
            "company_name_en", type=str, required=False,
        )
        parser.add_argument(
            "company_name_ja", type=str, required=False,
        )
        parser.add_argument(
            "company_tag_ko", type=str, required=False,
        )
        parser.add_argument(
            "company_tag_en", type=str, required=False,
        )
        parser.add_argument(
            "company_tag_ja", type=str, required=False,
        )
        args = parser.parse_args()
        return args


api_wrap.add_resource(AddCompany, "/add-company")


@api.route("/login", methods=["POST"])
def login():
    # if current_user.is_authenticated():
    #     return jsonify(flag='success')

    # username = request.form.get('username')
    # password = request.form.get('password')
    # if username and password:
    #     user, authenticated = User.authenticate(username, password)
    #     if user and authenticated:
    #         if login_user(user, remember='y'):
    #             return jsonify(flag='success')

    return jsonify(flag="fail", msg="Sorry, try again.")


@api.route("/logout")
def logout():
    # if current_user.is_authenticated():
    #     logout_user()
    return jsonify(flag="success", msg="Logouted.")
