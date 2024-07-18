from datetime import datetime

from app import db


class Offence(db.Model):
    """
    Model representing an offence.
    """

    __tablename__ = "offence"

    offenceId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    offenceDescription = db.Column(db.Text, nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Back populations
    offenders = db.relationship("Offender", back_populates="offence")

    def __repr__(self):
        return (
            f"Offence(offenceId = {self.offenceId}, offenceDescription "
            + f"= {self.offenceDescription})"
        )

    @classmethod
    def create(cls, details={}):
        """
        Create a new offence.
        """
        offence = cls(offenceDescription=details.get("offenceDescription"))
        db.session.add(offence)
        db.session.commit()

        return offence

    def updateDetails(self, details):
        """
        Updates offence
        """
        for key, value in details.items():
            setattr(self, key, value)

        db.session.add(self)
        db.session.commit()

    def getDetails(self):
        return {
            "offenceId": self.offenceId,
            "offenceDescription": self.offenceDescription,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }
