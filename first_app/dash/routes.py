from flask import Blueprint, render_template

dash_bp = Blueprint("dash_bp", __name__, url_prefix="/dash")


@dash_bp.route("/")
def index():
    return render_template("dash.html", title="Dash App")

