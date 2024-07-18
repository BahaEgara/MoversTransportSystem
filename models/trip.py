from datetime import datetime
from datetime import timedelta

from app import db


class Trip(db.Model):
    """
    Model representing a trip.
    """

    __tablename__ = "trip"

    tripId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tripDate = db.Column(db.DateTime, nullable=False)
    distance = db.Column(db.Float, nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Foreign Keys
    driverId = db.Column(
        db.Integer, db.ForeignKey("driver.driverId"), nullable=False
    )
    vehicleId = db.Column(
        db.Integer, db.ForeignKey("vehicle.vehicleId"), nullable=False
    )

    # Back references
    driver = db.relationship("Driver", back_populates="trips")
    vehicle = db.relationship("Vehicle", back_populates="trips")
    orders = db.relationship("Order", back_populates="trip")
    loader_assignments = db.relationship(
        "LoaderAssignment", back_populates="trip"
    )

    def __repr__(self):
        return (
            f"Trip(tripId = {self.tripId}, tripDate = {self.tripDate}, "
            + f"distance = {self.distance})"
        )

    @classmethod
    def create(cls, details={}):
        """
        Create a new trip.
        """
        trip = cls(
            driverId=details.get("driverId"),
            vehicleId=details.get("vehicleId"),
            tripDate=datetime.now() + timedelta(days=10),
            distance=details.get("distance"),
        )
        db.session.add(trip)
        db.session.commit()

        return trip

    def updateDetails(self, details):
        """
        Updates trip
        """
        for key, value in details.items():
            setattr(self, key, value)

        db.session.add(self)
        db.session.commit()

    def getDetails(self):
        return {
            "tripId": self.tripId,
            "driverId": self.driverId,
            "vehicleId": self.vehicleId,
            "orderId": self.orderId,
            "tripDate": self.tripDate,
            "distance": self.distance,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }
