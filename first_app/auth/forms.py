from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length, ValidationError

from first_app.models import User


class SignupForm(FlaskForm):
    first_name = StringField(label="First name", validators=[DataRequired("First name must be entered!"), Length(max=20, message="Maximum characters reached!")])
    last_name = StringField(label="Last name", validators=[DataRequired("Last name must be entered!"), Length(max=20, message="Maximum characters reached!")])
    email = EmailField(label="Email address", validators=[DataRequired("Email address must be entered!")])
    password = PasswordField(label="Password", validators=[DataRequired("A password must be entered!"), Length(min=8, max=20, message="Password must be between 8 and 20 characters long!")])
    password_repeat = PasswordField(label="Repeat Password",
                                    validators=[DataRequired("Repeat password!"), EqualTo("password", message="Entered passwords must match!")])

# add additional elements using links in week same task 2 file
# fix validation messages, the dont appear :(

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError("An account is already registered for that email address")

# add more custom validators from week 7 task 4


class LoginForm(FlaskForm):
    email = EmailField(label="Email address", validators=[DataRequired()])
    password = PasswordField(label="Password", validators=[DataRequired()])
    remember = BooleanField(label="Remember me")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("No account found with that email address.")

    def validate_password(self, password):
        user = User.query.filter_by(email=self.email.data).first()
        if user is None:
            raise ValidationError("No account found with that email address.")
        if not user.check_password(password.data):
            raise ValidationError("Incorrect password.")