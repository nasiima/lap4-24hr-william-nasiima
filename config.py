import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'guess-me'
    DEBUG = bool(os.environ.get('DEBUG')) or True
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI') or 'sqlite:///urlshortener.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False