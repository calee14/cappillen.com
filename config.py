import os
import datetime

JWT_SECRET_KEY = ""
try:
    from secret import JWT_SECRET_KEY
except:
    JWT_SECRET_KEY = os.environ["JWTKEY"]


class Config(object):
    TESTING = False
    DEBUG = True
    SECRET_KEY = os.urandom(32)
    JWT_SECRET_KEY = JWT_SECRET_KEY
    JWT_SESSION_COOKIE = False
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_COOKIE_SECURE = False
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(days=30)
    JWT_COOKIE_CSRF_PROTECT = False
    JWT_ACCESS_CSRF_HEADER_NAME = "X-CSRF-TOKEN-ACCESS"
    JWT_REFRESH_CSRF_HEADER_NAME = "X-CSRF-TOKEN-REFRESH"
