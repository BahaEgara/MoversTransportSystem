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


class Administrator(flask_login.UserMixin, db.Model):
    """
    Model representing an administrator.
    """

    __tablename__ = "administrator"

    administratorId = db.Column(
        db.Integer, primary_key=True, autoincrement=True
    )
    name = db.Column(db.String(100), nullable=False)
    isActive = db.Column(db.Boolean, default=True)
    emailAddress = db.Column(db.String(100), nullable=False, unique=True)
    phoneNumber = db.Column(db.String(15), nullable=False)
    passwordHash = db.Column(db.String(255), nullable=False)
    imageURL = db.Column(db.String(255))
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return (
            f"Administrator(administratorId = {self.administratorId}, "
            + f"name = {self.name})"
        )

    @classmethod
    def create(cls, details={}):
        """
        Create a new administrator.
        """
        administrator = cls(
            name=details.get("name"),
            isActive=details.get("isActive"),
            emailAddress=details.get("emailAddress"),
            phoneNumber=details.get("phoneNumber"),
            password=details.get("password"),
        )
        db.session.add(administrator)
        db.session.commit()

        return administrator

    def get_id(self):
        """
        Inherited UserMixin class method used to retrieve user id for
            flask_login
        """
        return self.administratorId

    def getDetails(self):
        return {
            "administratorId": self.administratorId,
            "name": self.name,
            "isActive": self.isActive,
            "emailAddress": self.emailAddress,
            "phoneNumber": self.phoneNumber,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }

    @property
    def password(self):
        """
        Raise an AttributeError since the password is private only
        """
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        """
        Hash the administrator's password
        """
        self.passwordHash = generate_password_hash(password)

    def activateAccount(self):
        """
        Activate administrator account.

        :return self: Administrator - the activated Administrator instance.
        """
        if not self.isActive:
            self.isActive = True

            db.session.add(self)
            db.session.commit()

        return self

    def deactivateAccount(self):
        """
        Deactivate administrator account.

        :return self: Administrator - the deactivated Administrator instance.
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
        flask.session["user_type"] = "administrator"

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

    def deleteProfileImage(self, folder):
        """
        Deletes administrator's profile image.

        :param folder: str - the folder in which the image will be stored.
        """
        # Delete actual file from the file system
        file_path = os.path.join(folder, self.imageURL)
        os.remove(file_path)

        # Update the same on the database
        self.imageURL = None
        db.session.add(self)
        db.session.commit()

    def updateProfileImage(self, image, folder):
        """
        Update administrator's profile image.

        :param image: FileStorage - the image file to be uploaded.
        :param folder: str - the folder in which the image will be stored.

        :return self: Administrator - the updated Administrator instance.
        """
        if not is_allowed_file(image):
            return (40, "Invalid Image")

        # Save image on file system
        saved_filename = save_image(image, folder)

        # Save filename in database
        self.imageURL = saved_filename
        db.session.add(self)
        db.session.commit()

        return self

    def generateConfirmationToken(self):
        """
        Generate a confirmation token.

        This method generates a token for confirming the user's email address.

        :return: str - The confirmation token.
        """
        serializer = Serializer(flask.current_app.config["SECRET_KEY"])
        return serializer.dumps(self.emailAddress)

    def confirm(self, token, expiration=3600):
        """
        Uses a token to confirm the administrator's email address.

        :param token: str - Contains administrator's email address within it.
        :param expiration: int - Determines the validity of the provided token.

        :return: bool - True if confirmation is successful, False otherwise.
        """
        serializer = Serializer(flask.current_app.config["SECRET_KEY"])

        try:
            data = serializer.loads(token, max_age=expiration)

        except Exception:
            return False

        # Ensure that the link is not corrupted
        if data != self.emailAddress:
            return False

        # Update confirm status
        self.isConfirmed = True
        db.session.commit()

        return True

    def sendPasswordResetEmail(self):
        """
        Send password reset email to the administrator.
        """
        token = self.generateConfirmationToken()
        reset_link = url_for(
            "accounts.administrator_password_reset",
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
        Send confirmation email to the administrator.
        """
        token = self.generateConfirmationToken()
        confirmation_link = url_for(
            "accounts.administrator_confirm",
            token=token,
            user_id=self.administratorId,
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
            administrator = Administrator.query.filter_by(emailAddress=data).first()

            return administrator

        except Exception as e:
            logging.error(
                f"An error occurred while loading the token: {str(e)}"
            )
            return None

    @staticmethod
    def resetPassword(token, new_password, expiration=3600):
        """
        Reset administrator's password.

        :param token: str - the token for password reset.
        :param new_password: str - the new password.
        """
        serializer = Serializer(flask.current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token, expiration)

        except Exception:
            return False

        administrator = Administrator.query.filter_by(emailAddress=data).first()
        if administrator is None:
            return False

        administrator.password = new_password
        db.session.add(administrator)
        db.session.commit()

        return True

    def updatePassword(self, current_password, new_password):
        """
        Updates administrator's password.

        :param current_password: str - Administrator's current password.
        :param new_password: str - Administrator's new password.

        :return self: Administrator - the updated Administrator instance.
        """
        if self.verifyPassword(current_password):
            self.password = new_password
            db.session.commit()

            return self
