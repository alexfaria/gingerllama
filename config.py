import os

class ProdConfig(object):
    DEBUG = False
    PORT = os.getenv('PORT', 5000)
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_TRACK_MODIFICATIONS = True       # surpress annoying message

class DevConfig(ProdConfig):
    DEBUG = True
