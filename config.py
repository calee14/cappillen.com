import os
from secret import JWT_SECRET_KEY
class Config(object):
    TESTING = False
    DEBUG = True
    SECRET_KEY = os.urandom(32)
    JWT_SECRET_KEY = JWT_SECRET_KEY