from flask import Blueprint, render_template
from first_app.auth.forms import SignupForm

auth_bp = Blueprint("auth", __name__, url_prefix="/signup")


@auth_bp.route("/", methods=["GET", "POST"])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        name = form.first_name.data
        return f"Congrats {name}, you are signed up to the TFL Travel Dashboard!"

    return render_template("signup.html", title="Sign Up", form=form)





