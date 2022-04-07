from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


csrf = CSRFProtect()
db = SQLAlchemy()


def create_app(config_class_name):
    """
    Initialise and configure the Flask application.
    :type: config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)
    csrf.init_app(app)
    db.init_app(app)

    with app.app_context():
        from first_app.models import User
        db.create_all()

    # Blueprints
    from first_app.main.routes import main_bp
    app.register_blueprint(main_bp)

    from first_app.auth.routes import auth_bp
    app.register_blueprint(auth_bp)

    from first_app.community.routes import community_bp
    app.register_blueprint(community_bp)

    from first_app.messaging.routes import messaging_bp
    app.register_blueprint(messaging_bp)

    from first_app.profile.routes import profile_bp
    app.register_blueprint(profile_bp)

    from first_app.dash.routes import dash_bp
    app.register_blueprint(dash_bp)



    return app

