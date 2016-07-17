import os

class ProdConfig(object):
    DEBUG = False
    PORT = os.getenv('PORT', 5000)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')
    SECRET_KEY = os.getenv('SECRET_KEY', os.urandom(24).encode('hex'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True       # surpress annoying message

class DevConfig(ProdConfig):
    DEBUG = True
