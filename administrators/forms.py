from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileRequired

from wtforms import StringField
from wtforms import DateField
from wtforms import SubmitField
from wtforms import DecimalField
from wtforms import SelectField
from wtforms import IntegerField
from wtforms.fields import DateTimeField
from wtforms import DateTimeLocalField
from wtforms import PasswordField
from wtforms import ValidationError

from wtforms.validators import Email
from wtforms.validators import NumberRange
from wtforms.validators import Length
from wtforms.validators import EqualTo
from wtforms.validators import DataRequired
from wtforms.widgets import DateInput

from ..models import Administrator
from ..models import Vehicle
from ..models import VehicleMake
from ..models import Goods
from ..models import Offence


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
        if Administrator.query.filter_by(emailAddress=field.data).first():
            raise ValidationError("Email address is already registered")


class UpdatePhoneNumberForm(FlaskForm):
    newPhoneNumber = StringField("Enter your new phone number")
    submit = SubmitField("Save Changes", render_kw={"id": "phone_submit"})

    def validate_newPhoneNumber(self, field):
        if Administrator.query.filter_by(phoneNumber=field.data).first():
            raise ValidationError("Phone number is already registered")


# Custom validators
def Unique(model, field, message="This field must be unique."):
    def _unique(form, field):
        if model.query.filter(
            getattr(model, field.name) == field.data
        ).first():
            raise ValidationError(message)

    return _unique


class RegisterServiceForm(FlaskForm):
    vehicleId = SelectField("Vehicle", choices=[], validators=[DataRequired()])
    cost = DecimalField(
        "Cost", validators=[DataRequired(), NumberRange(min=0)]
    )
    serviceDate = DateInput("Service Date")
    submit = SubmitField("Register Service")


class EditServiceForm(FlaskForm):
    vehicleId = SelectField("Vehicle", choices=[], validators=[DataRequired()])
    cost = DecimalField(
        "Cost", validators=[DataRequired(), NumberRange(min=0)]
    )
    serviceDate = DateTimeField("Service Date", validators=[DataRequired()])
    submit = SubmitField("Edit Service")


# Goods Forms
class RegisterGoodForm(FlaskForm):
    goodDescription = StringField(
        "Description",
        validators=[DataRequired(), Unique(Goods, "goodDescription")],
    )
    submit = SubmitField("Register Good")


class EditGoodForm(FlaskForm):
    goodDescription = StringField("Description", validators=[DataRequired()])
    submit = SubmitField("Edit Good")


# Vehicle Make Forms
class RegisterVehicleMakeForm(FlaskForm):
    makeType = StringField(
        "Make Type",
        validators=[DataRequired(), Unique(VehicleMake, "makeType")],
    )
    loadCapacity = DecimalField(
        "Load Capacity", validators=[DataRequired(), NumberRange(min=0)]
    )
    costPerKm = DecimalField(
        "Cost per KM", validators=[DataRequired(), NumberRange(min=0)]
    )
    numberOfLoaders = IntegerField(
        "Number of Loaders", validators=[DataRequired(), NumberRange(min=0)]
    )
    loaderPayment = DecimalField(
        "Loader Payment", validators=[DataRequired(), NumberRange(min=0)]
    )
    driverPayment = DecimalField(
        "Driver Payment", validators=[DataRequired(), NumberRange(min=0)]
    )
    submit = SubmitField("Register Vehicle Make")


class EditVehicleMakeForm(FlaskForm):
    makeType = StringField("Make Type", validators=[DataRequired()])
    loadCapacity = DecimalField(
        "Load Capacity", validators=[DataRequired(), NumberRange(min=0)]
    )
    costPerKm = DecimalField(
        "Cost per KM", validators=[DataRequired(), NumberRange(min=0)]
    )
    numberOfLoaders = IntegerField(
        "Number of Loaders", validators=[DataRequired(), NumberRange(min=0)]
    )
    loaderPayment = DecimalField(
        "Loader Payment", validators=[DataRequired(), NumberRange(min=0)]
    )
    driverPayment = DecimalField(
        "Driver Payment", validators=[DataRequired(), NumberRange(min=0)]
    )
    submit = SubmitField("Edit Vehicle Make")


# Vehicle Forms
class RegisterVehicleForm(FlaskForm):
    registrationPlate = StringField(
        "Registration Plate",
        validators=[DataRequired(), Unique(Vehicle, "registrationPlate")],
    )
    vehicleMakeId = SelectField(
        "Vehicle Make", choices=[], validators=[DataRequired()]
    )
    submit = SubmitField("Register Vehicle")


class EditVehicleForm(FlaskForm):
    registrationPlate = StringField(
        "Registration Plate", validators=[DataRequired()]
    )
    vehicleMakeId = SelectField(
        "Vehicle Make", choices=[], validators=[DataRequired()]
    )
    submit = SubmitField("Edit Vehicle")


# Offence Forms
class RegisterOffenceForm(FlaskForm):
    offenceDescription = StringField(
        "Offence Description", validators=[DataRequired()]
    )
    submit = SubmitField("Register Offence")


class EditOffenceForm(FlaskForm):
    offenceDescription = StringField(
        "Offence Description", validators=[DataRequired()]
    )
    submit = SubmitField("Edit Offence")


# Trip Forms
class RegisterTripForm(FlaskForm):
    driverId = SelectField("Driver", choices=[], validators=[DataRequired()])
    vehicleId = SelectField("Vehicle", choices=[], validators=[DataRequired()])
    tripDate = DateTimeField("Trip Date", validators=[DataRequired()])
    distance = DecimalField(
        "Distance", validators=[DataRequired(), NumberRange(min=0)]
    )
    submit = SubmitField("Register Trip")


class EditTripForm(FlaskForm):
    driverId = SelectField("Driver", choices=[], validators=[DataRequired()])
    vehicleId = SelectField("Vehicle", choices=[], validators=[DataRequired()])
    tripDate = DateTimeLocalField("Trip Date", validators=[DataRequired()])
    distance = DecimalField(
        "Distance", validators=[DataRequired(), NumberRange(min=0)]
    )
    submit = SubmitField("Edit Trip")


class AssignLoaderForm(FlaskForm):
    loaderId = SelectField(
        "Select Loader", validators=[DataRequired()], coerce=int
    )
    submit = SubmitField("Assign Loader")


class AssignOrderForm(FlaskForm):
    orderId = SelectField(
        "Select Order", validators=[DataRequired()], coerce=int
    )
    submit = SubmitField("Assign Order")


class AddServiceForm(FlaskForm):
    serviceDescription = StringField(
        "Service Description", validators=[DataRequired()]
    )
    serviceDate = DateField(
        "Service Date", format="%Y-%m-%d", validators=[DataRequired()]
    )
    cost = DecimalField("Cost", validators=[DataRequired()])
    submit = SubmitField("Add Service")


class AddOffenceForm(FlaskForm):
    offenceId = SelectField("Offence", validators=[DataRequired()], coerce=int)
    offenceDate = DateField(
        "Offence Date", format="%Y-%m-%d", validators=[DataRequired()]
    )
    submit = SubmitField("Add Offence")

    def __init__(self, *args, **kwargs):
        super(AddOffenceForm, self).__init__(*args, **kwargs)
        self.offenceId.choices = [
            (offence.offenceId, offence.offenceDescription)
            for offence in Offence.query.all()
        ]
