import flask
from flask_login import current_user
from flask_login import login_required

from . import authentication
from .forms import (
    DriverLoginForm,
    LoaderLoginForm,
    AdministratorLoginForm,
    FarmerLoginForm,
    RetailerLoginForm,
    DriverRegistrationForm,
    LoaderRegistrationForm,
    AdministratorRegistrationForm,
    FarmerRegistrationForm,
    RetailerRegistrationForm,
)
from ..models import Driver, Loader, Administrator, Farmer, Retailer
from utilities.authentication import user_type_validator


# ------------------------------------------------------------------------------
#                                 SIGNING IN
# ------------------------------------------------------------------------------
@authentication.route("/driver/login", methods=["GET", "POST"])
def driver_login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("drivers.dashboard"))

    form = DriverLoginForm()
    if form.validate_on_submit():
        driver = Driver.query.filter_by(
            emailAddress=form.emailAddress.data.lower()
        ).first()
        details = {
            "password": form.password.data,
            "remember_me": form.remember_me.data,
        }

        if driver:
            success, message = driver.login(details)
            if success:
                next = flask.request.args.get("next")
                if not next or not next.startswith("/"):
                    next = flask.url_for("drivers.dashboard")

                flask.flash(f"Hello {current_user.firstName}. Welcome back!")
                return flask.redirect(next)

        flask.flash("You provided invalid credentials. Please try again.")
    return flask.render_template("authentication/driver_login.html", form=form)


@authentication.route("/loader/login", methods=["GET", "POST"])
def loader_login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("loaders.dashboard"))

    form = LoaderLoginForm()
    if form.validate_on_submit():
        loader = Loader.query.filter_by(
            emailAddress=form.emailAddress.data.lower()
        ).first()
        details = {
            "password": form.password.data,
            "remember_me": form.remember_me.data,
        }

        if loader:
            success, message = loader.login(details)
            if success:
                next = flask.request.args.get("next")
                if not next or not next.startswith("/"):
                    next = flask.url_for("loaders.dashboard")

                flask.flash(f"Hello {current_user.firstName}. Welcome back!")
                return flask.redirect(next)

        flask.flash("You provided invalid credentials. Please try again.")
    return flask.render_template("authentication/loader_login.html", form=form)


@authentication.route("/administrator/login", methods=["GET", "POST"])
def administrator_login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("administrators.dashboard"))

    form = AdministratorLoginForm()
    if form.validate_on_submit():
        administrator = Administrator.query.filter_by(
            emailAddress=form.emailAddress.data.lower()
        ).first()
        details = {
            "password": form.password.data,
            "remember_me": form.remember_me.data,
        }

        if administrator:
            success, message = administrator.login(details)
            if success:
                next = flask.request.args.get("next")
                if not next or not next.startswith("/"):
                    next = flask.url_for("administrators.dashboard")

                flask.flash(f"Hello {current_user.name}. Welcome back!")
                return flask.redirect(next)

        flask.flash("You provided invalid credentials. Please try again.")
    return flask.render_template(
        "authentication/administrator_login.html", form=form
    )


@authentication.route("/farmer/login", methods=["GET", "POST"])
def farmer_login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("farmers.dashboard"))

    form = FarmerLoginForm()
    if form.validate_on_submit():
        farmer = Farmer.query.filter_by(
            emailAddress=form.emailAddress.data.lower()
        ).first()
        details = {
            "password": form.password.data,
            "remember_me": form.remember_me.data,
        }

        if farmer:
            success, message = farmer.login(details)
            if success:
                next = flask.request.args.get("next")
                if not next or not next.startswith("/"):
                    next = flask.url_for("farmers.dashboard")

                flask.flash(f"Hello {current_user.fullName}. Welcome back!")
                return flask.redirect(next)

        flask.flash("You provided invalid credentials. Please try again.")
    return flask.render_template("authentication/farmer_login.html", form=form)


@authentication.route("/retailer/login", methods=["GET", "POST"])
def retailer_login():
    if current_user.is_authenticated:
        return flask.redirect(flask.url_for("retailers.dashboard"))

    form = RetailerLoginForm()
    if form.validate_on_submit():
        retailer = Retailer.query.filter_by(
            emailAddress=form.emailAddress.data.lower()
        ).first()
        details = {
            "password": form.password.data,
            "remember_me": form.remember_me.data,
        }

        if retailer:
            success, message = retailer.login(details)
            if success:
                next = flask.request.args.get("next")
                if not next or not next.startswith("/"):
                    next = flask.url_for("retailers.dashboard")

                flask.flash(f"Hello {current_user.name}. Welcome back!")
                return flask.redirect(next)

        flask.flash("You provided invalid credentials. Please try again.")
    return flask.render_template(
        "authentication/retailer_login.html", form=form
    )


