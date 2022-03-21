from flask import Flask


def create_app(config_class_name):
    app = Flask(__name__)

    from first_app import auth_bp
    app.register_blueprint(auth_bp)
