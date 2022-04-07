"""Flask config class."""
import pathlib


class Config(object):
    """ Sets the Flask base configuration usd in all environments. """
    DEBUG = False
    SECRET_KEY = "DRvGGWVHAq9iudKYo6Fivg"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(DATA_PATH.joinpath("example.sqlite"))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(pathlib.Path(__file__).parent.joinpath('first_app.sqlite'))


class ProductionConfig(Config):
    ENV = 'production'


class DevelopmentConfig(Config):
    ENV = 'development'
    DEBUG = True
    SQLALCHEMY_ECH0 = True


class TestingConfig(Config):
    ENV = 'testing'
    TESTING = True
    SQLALCHEMY_ECH0 = True



