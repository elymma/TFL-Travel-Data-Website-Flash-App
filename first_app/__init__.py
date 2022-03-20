from flask import Flask
from config import DevelopmentConfig


def create_app():
    """
    Initialise and configure the Flask application.
    :type: config_classname: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    from first_app.community.routes import community_bp
    app.register_blueprint(community_bp)

    from first_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    return app
