import flask
from datetime import datetime
from flask_login import current_user
from flask_login import login_required

from . import administrators
from .forms import GeneralInformationForm
from .forms import UploadProfilePictureForm
from .forms import UpdatePasswordForm
from .forms import UpdateEmailAddressForm
from .forms import UpdatePhoneNumberForm
from .forms import RegisterServiceForm
from .forms import EditServiceForm
from .forms import RegisterGoodForm
from .forms import EditGoodForm
from .forms import RegisterVehicleMakeForm
from .forms import EditVehicleMakeForm
from .forms import RegisterVehicleForm
from .forms import EditVehicleForm
from .forms import RegisterOffenceForm
from .forms import EditOffenceForm
from .forms import RegisterTripForm
from .forms import EditTripForm
from .forms import AssignLoaderForm
from .forms import AssignOrderForm
from .forms import AddServiceForm
from .forms import AddOffenceForm

from app import db
from ..models import Retailer
from ..models import Administrator
from ..models import LoaderAssignment
from ..models import Farmer
from ..models import Goods
from ..models import Offence
from ..models import Service
from ..models import Trip
from ..models import Vehicle
from ..models import Offender
from ..models import VehicleMake
from ..models import Order
from ..models import Loader
from ..models import Driver

from utilities.email import send_email
from utilities.authentication import user_type_validator


@administrators.route("/trips/<int:trip_id>", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def view_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)

    # Forms
    assign_loader_form = AssignLoaderForm()
    assign_order_form = AssignOrderForm()

    # Populate loader choices
    assigned_loader_ids = {
        assignment.loaderId for assignment in trip.loader_assignments
    }
    available_loaders = Loader.query.filter(
        ~Loader.loaderId.in_(assigned_loader_ids)
    ).all()
    assign_loader_form.loaderId.choices = [
        (loader.loaderId, f"{loader.firstName} {loader.lastName}")
        for loader in available_loaders
    ]

    # Populate order choices
    assigned_order_ids = {order.orderId for order in trip.orders}
    available_orders = Order.query.filter(
        ~Order.orderId.in_(assigned_order_ids)
    ).all()
    assign_order_form.orderId.choices = [
        (order.orderId, order.retailName) for order in available_orders
    ]

    if (
        assign_loader_form.validate_on_submit()
        and "assign_loader" in flask.request.form
    ):
        loader_id = assign_loader_form.loaderId.data
        loader_assignment = LoaderAssignment(
            loaderId=loader_id,
            tripId=trip.tripId,
            assignmentDate=datetime.utcnow(),
        )
        db.session.add(loader_assignment)
        db.session.commit()
        flask.flash("Loader assigned to trip successfully", "success")
        return flask.redirect(
            flask.url_for("administrators.view_trip", trip_id=trip_id)
        )

    if (
        assign_order_form.validate_on_submit()
        and "assign_order" in flask.request.form
    ):
        order_id = assign_order_form.orderId.data
        order = Order.query.get_or_404(order_id)
        order.tripId = trip.tripId
        db.session.commit()

        subject = (
            f"Trip #{trip.tripId} Assigned to Your Order "
            + f"#{order.orderId}"
        )
        send_email(
            [order.farmer.emailAddress],
            subject,
            "emails/trip_assignment",
            farmer=order.farmer,
        )
        flask.flash("Order assigned to trip successfully", "success")
        return flask.redirect(
            flask.url_for("administrators.view_trip", trip_id=trip_id)
        )

    return flask.render_template(
        "administrators/view_trip.html",
        trip=trip,
        assign_loader_form=assign_loader_form,
        assign_order_form=assign_order_form,
    )


@administrators.route(
    "/trip/<int:trip_id>/remove_loader/<int:loader_id>", methods=["POST"]
)
@login_required
@user_type_validator("administrator")
def remove_loader_from_trip(trip_id, loader_id):
    loader_assignment = LoaderAssignment.query.filter_by(
        tripId=trip_id, loaderId=loader_id
    ).first_or_404()
    db.session.delete(loader_assignment)
    db.session.commit()
    flask.flash("Loader removed from trip successfully", "success")
    return flask.redirect(
        flask.url_for("administrators.view_trip", trip_id=trip_id)
    )


