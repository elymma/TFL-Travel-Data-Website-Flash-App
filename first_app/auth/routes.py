from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from sqlalchemy.exc import IntegrityError
from urllib.parse import urlparse, urljoin
from datetime import timedelta
from flask_login import login_user, logout_user, login_required

from first_app import db
from first_app.auth.forms import SignupForm, LoginForm
from first_app.models import User
from first_app import login_manager

auth_bp = Blueprint("auth", __name__, url_prefix="/signup")


@auth_bp.route("/", methods=["GET", "POST"])
def signup():
    signup_form = SignupForm(request.form)
    if signup_form.validate_on_submit():
        user = User(first_name=signup_form.first_name.data, last_name=signup_form.last_name.data,
                    email=signup_form.email.data)
        user.set_password(signup_form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Congrats, {user.first_name} {user.last_name}. You are signed up to the TFL Travel Dashboard!")
        except IntegrityError:
            db.session.rollback()
            flash(f"Error, unable to register {signup_form.email.data}. ", "error")
            return redirect(url_for("auth.signup"))
        return redirect(url_for("main.index"))
    return render_template("signup.html", title="Sign Up", form=signup_form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if login_form.validate_on_submit():
        user = User.query.filter_by(email=login_form.email.data).first()
        login_user(user, remember=login_form.remember.data, duration=timedelta(minutes=1))
        next = request.args.get("next")
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for("main.index"))
    return render_template("login.html", title="Login", form=login_form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@login_manager.user_loader
def load_user(user_id):
    """ Takes a user ID and returns a user object or None if the user does not exist"""
    if user_id is not None:
        return User.query.get(user_id)
    return None


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash("Oops! You must be logged in to view the TFL Travel Dashbaord.")
    return redirect(url_for("auth.login"))


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ("http", "https") and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get("next")
    if url and is_safe_url(url):
        return url
    url = request.referrer
    if url and is_safe_url(url):
        return url
    return "/"
