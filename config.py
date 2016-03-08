import os

class ProdConfig(object):
    DEBUG = False
    PORT = os.getenv('PORT', 5000)
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = '\xf4\xf3\xda\x83\xab\x0f\xf8\x92DZ\xa2\x17\xe0\xdd\xd8\xa4\xdc\xdd\xa9[l\xf9~\x1f'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

class DevConfig(ProdConfig):
    DEBUG = True