@administrators.route(
    "/trip/<int:trip_id>/remove_order/<int:order_id>", methods=["POST"]
)
@login_required
@user_type_validator("administrator")
def remove_order_from_trip(trip_id, order_id):
    order = Order.query.filter_by(
        tripId=trip_id, orderId=order_id
    ).first_or_404()
    order.tripId = None
    db.session.commit()
    flask.flash("Order removed from trip successfully", "success")
    return flask.redirect(
        flask.url_for("administrators.view_trip", trip_id=trip_id)
    )


@administrators.route("/")
@administrators.route("/dashboard")
@login_required
@user_type_validator("administrator")
def dashboard():
    return flask.render_template(
        "administrators/dashboard.html",
    )


@administrators.route("/retailers")
@login_required
@user_type_validator("administrator")
def get_retailers():
    retailers = Retailer.query.all()
    return flask.render_template(
        "administrators/get_retailers.html", retailers=retailers
    )


@administrators.route("/farmers")
@login_required
@user_type_validator("administrator")
def get_farmers():
    farmers = Farmer.query.all()
    return flask.render_template(
        "administrators/get_farmers.html", farmers=farmers
    )


@administrators.route("/drivers")
@login_required
@user_type_validator("administrator")
def get_drivers():
    drivers = Driver.query.all()
    return flask.render_template(
        "administrators/get_drivers.html", drivers=drivers
    )


@administrators.route("/goods")
@login_required
@user_type_validator("administrator")
def get_goods():
    goods = Goods.query.all()
    return flask.render_template("administrators/get_goods.html", goods=goods)


@administrators.route("/trips")
@login_required
@user_type_validator("administrator")
def get_trips():
    trips = Trip.query.all()
    return flask.render_template("administrators/get_trips.html", trips=trips)


@administrators.route("/vehicles")
@login_required
@user_type_validator("administrator")
def get_vehicles():
    vehicles = Vehicle.query.all()
    return flask.render_template(
        "administrators/get_vehicles.html", vehicles=vehicles
    )


@administrators.route("/vehicle_makes")
@login_required
@user_type_validator("administrator")
def get_vehicle_makes():
    vehicle_makes = VehicleMake.query.all()
    return flask.render_template(
        "administrators/get_vehicle_makes.html", vehicle_makes=vehicle_makes
    )


@administrators.route("/administrators")
@login_required
@user_type_validator("administrator")
def get_administrators():
    administrators = Administrator.query.all()
    return flask.render_template(
        "administrators/get_administrators.html", administrators=administrators
    )


@administrators.route("/loaders")
@login_required
@user_type_validator("administrator")
def get_loaders():
    loaders = Loader.query.all()
    return flask.render_template(
        "administrators/get_loaders.html", loaders=loaders
    )


@administrators.route("/offences")
@login_required
@user_type_validator("administrator")
def get_offences():
    offences = Offence.query.all()
    return flask.render_template(
        "administrators/get_offences.html", offences=offences
    )


@administrators.route("/orders")
@login_required
@user_type_validator("administrator")
def get_orders():
    orders = Order.query.all()
    return flask.render_template(
        "administrators/get_orders.html", orders=orders
    )


@administrators.route("/services")
@login_required
@user_type_validator("administrator")
def get_services():
    services = Service.query.all()
    return flask.render_template(
        "administrators/get_services.html", services=services
    )


@administrators.route("/loader_assignments")
@login_required
@user_type_validator("administrator")
def get_loader_assignments():
    loader_assignments = LoaderAssignment.query.all()
    return flask.render_template(
        "administrators/get_loader_assignments.html",
        loader_assignments=loader_assignments,
    )


@administrators.route("/retailers/<int:retailer_id>")
@login_required
@user_type_validator("administrator")
def view_retailer(retailer_id):
    retailer = Retailer.query.filter_by(retailerId=retailer_id).first_or_404()
    return flask.render_template(
        "administrators/view_retailer.html", retailer=retailer
    )


@administrators.route("/farmers/<int:farmer_id>")
@login_required
@user_type_validator("administrator")
def view_farmer(farmer_id):
    farmer = Farmer.query.filter_by(farmerId=farmer_id).first_or_404()
    return flask.render_template(
        "administrators/view_farmer.html", farmer=farmer
    )


