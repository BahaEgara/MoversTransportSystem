import flask
from flask_login import current_user
from flask_login import login_required

from . import farmers
from .forms import GeneralInformationForm
from .forms import UploadProfilePictureForm
from .forms import UpdatePasswordForm
from .forms import UpdateEmailAddressForm
from .forms import UpdatePhoneNumberForm
from .forms import CreateOrderForm
from .forms import AssignGoodForm

from ..models import Retailer
from ..models import Order
from ..models import Goods
from ..models import OrderGood

from utilities.authentication import user_type_validator


@farmers.route("/")
@farmers.route("/dashboard")
@login_required
@user_type_validator("farmer")
def dashboard():
    return flask.render_template(
        "farmers/dashboard.html",
    )


@farmers.route("/orders/create", methods=["GET", "POST"])
@login_required
@user_type_validator("farmer")
def create_order():
    form = CreateOrderForm()

    form.retailerId.choices = [
        (retailer.retailerId, retailer.name)
        for retailer in Retailer.query.filter_by().all()
    ]

    if form.validate_on_submit():
        details = {field.name: field.data for field in form}

        details.update({"farmerId": current_user.farmerId})

        getattr(Order, "create")(details)
        flask.flash("Order created successfully", "success")
        return flask.redirect(flask.url_for("farmers.create_order"))
    return flask.render_template("farmers/create_order.html", form=form)


@farmers.route("/orders/<int:order_id>", methods=["GET", "POST"])
@login_required
@user_type_validator("farmer")
def view_order(order_id):
    order = Order.query.get_or_404(order_id)

    # Get goods that are not already assigned to the order
    assigned_good_ids = {og.goodId for og in order.orderGoods}
    available_goods = Goods.query.filter(
        ~Goods.goodId.in_(assigned_good_ids)
    ).all()

    # Create the form and populate choices
    form = AssignGoodForm()
    form.goodId.choices = [
        (good.goodId, good.goodDescription) for good in available_goods
    ]

    if form.validate_on_submit():
        good_id = form.goodId.data
        quantity = form.quantity.data
        unit_price = form.unitPrice.data
        sub_total = float(quantity) * float(unit_price)

        details = {
            "orderId": order.orderId,
            "goodId": good_id,
            "quantity": quantity,
            "unitPrice": unit_price,
            "subTotal": sub_total,
        }
        OrderGood.create(details)
        flask.flash("Good assigned to order successfully", "success")
        return flask.redirect(
            flask.url_for("farmers.view_order", order_id=order_id)
        )
    return flask.render_template(
        "farmers/view_order.html", order=order, form=form
    )


@farmers.route("/orders/<int:order_id>/delete", methods=["POST" , "GET"])
@login_required
@user_type_validator("farmer")
def delete_order(order_id):
    # Retrieve specified order
    order = Order.query.filter_by(orderId=order_id).first_or_404()

    # Delete order record
    order.delete()

    # Redirect user to get orders page
    flask.flash("Order deleted successfully", "success")
    return flask.redirect(flask.url_for("farmers.dashboard"))


# **********************************************************************#
#                                                                       #
#                       ACCOUNT MANAGEMENT                              #
#                                                                       #
# **********************************************************************#
@farmers.route("/account")
@login_required
@user_type_validator("farmer")
def view_account():
    return flask.render_template("farmers/view_account.html")


@farmers.route("/account/delete-profile-picture")
@login_required
@user_type_validator("farmer")
def delete_profile_picture():
    # Retrieve folder name
    folder = flask.current_app.config["FARMER_PROFILE_UPLOAD_PATH"]

    # Delete profile image
    current_user.deleteProfileImage(folder)

    # Render success message
    flask.flash("Profile picture deleted successfully", "success")
    return flask.redirect(
        flask.url_for("farmers.account_settings")
    )


@farmers.route("/account/settings", methods=["GET", "POST"])
@login_required
@user_type_validator("farmer")
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
        return flask.redirect(
            flask.url_for("farmers.account_settings")
        )

    elif upload_profile_picture_form.validate_on_submit():
        # Retrieve image
        file = upload_profile_picture_form.profileImage.data

        # Save profile image
        folder = flask.current_app.config["FARMER_PROFILE_UPLOAD_PATH"]
        current_user.updateProfileImage(file, folder)

        # Flash success message
        flask.flash("Profile picture updated successfully")
        return flask.redirect(
            flask.url_for("farmers.account_settings")
        )

    elif update_password_form.validate_on_submit():
        # Get user input
        oldPassword = (update_password_form.oldPassword.data,)
        newPassword = (update_password_form.newPassword.data,)

        # Save new password
        current_user.updatePassword(oldPassword[0], newPassword[0])

        # Flash success message
        flask.flash("Password updated successfully")
        return flask.redirect(
            flask.url_for("farmers.account_settings")
        )

    elif update_email_address_form.validate_on_submit():
        # Retrieve new email address
        newEmailAddress = update_email_address_form.newEmailAddress.data

        # Save new email address
        current_user.updateEmailAddress(newEmailAddress)

        # Flash success message
        flask.flash("Email address updated successfully. Remember to confirm.")
        return flask.redirect(
            flask.url_for("farmers.account_settings")
        )

    elif update_phone_number_form.validate_on_submit():
        # Retrieve new phone number
        newPhoneNumber = update_phone_number_form.newPhoneNumber.data

        # Save new phone number
        current_user.updatePhoneNumber(newPhoneNumber)

        # Flash success message
        flask.flash("Phone number updated successfully.")
        return flask.redirect(
            flask.url_for("farmers.account_settings")
        )

    # Populate current name
    general_information_form.fullName.data = current_user.fullName

    # Ensure unique ids for csrf tokens
    general_information_form.csrf_token.render_kw = {"id": "general_csrf"}
    update_phone_number_form.csrf_token.render_kw = {"id": "phone_csrf"}
    update_email_address_form.csrf_token.render_kw = {"id": "email_csrf"}
    update_password_form.csrf_token.render_kw = {"id": "password_csrf"}
    upload_profile_picture_form.csrf_token.render_kw = {"id": "photo_csrf"}

    return flask.render_template(
        "farmers/account_settings.html",
        general_information_form=general_information_form,
        upload_profile_picture_form=upload_profile_picture_form,
        update_password_form=update_password_form,
        update_email_address_form=update_email_address_form,
        update_phone_number_form=update_phone_number_form,
    )
