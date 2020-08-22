# -*- coding: utf-8 -*-

from flask import Blueprint, jsonify, request

# from flask_login import login_user, current_user, logout_user
from flask_restful import Api, Resource, reqparse

# from ..user import User


api = Blueprint("api", __name__, url_prefix="/api")
api_wrap = Api(api)


class CompanyNameCandi(Resource):
    #  curl http://127.0.0.1:5000/api/company-name-candi?type=round
    def get(self):
        (companyNameSeg) = self._getArguments()

        return {"company_name_candidates": ['wanted', 'warned']}

    def _getArguments(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            "company_name", help="company_name is needed", type=str, required=True,
        )
        args = parser.parse_args()
        return args["company_name"]


api_wrap.add_resource(CompanyNameCandi, "/company-name-candi")


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
