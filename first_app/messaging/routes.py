from flask import Blueprint, render_template

messaging_bp = Blueprint("messaging_bp", __name__, url_prefix="/messaging")


@messaging_bp.route("/")
def index():
    return render_template("message.html", title="Messaging")

