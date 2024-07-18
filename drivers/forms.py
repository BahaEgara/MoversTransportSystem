from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileRequired

from wtforms import StringField
from wtforms import SelectField
from wtforms import SubmitField
from wtforms import DateField
from wtforms import PasswordField
from wtforms import ValidationError

from wtforms.validators import Email
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import DataRequired

from ..models import Driver


class GeneralInformationForm(FlaskForm):
    fullName = StringField(
        "Enter your full name", validators=[DataRequired(), Length(1, 120)]
    )
    submit = SubmitField("Save Changes", render_kw={"id": "general_submit"})


class UploadProfilePictureForm(FlaskForm):
    profileImage = FileField(
        "Select Profile Image",
        validators=[
            FileRequired(),
            FileAllowed({"png", "jpg", "jpeg", "gif"}, "Images only!"),
        ],
    )
    submit = SubmitField("Save", render_kw={"id": "image_submit"})


class UpdatePasswordForm(FlaskForm):
    oldPassword = PasswordField(
        "Old Password",
        validators=[DataRequired()],
        render_kw={"placeholder": "Enter old password"},
    )
    newPassword = PasswordField(
        "New Password",
        validators=[
            DataRequired(),
        ],
        render_kw={"placeholder": "Enter new password"},
    )
    confirmPassword = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("newPassword")],
        render_kw={"placeholder": "Confirm new password"},
    )
    submit = SubmitField("Save Changes", render_kw={"id": "password_submit"})


class UpdateEmailAddressForm(FlaskForm):
    newEmailAddress = StringField(
        "Enter your new email address",
        validators=[DataRequired(), Length(1, 128), Email()],
        render_kw={"placeholder": "Enter your new email address here"},
    )
    submit = SubmitField("Save Changes", render_kw={"id": "email_submit"})

    def validate_newEmailAddress(self, field):
        if Driver.query.filter_by(emailAddress=field.data).first():
            raise ValidationError("Email address is already registered")


class UpdatePhoneNumberForm(FlaskForm):
    newPhoneNumber = StringField("Enter your new phone number")
    submit = SubmitField("Save Changes", render_kw={"id": "phone_submit"})

    def validate_newPhoneNumber(self, field):
        if Driver.query.filter_by(phoneNumber=field.data).first():
            raise ValidationError("Phone number is already registered")


class CreateOrderForm(FlaskForm):
    retailerId = SelectField(
        "Retailer", choices=[], validators=[DataRequired()]
    )
    farmerId = SelectField("Farmer", choices=[], validators=[DataRequired()])
    orderDate = DateField("Order Date", validators=[DataRequired()])
    retailName = StringField("Retail Name", validators=[DataRequired()])
    locationAddress = StringField(
        "Location Address", validators=[DataRequired()]
    )
    retailTelephone = StringField(
        "Retail Telephone", validators=[DataRequired()]
    )
    submit = SubmitField("Create Order")
