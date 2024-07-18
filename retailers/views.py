import flask
from flask_login import login_required

from . import retailers
from utilities.email import send_email
from utilities.authentication import user_type_validator
from ..models import Order


@retailers.route("/")
@retailers.route("/dashboard")
@login_required
@user_type_validator("retailer")
def dashboard():
    return flask.render_template(
        "retailers/dashboard.html",
    )


# **********************************************************************#
#                                                                       #
#                       ACCOUNT MANAGEMENT                              #
#                                                                       #
# **********************************************************************#
@retailers.route("/account")
@login_required
@user_type_validator("retailer")
def view_account():
    return flask.render_template("retailers/view_account.html")


@retailers.route("/orders/<int:order_id>/confirm")
@login_required
@user_type_validator("retailer")
def confirm_order_receipt(order_id):
    order = Order.query.get(order_id)
    if order:
        subject = (
            f"Confirmation of Order #{order.orderId} Delivery to Retailer"
        )
        send_email(
            [order.farmer.emailAddress],
            subject,
            "emails/confirm_order_receipt",
            farmer=order.farmer,
        )
        flask.flash("Confirmation email sent successfully", "success")
    return flask.redirect(flask.url_for("retailers.dashboard"))
