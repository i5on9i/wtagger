# -*- coding: utf-8 -*-

import os

from wtagger.utils import INSTANCE_FOLDER_PATH, make_dir


class BaseConfig(object):

    PROJECT = "wtagger"

    # Get app root path, also can use flask.root_path.
    # ../../config.py
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    ADMINS = ["youremail@yourdomain.com"]

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = "secret key"

    LOG_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, "logs")

    # Fild upload, should override in production.
    # Limited the maximum allowed payload to 16 megabytes.
    # http://flask.pocoo.org/docs/patterns/fileuploads/#improving-uploads
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(INSTANCE_FOLDER_PATH, "uploads")


class DefaultConfig(BaseConfig):

    DEBUG = True

    SENTRY_DSN = ""

    MAIL_HOST = ""
    FROM_ADDR = ""
    TO_ADDRS = [""]
    MAIL_USERNAME = ""
    MAIL_PASSWORD = ""

    # Flask-Sqlalchemy: http://packages.python.org/Flask-SQLAlchemy/config.html
    SQLALCHEMY_ECHO = False
    # SQLALCHEMY_TRACK_MODIFICATIONS adds significant overhead and will be
    # disabled by default in the future.
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # SQLITE for prototyping.
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + INSTANCE_FOLDER_PATH + "/db.sqlite"
    # MYSQL for production.
    # SQLALCHEMY_DATABASE_URI = 'mysql://username:password@server/db?charset=utf8'


class TestConfig(BaseConfig):
    TEST_DB = "test.db"

    TESTING = True
    CSRF_ENABLED = False
    WTF_CSRF_ENABLED = False

    SQLALCHEMY_ECHO = False

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
        os.path.dirname(__file__), "tests", TEST_DB
    )