@administrators.route("/loaders/<int:loader_id>")
@login_required
@user_type_validator("administrator")
def view_loader(loader_id):
    loader = Loader.query.filter_by(loaderId=loader_id).first_or_404()
    return flask.render_template(
        "administrators/view_loader.html", loader=loader
    )


@administrators.route("/orders/<int:order_id>")
@login_required
@user_type_validator("administrator")
def view_order(order_id):
    order = Order.query.filter_by(orderId=order_id).first_or_404()
    return flask.render_template("administrators/view_order.html", order=order)


@administrators.route("/offences/<int:offence_id>/delete", methods=["POST"])
@login_required
@user_type_validator("administrator")
def delete_offence(offence_id):
    # Retrieve specified offence
    offence = Offence.query.filter_by(offenceId=offence_id).first_or_404()

    # Delete offence record
    offence.delete()

    # Redirect user to get offences page
    flask.flash("Trip deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.get_offences"))


@administrators.route("/loaders/<int:loader_id>/delete", methods=["POST"])
@login_required
@user_type_validator("administrator")
def delete_loader(loader_id):
    # Retrieve specified loader
    loader = Loader.query.filter_by(loaderId=loader_id).first_or_404()

    # Delete loader record
    loader.delete()

    # Redirect user to get loaders page
    flask.flash("Trip deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.get_loaders"))


@administrators.route("/farmers/<int:farmer_id>/delete", methods=["POST"])
@login_required
@user_type_validator("administrator")
def delete_farmer(farmer_id):
    # Retrieve specified farmer
    farmer = Trip.query.filter_by(farmerId=farmer_id).first_or_404()

    # Delete farmer record
    farmer.delete()

    # Redirect user to get farmers page
    flask.flash("Trip deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.get_farmers"))


@administrators.route("/trips/<int:trip_id>/delete", methods=["POST"])
@login_required
@user_type_validator("administrator")
def delete_trip(trip_id):
    # Retrieve specified trip
    trip = Trip.query.filter_by(tripId=trip_id).first_or_404()

    # Delete trip record
    trip.delete()

    # Redirect user to get trips page
    flask.flash("Trip deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.get_trips"))


@administrators.route("/drivers/<int:driver_id>/delete", methods=["POST"])
@login_required
@user_type_validator("administrator")
def delete_driver(driver_id):
    # Retrieve specified driver
    driver = Driver.query.filter_by(driverId=driver_id).first_or_404()

    # Delete driver record
    driver.delete()

    # Redirect user to get drivers page
    flask.flash("Driver deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.get_drivers"))


@administrators.route(
    "/vehicle_makes/<int:vehicle_make_id>/delete", methods=["POST"]
)
@login_required
@user_type_validator("administrator")
def delete_vehicle_make(vehicle_make_id):
    # Retrieve specified vehicle make
    vehicle_make = VehicleMake.query.filter_by(
        vehicleMakeId=vehicle_make_id
    ).first_or_404()

    # Delete vehicle make record
    vehicle_make.delete()

    # Redirect user to get vehicle_makes page
    flask.flash("Vehicle make deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.get_vehicle_makes"))


@administrators.route("/vehicles/<int:vehicle_id>/delete", methods=["POST"])
@login_required
@user_type_validator("administrator")
def delete_vehicle(vehicle_id):
    # Retrieve specified vehicle
    vehicle = Vehicle.query.filter_by(vehicleId=vehicle_id).first_or_404()

    # Delete vehicle record
    vehicle.delete()

    # Redirect user to get vehicles page
    flask.flash("Vehicle deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.get_vehicles"))


@administrators.route(
    "/services/<int:service_id>/delete", methods=["GET", "POST"]
)
@login_required
@user_type_validator("administrator")
def delete_service(service_id):
    # Retrieve specified service
    service = Service.query.filter_by(serviceId=service_id).first_or_404()

    # Delete service record
    db.session.delete(service)
    db.session.commit()

    # Redirect user to get services page
    flask.flash("Service deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.get_services"))


