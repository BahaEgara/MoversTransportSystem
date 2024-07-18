from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import BooleanField
from wtforms import SubmitField
from wtforms import ValidationError

from wtforms.validators import Email
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import DataRequired

from ..models import Driver
from ..models import Loader
from ..models import Farmer
from ..models import Retailer
from ..models import Administrator


class DriverLoginForm(FlaskForm):
    emailAddress = StringField(
        "Enter your email address",
        validators=[DataRequired(), Length(1, 128), Email()],
        render_kw={"placeholder": "Enter your email address here"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")


class LoaderLoginForm(FlaskForm):
    emailAddress = StringField(
        "Enter your email address",
        validators=[DataRequired(), Length(1, 128), Email()],
        render_kw={"placeholder": "Enter your email address here"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")


class FarmerLoginForm(FlaskForm):
    emailAddress = StringField(
        "Enter your email address",
        validators=[DataRequired(), Length(1, 128), Email()],
        render_kw={"placeholder": "Enter your email address here"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")


class RetailerLoginForm(FlaskForm):
    emailAddress = StringField(
        "Enter your email address",
        validators=[DataRequired(), Length(1, 128), Email()],
        render_kw={"placeholder": "Enter your email address here"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")


class AdministratorLoginForm(FlaskForm):
    emailAddress = StringField(
        "Enter your email address",
        validators=[DataRequired(), Length(1, 128), Email()],
        render_kw={"placeholder": "Enter your email address here"},
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter password"},
    )
    remember_me = BooleanField("Keep me logged in")
    submit = SubmitField("Login")


class DriverRegistrationForm(FlaskForm):
    # Personal details
    firstName = StringField(
        "Enter first name", validators=[DataRequired(), Length(1, 50)]
    )
    lastName = StringField(
        "Enter last name", validators=[DataRequired(), Length(1, 50)]
    )
    gender = SelectField(
        "Select your gender",
        choices=[("Female", "Female"), ("Male", "Male")],
        validators=[DataRequired()],
    )
    nationalIdNumber = StringField(
        "Enter National ID Number", validators=[DataRequired(), Length(1, 20)]
    )
    licenseId = StringField(
        "Enter License ID", validators=[DataRequired(), Length(1, 20)]
    )

    # Contact details
    emailAddress = StringField(
        "Enter your email address",
        validators=[DataRequired(), Length(1, 120), Email()],
    )
    phoneNumber = StringField(
        "Enter your phone number", validators=[DataRequired(), Length(1, 15)]
    )

    # Security details
    password = PasswordField(
        "Enter your Password",
        validators=[DataRequired()],
        render_kw={"autocomplete": "new-password"},
    )
    confirmPassword = PasswordField(
        "Confirm your password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"autocomplete": "new-password"},
    )

    # Driver consent
    consent = BooleanField(
        "I agree to all statements in Terms of service",
        validators=[DataRequired()],
    )
    submit = SubmitField("Register")

    def validate_emailAddress(self, field):
        if Driver.query.filter_by(emailAddress=field.data.lower()).first():
            raise ValidationError("Email address already registered.")


class LoaderRegistrationForm(FlaskForm):
    # Personal details
    firstName = StringField(
        "Enter first name", validators=[DataRequired(), Length(1, 50)]
    )
    lastName = StringField(
        "Enter last name", validators=[DataRequired(), Length(1, 50)]
    )
    gender = SelectField(
        "Select your gender",
        choices=[("Female", "Female"), ("Male", "Male")],
        validators=[DataRequired()],
    )
    nationalIdNumber = StringField(
        "Enter National ID Number", validators=[DataRequired(), Length(1, 20)]
    )

    # Contact details
    emailAddress = StringField(
        "Enter your email address",
        validators=[DataRequired(), Length(1, 120), Email()],
    )
    phoneNumber = StringField(
        "Enter your phone number", validators=[DataRequired(), Length(1, 15)]
    )

    # Security details
    password = PasswordField(
        "Enter your Password",
        validators=[DataRequired()],
        render_kw={"autocomplete": "new-password"},
    )
    confirmPassword = PasswordField(
        "Confirm your password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"autocomplete": "new-password"},
    )

    # Loader consent
    consent = BooleanField(
        "I agree to all statements in Terms of service",
        validators=[DataRequired()],
    )
    submit = SubmitField("Register")

    def validate_emailAddress(self, field):
        if Loader.query.filter_by(emailAddress=field.data.lower()).first():
            raise ValidationError("Email address already registered.")


class AdministratorRegistrationForm(FlaskForm):
    # Personal details
    name = StringField("Enter full name", validators=[Length(0, 99)])
    gender = SelectField(
        "Select your gender",
        choices=[("Female", "Female"), ("Male", "Male")],
        validators=[DataRequired()],
    )

    # Contact details
    emailAddress = StringField(
        "Enter your email address",
        validators=[DataRequired(), Length(1, 120), Email()],
    )
    phoneNumber = StringField(
        "Enter your phone number", validators=[DataRequired(), Length(1, 15)]
    )

    # Security details
    password = PasswordField(
        "Enter your Password",
        validators=[DataRequired()],
        render_kw={"autocomplete": "new-password"},
    )
    confirmPassword = PasswordField(
        "Confirm your password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"autocomplete": "new-password"},
    )

    # Admin consent
    consent = BooleanField(
        "I agree to all statements in Terms of service",
        validators=[DataRequired()],
    )
    submit = SubmitField("Register")

    def validate_emailAddress(self, field):
        if Administrator.query.filter_by(
            emailAddress=field.data.lower()
        ).first():
            raise ValidationError("Email address already registered.")


class FarmerRegistrationForm(FlaskForm):
    # Personal details
    name = StringField(
        "Enter your name", validators=[DataRequired(), Length(1, 100)]
    )

    # Contact details
    emailAddress = StringField(
        "Enter your email address",
        validators=[DataRequired(), Length(1, 120), Email()],
    )
    phoneNumber = StringField(
        "Enter your phone number", validators=[DataRequired(), Length(1, 15)]
    )
    locationAddress = StringField(
        "Enter your location address", validators=[Length(0, 255)]
    )
    natureOfProduce = StringField(
        "Enter nature of produce", validators=[Length(0, 255)]
    )

    # Security details
    password = PasswordField(
        "Enter your Password",
        validators=[DataRequired()],
        render_kw={"autocomplete": "new-password"},
    )
    confirmPassword = PasswordField(
        "Confirm your password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"autocomplete": "new-password"},
    )

    # Farmer consent
    consent = BooleanField(
        "I agree to all statements in Terms of service",
        validators=[DataRequired()],
    )
    submit = SubmitField("Register")

    def validate_emailAddress(self, field):
        if Farmer.query.filter_by(emailAddress=field.data.lower()).first():
            raise ValidationError("Email address already registered.")


class RetailerRegistrationForm(FlaskForm):
    # Personal details
    name = StringField(
        "Enter your name", validators=[DataRequired(), Length(1, 100)]
    )

    # Contact details
    emailAddress = StringField(
        "Enter your email address",
        validators=[DataRequired(), Length(1, 120), Email()],
    )
    phoneNumber = StringField(
        "Enter your phone number", validators=[DataRequired(), Length(1, 15)]
    )
    locationAddress = StringField(
        "Enter your location address", validators=[Length(0, 255)]
    )

    # Security details
    password = PasswordField(
        "Enter your Password",
        validators=[DataRequired()],
        render_kw={"autocomplete": "new-password"},
    )
    confirmPassword = PasswordField(
        "Confirm your password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"autocomplete": "new-password"},
    )

    # Retailer consent
    consent = BooleanField(
        "I agree to all statements in Terms of service",
        validators=[DataRequired()],
    )
    submit = SubmitField("Register")

    def validate_emailAddress(self, field):
        if Retailer.query.filter_by(emailAddress=field.data.lower()).first():
            raise ValidationError("Email address already registered.")


class PasswordResetForm(FlaskForm):
    password = PasswordField(
        "Enter your Password",
        validators=[
            DataRequired(),
        ],
        render_kw={
            "autocomplete": "new-password",
        },
    )
    confirmPassword = PasswordField(
        "Confirm your password",
        validators=[DataRequired(), EqualTo("password")],
        render_kw={"autocomplete": "new-password"},
    )
    submit = SubmitField("Submit")
