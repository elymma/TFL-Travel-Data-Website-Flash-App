from flask import Blueprint, render_template

profile_bp = Blueprint("profile_bp", __name__, url_prefix="/profile")


@profile_bp.route("/")
def index():
    return render_template("profile.html", title="Profile")

