from flask import Blueprint, render_template

community_bp = Blueprint("community_bp", __name__, url_prefix="/community")


@community_bp.route("/")
def index():
    return render_template("message.html", title="Messaging")

