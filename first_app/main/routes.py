from flask import Blueprint

main_bp = Blueprint("main", __name__, url_prefix="/main")


@main_bp.route("/")
def index():
    return "This is the main page for my_flask_app"
