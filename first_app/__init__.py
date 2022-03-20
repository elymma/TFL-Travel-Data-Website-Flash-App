from flask import Flask
from config import DevelopmentConfig


def create_app():
    """
    Initialise the Flask application.
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    return app