@administrators.route("/retailers/<int:retailer_id>/delete", methods=["POST"])
@login_required
@user_type_validator("administrator")
def delete_retailer(retailer_id):
    # Retrieve specified retailer
    retailer = Retailer.query.filter_by(retailerId=retailer_id).first_or_404()

    # Delete retailer record
    retailer.delete()

    # Redirect user to get retailers page
    flask.flash("Retailer deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.get_retailers"))


@administrators.route("/goods/<int:good_id>/delete", methods=["POST"])
@login_required
@user_type_validator("administrator")
def delete_good(good_id):
    # Retrieve specified good
    good = Goods.query.filter_by(goodId=good_id).first_or_404()

    # Delete good record
    good.delete()

    # Redirect user to get goods page
    flask.flash("Goods deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.get_goods"))


# **********************************************************************#
#                                                                       #
#                       ACCOUNT MANAGEMENT                              #
#                                                                       #
# **********************************************************************#
@administrators.route("/account")
@login_required
@user_type_validator("administrator")
def view_account():
    return flask.render_template("administrators/view_account.html")


@administrators.route("/account/delete-profile-picture")
@login_required
@user_type_validator("administrator")
def delete_profile_picture():
    # Retrieve folder name
    folder = flask.current_app.config["FARMER_PROFILE_UPLOAD_PATH"]

    # Delete profile image
    current_user.deleteProfileImage(folder)

    # Render success message
    flask.flash("Profile picture deleted successfully", "success")
    return flask.redirect(flask.url_for("administrators.account_settings"))


