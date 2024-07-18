import flask
from flask_login import current_user
from flask_login import login_required

from . import drivers
from .forms import GeneralInformationForm
from .forms import UploadProfilePictureForm
from .forms import UpdatePasswordForm
from .forms import UpdateEmailAddressForm
from .forms import UpdatePhoneNumberForm

from utilities.authentication import user_type_validator


@drivers.route("/")
@drivers.route("/dashboard")
@login_required
@user_type_validator("driver")
def dashboard():
    return flask.render_template(
        "drivers/dashboard.html",
    )


# **********************************************************************#
#                                                                       #
#                       ACCOUNT MANAGEMENT                              #
#                                                                       #
# **********************************************************************#
@drivers.route("/account")
@login_required
@user_type_validator("driver")
def view_account():
    return flask.render_template("drivers/view_account.html")


@drivers.route("/account/delete-profile-picture")
@login_required
@user_type_validator("driver")
def delete_profile_picture():
    # Retrieve folder name
    folder = flask.current_app.config["FARMER_PROFILE_UPLOAD_PATH"]

    # Delete profile image
    current_user.deleteProfileImage(folder)

    # Render success message
    flask.flash("Profile picture deleted successfully", "success")
    return flask.redirect(flask.url_for("drivers.account_settings"))


@drivers.route("/account/settings", methods=["GET", "POST"])
@login_required
@user_type_validator("driver")
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
        return flask.redirect(flask.url_for("drivers.account_settings"))

    elif upload_profile_picture_form.validate_on_submit():
        # Retrieve image
        file = upload_profile_picture_form.profileImage.data

        # Save profile image
        folder = flask.current_app.config["FARMER_PROFILE_UPLOAD_PATH"]
        current_user.updateProfileImage(file, folder)

        # Flash success message
        flask.flash("Profile picture updated successfully")
        return flask.redirect(flask.url_for("drivers.account_settings"))

    elif update_password_form.validate_on_submit():
        # Get user input
        oldPassword = (update_password_form.oldPassword.data,)
        newPassword = (update_password_form.newPassword.data,)

        # Save new password
        current_user.updatePassword(oldPassword[0], newPassword[0])

        # Flash success message
        flask.flash("Password updated successfully")
        return flask.redirect(flask.url_for("drivers.account_settings"))

    elif update_email_address_form.validate_on_submit():
        # Retrieve new email address
        newEmailAddress = update_email_address_form.newEmailAddress.data

        # Save new email address
        current_user.updateEmailAddress(newEmailAddress)

        # Flash success message
        flask.flash("Email address updated successfully. Remember to confirm.")
        return flask.redirect(flask.url_for("drivers.account_settings"))

    elif update_phone_number_form.validate_on_submit():
        # Retrieve new phone number
        newPhoneNumber = update_phone_number_form.newPhoneNumber.data

        # Save new phone number
        current_user.updatePhoneNumber(newPhoneNumber)

        # Flash success message
        flask.flash("Phone number updated successfully.")
        return flask.redirect(flask.url_for("drivers.account_settings"))

    # Populate current name
    general_information_form.fullName.data = current_user.fullName

    # Ensure unique ids for csrf tokens
    general_information_form.csrf_token.render_kw = {"id": "general_csrf"}
    update_phone_number_form.csrf_token.render_kw = {"id": "phone_csrf"}
    update_email_address_form.csrf_token.render_kw = {"id": "email_csrf"}
    update_password_form.csrf_token.render_kw = {"id": "password_csrf"}
    upload_profile_picture_form.csrf_token.render_kw = {"id": "photo_csrf"}

    return flask.render_template(
        "drivers/account_settings.html",
        general_information_form=general_information_form,
        upload_profile_picture_form=upload_profile_picture_form,
        update_password_form=update_password_form,
        update_email_address_form=update_email_address_form,
        update_phone_number_form=update_phone_number_form,
    )
