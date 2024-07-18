import os
import logging
from datetime import datetime

import flask
import flask_login
from flask import url_for
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer

from app import db
from utilities.securities import get_gravatar_hash
from utilities.file_saver import is_allowed_file
from utilities.file_saver import save_image
from utilities.email import send_email


class Farmer(flask_login.UserMixin, db.Model):
    """
    Model representing a farmer.
    """

    __tablename__ = "farmer"

    farmerId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    fullName = db.Column(db.String(120), nullable=False)
    natureOfProduce = db.Column(db.String(255))
    locationAddress = db.Column(db.String(255))
    emailAddress = db.Column(
        db.String(120), unique=True, nullable=False, index=True
    )
    phoneNumber = db.Column(db.String(20), nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    imageURL = db.Column(db.String(255))
    avatarHash = db.Column(db.String(255))
    isActive = db.Column(db.Boolean, default=True)

    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __init__(self, **kwargs):
        super(Farmer, self).__init__(**kwargs)

        # Generate avatar hash
        if self.emailAddress is not None and self.avatarHash is None:
            self.avatarHash = get_gravatar_hash(self.emailAddress)

    # Back references
    orders = db.relationship("Order", back_populates="farmer")

    def __repr__(self):
        return (
            f"Farmer(farmerId = {self.farmerId}, fullName = "
            + f"'{self.fullName}', emailAddress = '{self.emailAddress}')"
        )

    def get_id(self):
        """
        Inherited UserMixin class method used to retrieve user id for
            flask_login
        """
        return self.farmerId

    @classmethod
    def create(cls, details={}):
        """
        Register a new farmer account.
        """
        # Create a new farmer
        farmer = cls(
            fullName=details.get("fullName"),
            emailAddress=details.get("emailAddress"),
            phoneNumber=details.get("phoneNumber"),
            password=details.get("password"),
            natureOfProduce=details.get("natureOfProduce"),
            locationAddress=details.get("locationAddress"),
        )

        # Save details in database
        db.session.add(farmer)
        db.session.commit()

        return farmer

    @property
    def password(self):
        """
        Raise an AttributeError since the password is private only
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        Hash the farmer's password
        """
        self.passwordHash = generate_password_hash(password)

    def activateAccount(self):
        """
        Activate farmer account.

        :return self: Farmer - the activated Farmer instance.
        """
        if not self.isActive:
            self.isActive = True

            db.session.add(self)
            db.session.commit()

        return self

    def deactivateAccount(self):
        """
        Deactivate farmer account.

        :return self: Farmer - the deactivated Farmer instance.
        """
        if self.isActive:
            self.isActive = False

            db.session.add(self)
            db.session.commit()

        return self

    def login(self, details=dict()):
        """
        Authenticates the user and logs them in when provided password is
            valid.

        :param details: dict - Contains password and remember_me boolean
            variable

        :return: tuple - Contains the return status and return message.
        """
        # Set user type session variable
        flask.session.permanent = True
        flask.session["user_type"] = "farmer"

        if self.verifyPassword(details.get("password", "")):
            flask_login.login_user(self, details.get("remember_me", False))
            return (1, "Login Successful")

        return (0, "Invalid password")

    def logout(self):
        """
        Terminate active user session.

        :return: tuple - Contains return status and return message.
        """
        flask_login.logout_user()
        return (1, "Logout successful")

    def verifyPassword(self, password):
        """
        Verify whether the provided password matches the hashed password.

        :param password: str - The password to be verified.

        :return: bool - True if the password is verified, False otherwise
        """
        return check_password_hash(self.passwordHash, password)

    def sendPasswordResetEmail(self):
        """
        Send password reset email to the farmer.
        """
        token = self.generateConfirmationToken()
        reset_link = url_for(
            "accounts.farmer_password_reset",
            token=token,
            _scheme="https",
            _external=True,
        )

        subject = "Password Reset Request"
        send_email(
            [self.emailAddress],
            subject,
            "email/password_reset",
            user=self,
            reset_link=reset_link,
        )

    def sendConfirmationEmail(self):
        """
        Send confirmation email to the farmer.
        """
        token = self.generateConfirmationToken()
        confirmation_link = url_for(
            "accounts.farmer_confirm",
            token=token,
            user_id=self.farmerId,
            _scheme="https",
            _external=True,
        )

        subject = "Email Confirmation"
        send_email(
            [self.emailAddress],
            subject,
            "email/email_confirmation",
            username=f"{self.fullName}",
            confirmation_link=confirmation_link,
        )

    @staticmethod
    def confirmPasswordResetToken(token, expiration=3600):
        """
        Validate password request link provided.
        """
        serializer = Serializer(flask.current_app.config["SECRET_KEY"])

        try:
            data = serializer.loads(token, max_age=expiration)
            farmer = Farmer.query.filter_by(emailAddress=data).first()

            return farmer

        except Exception as e:
            logging.error(
                f"An error occurred while loading the token: {str(e)}"
            )
            return None

    @staticmethod
    def resetPassword(token, new_password, expiration=3600):
        """
        Reset farmer's password.

        :param token: str - the token for password reset.
        :param new_password: str - the new password.
        """
        serializer = Serializer(flask.current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token, expiration)

        except Exception:
            return False

        farmer = Farmer.query.filter_by(emailAddress=data).first()
        if farmer is None:
            return False

        farmer.password = new_password
        db.session.add(farmer)
        db.session.commit()

        return True

    def updatePassword(self, current_password, new_password):
        """
        Updates farmer's password.

        :param current_password: str - Farmer's current password.
        :param new_password: str - Farmer's new password.

        :return self: Farmer - the updated Farmer instance.
        """
        if self.verifyPassword(current_password):
            self.password = new_password
            db.session.commit()

            return self