# ------------------------------------------------------------------------------
#                                REGISTRATION
# ------------------------------------------------------------------------------
@authentication.route("/driver/register", methods=["GET", "POST"])
def driver_registration():
    form = DriverRegistrationForm()
    if form.validate_on_submit():
        details = {
            "firstName": form.firstName.data,
            "lastName": form.lastName.data,
            "gender": form.gender.data,
            "emailAddress": form.emailAddress.data,
            "nationalIdNumber": form.nationalIdNumber.data,
            "licenseId": form.licenseId.data,
            "phoneNumber": form.phoneNumber.data,
            "password": form.password.data,
        }
        Driver.create(details)
        flask.flash("Registration successful. Feel free to login.", "success")
        return flask.redirect(flask.url_for("authentication.driver_login"))
    return flask.render_template(
        "authentication/driver_registration.html", form=form
    )


@authentication.route("/loader/register", methods=["GET", "POST"])
def loader_registration():
    form = LoaderRegistrationForm()
    if form.validate_on_submit():
        details = {
            "firstName": form.firstName.data,
            "lastName": form.lastName.data,
            "gender": form.gender.data,
            "nationalIdNumber": form.nationalIdNumber.data,
            "emailAddress": form.emailAddress.data,
            "phoneNumber": form.phoneNumber.data,
            "password": form.password.data,
        }
        Loader.create(details)
        flask.flash("Registration successful. Feel free to login.", "success")
        return flask.redirect(flask.url_for("authentication.loader_login"))
    return flask.render_template(
        "authentication/loader_registration.html", form=form
    )


@authentication.route("/administrator/register", methods=["GET", "POST"])
def administrator_registration():
    form = AdministratorRegistrationForm()
    if form.validate_on_submit():
        details = {
            "name": form.name.data,
            "gender": form.gender.data,
            "emailAddress": form.emailAddress.data,
            "phoneNumber": form.phoneNumber.data,
            "password": form.password.data,
        }
        Administrator.create(details)
        flask.flash("Registration successful. Feel free to login.", "success")
        return flask.redirect(
            flask.url_for("authentication.administrator_login")
        )
    return flask.render_template(
        "authentication/administrator_registration.html", form=form
    )


@authentication.route("/farmer/register", methods=["GET", "POST"])
def farmer_registration():
    form = FarmerRegistrationForm()
    if form.validate_on_submit():
        details = {
            "fullName": form.name.data,
            "emailAddress": form.emailAddress.data,
            "phoneNumber": form.phoneNumber.data,
            "locationAddress": form.locationAddress.data,
            "natureOfProduce": form.natureOfProduce.data,
            "password": form.password.data,
        }
        Farmer.create(details)
        flask.flash("Registration successful. Feel free to login.", "success")
        return flask.redirect(flask.url_for("authentication.farmer_login"))
    return flask.render_template(
        "authentication/farmer_registration.html", form=form
    )


@authentication.route("/retailer/register", methods=["GET", "POST"])
def retailer_registration():
    form = RetailerRegistrationForm()
    if form.validate_on_submit():
        details = {
            "name": form.name.data,
            "locationAddress": form.locationAddress.data,
            "emailAddress": form.emailAddress.data,
            "phoneNumber": form.phoneNumber.data,
            "password": form.password.data,
        }
        Retailer.create(details)
        flask.flash("Registration successful. Feel free to login.", "success")
        return flask.redirect(flask.url_for("authentication.retailer_login"))
    return flask.render_template(
        "authentication/retailer_registration.html", form=form
    )


# ------------------------------------------------------------------------------
#                                SIGNING OUT
# ------------------------------------------------------------------------------
@authentication.route("/driver/logout")
@login_required
@user_type_validator("driver")
def driver_logout():
    current_user.logout()
    flask.flash("You have been logged out successfully.")
    return flask.redirect(flask.url_for("authentication.driver_login"))


@authentication.route("/loader/logout")
@login_required
@user_type_validator("loader")
def loader_logout():
    current_user.logout()
    flask.flash("You have been logged out successfully.")
    return flask.redirect(flask.url_for("authentication.loader_login"))


@authentication.route("/administrator/logout")
@login_required
@user_type_validator("administrator")
def administrator_logout():
    current_user.logout()
    flask.flash("You have been logged out successfully.")
    return flask.redirect(flask.url_for("authentication.administrator_login"))


@authentication.route("/farmer/logout")
@login_required
@user_type_validator("farmer")
def farmer_logout():
    current_user.logout()
    flask.flash("You have been logged out successfully.")
    return flask.redirect(flask.url_for("authentication.farmer_login"))


@authentication.route("/retailer/logout")
@login_required
@user_type_validator("retailer")
def retailer_logout():
    current_user.logout()
    flask.flash("You have been logged out successfully.")
    return flask.redirect(flask.url_for("authentication.retailer_login"))
