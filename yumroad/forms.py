from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash
from wtforms import PasswordField, StringField
from wtforms.fields import DecimalField
from wtforms.validators import (
    URL,
    EqualTo,
    InputRequired,
    Length,
    Optional,
    email,
)

from yumroad.models import User


class ProductForm(FlaskForm):
    name = StringField("Name", validators=[Length(min=4, max=60)])
    description = StringField("Description")
    picture_url = StringField(
        "Picture URL", description="Optional", validators=[Optional(), URL()]
    )
    price = DecimalField("Price", description="In USD, Optional")


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[email(), InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

    def validate(self, extra_validators=None):
        check_validate = super(LoginForm, self).validate()
        if not check_validate:
            return False

        user = User.query.filter_by(email=self.email.data).first()
        if not user or not check_password_hash(
            user.password, self.password.data
        ):
            self.email.errors.append("Invalid email or password")
            return False
        return True


class SignupForm(FlaskForm):
    email = StringField("Email", validators=[email(), InputRequired()])
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(),
            Length(min=4),
            EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Confirm Password", validators=[InputRequired()])
    store_name = StringField(
        "Store Name", validators=[InputRequired(), Length(min=4)]
    )

    def validate(self, extra_validators=None):
        check_validate = super(SignupForm, self).validate()
        if not check_validate:
            return False

        # Does the user exist already? Must return false,
        # otherwise we'll allow anyone to sign in
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("That email already has an account")
            return False
        return True
