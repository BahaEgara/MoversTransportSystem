from datetime import datetime

from app import db


class Vehicle(db.Model):
    """
    Model representing a vehicle.
    """

    __tablename__ = "vehicle"

    vehicleId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    registrationPlate = db.Column(db.String(20), nullable=False, unique=True)
    vehicleMakeId = db.Column(
        db.Integer, db.ForeignKey("vehicleMake.vehicleMakeId")
    )
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Back references
    vehicleMake = db.relationship("VehicleMake", back_populates="vehicles")
    trips = db.relationship("Trip", back_populates="vehicle")
    services = db.relationship("Service", back_populates="vehicle")

    def __repr__(self):
        return (
            f"Vehicle(vehicleId = {self.vehicleId}, registrationPlate "
            + f"= {self.registrationPlate})"
        )

    @classmethod
    def create(cls, details={}):
        """
        Create a new vehicle.
        """
        vehicle = cls(
            registrationPlate=details.get("registrationPlate"),
            vehicleMakeId=details.get("vehicleMakeId"),
        )
        db.session.add(vehicle)
        db.session.commit()

        return vehicle

    def updateDetails(self, details):
        """
        Updates vehicle
        """
        for key, value in details.items():
            setattr(self, key, value)

        db.session.add(self)
        db.session.commit()

    def getDetails(self):
        return {
            "vehicleId": self.vehicleId,
            "registrationPlate": self.registrationPlate,
            "vehicleMakeId": self.vehicleMakeId,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }
