import os


class Config(object):
    DEBUG = False

    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = 'SECRET_OR_NOT_KEY'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False


class DevelopmentConfig(Config):
    DEBUG = True
