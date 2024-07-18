from datetime import datetime
from datetime import timedelta

from app import db


class Offender(db.Model):
    """
    Model representing an offender.
    """

    __tablename__ = "offender"

    offenderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    offenceDate = db.Column(db.Date, nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Foreign Keys
    driverId = db.Column(
        db.Integer, db.ForeignKey("driver.driverId"), nullable=False
    )
    offenceId = db.Column(
        db.Integer, db.ForeignKey("offence.offenceId"), nullable=False
    )

    # Back references
    driver = db.relationship("Driver", back_populates="offenders")
    offence = db.relationship("Offence", back_populates="offenders")

    def __repr__(self):
        return (
            f"Offender(offenderId = {self.offenderId}, offenceDate = "
            + f"{self.offenceDate})"
        )

    @classmethod
    def create(cls, details={}):
        """
        Create a new offender.
        """
        offender = cls(
            driverId=details.get("driverId"),
            offenceId=details.get("offenceId"),
            offenceDate=details.get("offenceDate"),
        )
        db.session.add(offender)
        db.session.commit()

        # Check if the driver should be deactivated
        cls.check_deactivate_driver(details.get("driverId"))

        return offender

    @classmethod
    def check_deactivate_driver(cls, driver_id):
        """
        Check if the driver should be deactivated based on offence count
            and timing.
        """
        three_months_ago = datetime.utcnow() - timedelta(days=90)
        offences_count = Offender.query.filter(
            Offender.driverId == driver_id,
            Offender.offenceDate >= three_months_ago,
        ).count()

        if offences_count >= 3:
            driver = cls.query.get(driver_id)
            driver.isActive = False
            db.session.commit()

    def updateDetails(self, details):
        """
        Updates offender
        """
        for key, value in details.items():
            setattr(self, key, value)

        db.session.add(self)
        db.session.commit()

    def getDetails(self):
        return {
            "offenderId": self.offenderId,
            "driverId": self.driverId,
            "offenceId": self.offenceId,
            "offenceDate": self.offenceDate,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }
