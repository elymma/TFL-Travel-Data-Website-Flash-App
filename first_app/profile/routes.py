from flask import Blueprint, render_template, flash
from flask_login import current_user
import json

profile_bp = Blueprint("profile_bp", __name__, url_prefix="/profile")


@profile_bp.route("/")
def index():
    if not current_user.is_anonymous:
        name = current_user.first_name
        user_details = {"f_name": current_user.first_name,
                        "l_name": current_user.last_name,
                        "e_mail": current_user.email}
        flash(f"Hello {name} here you can view your profile details.")
    else:
        user_details = {}

    return render_template("profile.html", res=json.dumps(user_details), title="Profile")
