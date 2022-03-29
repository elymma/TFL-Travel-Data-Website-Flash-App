from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length


class SignupForm(FlaskForm):
    first_name = StringField(label="First name", validators=[DataRequired("First name must be entered!"), Length(max=20, message="Maximum characters reached!")])
    last_name = StringField(label="Last name", validators=[DataRequired("Last name must be entered!"), Length(max=20, message="Maximum characters reached!")])
    email = EmailField(label="Email address", validators=[DataRequired("Email address must be entered!")])
    password = PasswordField(label="Password", validators=[DataRequired("A password must be entered!"), Length(min=8, max=20, message="Password must be between 8 and 20 characters long!")])
    password_repeat = PasswordField(label="Repeat Password",
                                    validators=[DataRequired("Repeat password!"), EqualTo("password", message="Entered passwords must match!")])


