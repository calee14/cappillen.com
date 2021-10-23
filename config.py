import os
JWT_SECRET_KEY = ''
try:
    from secret import JWT_SECRET_KEY
except:
    JWT_SECRET_KEY = os.environ['JWTKEY']
class Config(object):
    TESTING = False
    DEBUG = True
    SECRET_KEY = os.urandom(32)
    JWT_SECRET_KEY = JWT_SECRET_KEY