@administrators.route("/account/settings", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def account_settings():
    general_information_form = GeneralInformationForm()
    upload_profile_picture_form = UploadProfilePictureForm()
    update_password_form = UpdatePasswordForm()
    update_email_address_form = UpdateEmailAddressForm()
    update_phone_number_form = UpdatePhoneNumberForm()

    if general_information_form.validate_on_submit():
        # Retrieve updated details
        details = {"fullName": general_information_form.fullName.data}

        # Save updated details
        current_user.updateDetails(details)

        # Flash success message
        flask.flash("Profile updated successfully")
        return flask.redirect(flask.url_for("administrators.account_settings"))

    elif upload_profile_picture_form.validate_on_submit():
        # Retrieve image
        file = upload_profile_picture_form.profileImage.data

        # Save profile image
        folder = flask.current_app.config["FARMER_PROFILE_UPLOAD_PATH"]
        current_user.updateProfileImage(file, folder)

        # Flash success message
        flask.flash("Profile picture updated successfully")
        return flask.redirect(flask.url_for("administrators.account_settings"))

    elif update_password_form.validate_on_submit():
        # Get user input
        oldPassword = (update_password_form.oldPassword.data,)
        newPassword = (update_password_form.newPassword.data,)

        # Save new password
        current_user.updatePassword(oldPassword[0], newPassword[0])

        # Flash success message
        flask.flash("Password updated successfully")
        return flask.redirect(flask.url_for("administrators.account_settings"))

    elif update_email_address_form.validate_on_submit():
        # Retrieve new email address
        newEmailAddress = update_email_address_form.newEmailAddress.data

        # Save new email address
        current_user.updateEmailAddress(newEmailAddress)

        # Flash success message
        flask.flash("Email address updated successfully. Remember to confirm.")
        return flask.redirect(flask.url_for("administrators.account_settings"))

    elif update_phone_number_form.validate_on_submit():
        # Retrieve new phone number
        newPhoneNumber = update_phone_number_form.newPhoneNumber.data

        # Save new phone number
        current_user.updatePhoneNumber(newPhoneNumber)

        # Flash success message
        flask.flash("Phone number updated successfully.")
        return flask.redirect(flask.url_for("administrators.account_settings"))

    # Populate current name
    general_information_form.fullName.data = current_user.fullName

    # Ensure unique ids for csrf tokens
    general_information_form.csrf_token.render_kw = {"id": "general_csrf"}
    update_phone_number_form.csrf_token.render_kw = {"id": "phone_csrf"}
    update_email_address_form.csrf_token.render_kw = {"id": "email_csrf"}
    update_password_form.csrf_token.render_kw = {"id": "password_csrf"}
    upload_profile_picture_form.csrf_token.render_kw = {"id": "photo_csrf"}

    return flask.render_template(
        "administrators/account_settings.html",
        general_information_form=general_information_form,
        upload_profile_picture_form=upload_profile_picture_form,
        update_password_form=update_password_form,
        update_email_address_form=update_email_address_form,
        update_phone_number_form=update_phone_number_form,
    )


# Register and Edit Service
@administrators.route("/services/register", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def register_service():
    form = RegisterServiceForm()
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        getattr(Service, "create")(details)
        flask.flash("Service registered successfully", "success")
        return flask.redirect(flask.url_for("administrators.register_service"))
    return flask.render_template(
        "administrators/register_service.html", form=form
    )


@administrators.route(
    "/services/<int:service_id>/edit", methods=["GET", "POST"]
)
@login_required
@user_type_validator("administrator")
def edit_service(service_id):
    service = Service.query.get_or_404(service_id)
    form = EditServiceForm(obj=service)
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        service.updateDetails(details)
        flask.flash("Service updated successfully", "success")
        return flask.redirect(flask.url_for("administrators.services"))
    return flask.render_template("administrators/edit_service.html", form=form)


# Register and Edit Goods
@administrators.route("/goods/register", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def register_good():
    form = RegisterGoodForm()
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        getattr(Goods, "create")(details)
        flask.flash("Good registered successfully", "success")
        return flask.redirect(flask.url_for("administrators.register_good"))
    return flask.render_template(
        "administrators/register_good.html", form=form
    )


@administrators.route("/goods/<int:good_id>/edit", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def edit_good(good_id):
    good = Goods.query.get_or_404(good_id)
    form = EditGoodForm(obj=good)
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        good.updateDetails(details)
        flask.flash("Good updated successfully", "success")
        return flask.redirect(flask.url_for("administrators.goods"))
    return flask.render_template("administrators/edit_good.html", form=form)


# Register and Edit Vehicle Make
@administrators.route("/vehicle-makes/register", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def register_vehicle_make():
    form = RegisterVehicleMakeForm()
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        getattr(VehicleMake, "create")(details)
        flask.flash("Vehicle Make registered successfully", "success")
        return flask.redirect(
            flask.url_for("administrators.register_vehicle_make")
        )
    return flask.render_template(
        "administrators/register_vehicle_make.html", form=form
    )


@administrators.route(
    "/vehicle-makes/<int:vehicle_make_id>/edit", methods=["GET", "POST"]
)
@login_required
@user_type_validator("administrator")
def edit_vehicle_make(vehicle_make_id):
    vehicle_make = VehicleMake.query.get_or_404(vehicle_make_id)
    form = EditVehicleMakeForm(obj=vehicle_make)
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        vehicle_make.updateDetails(details)
        flask.flash("Vehicle Make updated successfully", "success")
        return flask.redirect(flask.url_for("administrators.vehicle_makes"))
    return flask.render_template(
        "administrators/edit_vehicle_make.html", form=form
    )


# Register and Edit Vehicle
@administrators.route("/vehicles/register", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def register_vehicle():
    form = RegisterVehicleForm()
    form.vehicleMakeId.choices = [
        (make.vehicleMakeId, make.makeType) for make in VehicleMake.query.all()
    ]
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        getattr(Vehicle, "create")(details)
        flask.flash("Vehicle registered successfully", "success")
        return flask.redirect(flask.url_for("administrators.register_vehicle"))
    return flask.render_template(
        "administrators/register_vehicle.html", form=form
    )


@administrators.route(
    "/vehicles/<int:vehicle_id>/edit", methods=["GET", "POST"]
)
@login_required
@user_type_validator("administrator")
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    form = EditVehicleForm(obj=vehicle)
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        vehicle.updateDetails(details)
        flask.flash("Vehicle updated successfully", "success")
        return flask.redirect(flask.url_for("administrators.vehicles"))
    return flask.render_template("administrators/edit_vehicle.html", form=form)


# Register and Edit Offence
@administrators.route("/offences/register", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def register_offence():
    form = RegisterOffenceForm()
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        getattr(Offence, "create")(details)
        flask.flash("Offence registered successfully", "success")
        return flask.redirect(flask.url_for("administrators.register_offence"))
    return flask.render_template(
        "administrators/register_offence.html", form=form
    )


@administrators.route(
    "/offences/<int:offence_id>/edit", methods=["GET", "POST"]
)
@login_required
@user_type_validator("administrator")
def edit_offence(offence_id):
    offence = Offence.query.get_or_404(offence_id)
    form = EditOffenceForm(obj=offence)
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        offence.updateDetails(details)
        flask.flash("Offence updated successfully", "success")
        return flask.redirect(flask.url_for("administrators.offences"))
    return flask.render_template("administrators/edit_offence.html", form=form)


# Register and Edit Trip
@administrators.route("/trips/register", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def register_trip():
    form = RegisterTripForm()

    form.vehicleId.choices = [
        (vehicle.vehicleId, vehicle.registrationPlate)
        for vehicle in Vehicle.query.all()
    ]

    form.driverId.choices = [
        (driver.driverId, f"{driver.firstName} {driver.lastName}")
        for driver in Driver.query.all()
    ]
    print({field.name: field.data for field in form})
    if flask.request.method == "POST":
        details = {field.name: field.data for field in form}
        getattr(Trip, "create")(details)
        flask.flash("Trip registered successfully", "success")
        return flask.redirect(flask.url_for("administrators.register_trip"))
    return flask.render_template(
        "administrators/register_trip.html", form=form
    )


@administrators.route("/trips/<int:trip_id>/edit", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def edit_trip(trip_id):
    trip = Trip.query.get_or_404(trip_id)
    form = EditTripForm(obj=trip)
    if form.validate_on_submit():
        details = {field.name: field.data for field in form}
        trip.updateDetails(details)
        flask.flash("Trip updated successfully", "success")
        return flask.redirect(flask.url_for("administrators.trips"))
    return flask.render_template("administrators/edit_trip.html", form=form)


@administrators.route("/vehicles/<int:vehicle_id>", methods=["GET", "POST"])
@login_required
@user_type_validator("administrator")
def view_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    # Form
    add_service_form = AddServiceForm()

    if add_service_form.validate_on_submit():
        service = Service(
            vehicleId=vehicle.vehicleId,
            serviceDescription=add_service_form.serviceDescription.data,
            serviceDate=add_service_form.serviceDate.data,
            cost=add_service_form.cost.data,
        )
        db.session.add(service)
        db.session.commit()

        flask.flash("Service added successfully", "success")
        return flask.redirect(
            flask.url_for(
                "administrators.view_vehicle", vehicle_id=vehicle.vehicleId
            )
        )

    return flask.render_template(
        "administrators/view_vehicle.html",
        vehicle=vehicle,
        add_service_form=add_service_form,
    )


@administrators.route("/driver/<int:driver_id>", methods=["GET", "POST"])
def view_driver(driver_id):
    driver = Driver.query.get_or_404(driver_id)

    # Form
    add_offence_form = AddOffenceForm()

    if add_offence_form.validate_on_submit():
        new_offence = Offender(
            driverId=driver.driverId,
            offenceId=add_offence_form.offenceId.data,
            offenceDate=add_offence_form.offenceDate.data,
        )
        if len(driver.offenders) >= 3:
            driver.isActive = False
            flask.flash("Driver deactivated", "success")

        db.session.add(driver)
        db.session.add(new_offence)
        db.session.commit()

        flask.flash("Offence added successfully", "success")
        return flask.redirect(
            flask.url_for(
                "administrators.view_driver", driver_id=driver.driverId
            )
        )

    if (
        flask.request.method == "POST"
        and "delete_offence" in flask.request.form
    ):
        offender_id = flask.request.form.get("delete_offence")
        offender = Offender.query.get_or_404(offender_id)
        db.session.delete(offender)
        db.session.commit()

        flask.flash("Offence deleted successfully", "success")
        return flask.redirect(
            flask.url_for(
                "administrators.view_driver", driver_id=driver.driverId
            )
        )

    return flask.render_template(
        "administrators/view_driver.html",
        driver=driver,
        add_offence_form=add_offence_form,
    )
