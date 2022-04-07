from flask import Blueprint, render_template, flash, redirect, url_for, request
from sqlalchemy.exc import IntegrityError

from first_app import db
from first_app.auth.forms import SignupForm
from first_app.models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/signup")


@auth_bp.route("/", methods=["GET", "POST"])
def signup():
    form = SignupForm(request.form)
    if form.validate_on_submit():
        # name = form.first_name.data
        # flash(f"Congrats {name}, you are signed up to the TFL Travel Dashboard!")
        # return redirect(url_for("main.index"))
        user = User(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.first_name} {user.last_name}. You are signed up.")
        except IntegrityError:
            db.session.rollback()
            flash(f"Error, unable to register {form.email.data}. ", "error")
            return redirect(url_for("auth.signup"))
        return redirect(url_for("main.index"))
    return render_template("signup.html", title="Sign Up", form=form)





