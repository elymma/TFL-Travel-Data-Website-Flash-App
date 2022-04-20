from flask import Blueprint, render_template, flash
from flask_login import current_user

profile_bp = Blueprint("profile_bp", __name__, url_prefix="/profile")


@profile_bp.route("/")
def index():
    if not current_user.is_anonymous:
        name = current_user.first_name
        user_details = {"First Name": current_user.first_name,
                        "Last Name": current_user.last_name,
                        "Email Address": current_user.email}
        flash(f"Hello {name}! Here you can view your profile details.")
    else:
        user_details = {}
        flash("Oops! You must be logged in to view your profile details.")

    return render_template("profile.html", profile_details=user_details, title="Profile")
