from pathlib import Path

import dash
import dash_bootstrap_components as dbc
# import flask_images
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
# from flask_uploads import UploadSet, IMAGES, configure_uploads
from flask_login import LoginManager, login_required
from flask.helpers import get_root_path
# from flask_images import resized_img_src


csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')
db = SQLAlchemy()
login_manager = LoginManager()
# photos = UploadSet("photos", IMAGES)



def create_app(config_class_name):
    """
    Initialise and configure the Flask application.
    :type: config_class_name: Specifies the configuration class
    :rtype: Returns a configured Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class_name)

    register_dashapp(app)

    csrf.init_app(app)
    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)



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

    return app


def register_dashapp(app):
    """ Registers the Dash app in the Flask app and make it accessible on the route /dashboard/ """
    from tfl_app.layout import layout
    from tfl_app.callbacks import register_callbacks

    meta_viewport = {"name": "viewport", "content": "width=device-width, initial-scale=1, shrink-to-fit=no"}

    dashapp = dash.Dash(__name__,
                        server=app,
                        url_base_pathname='/dashboard/',
                        assets_folder=get_root_path(__name__) + '/dashboard/assets/',
                        meta_tags=[meta_viewport],
                        external_stylesheets=[dbc.themes.LUX])

    with app.app_context():
        dashapp.title = 'Dashboard'
        dashapp.layout = layout
        register_callbacks(dashapp)

        # Protects the views with Flask-Login
        _protect_dash_views(dashapp)


def _protect_dash_views(dash_app):
    """ Protects Dash views with Flask-Login"""
    for view_func in dash_app.server.view_functions:
        if view_func.startswith(dash_app.config.routes_pathname_prefix):
            dash_app.server.view_functions[view_func] = login_required(dash_app.server.view_functions[view_func])
