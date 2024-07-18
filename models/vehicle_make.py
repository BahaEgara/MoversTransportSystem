from datetime import datetime

from app import db


class VehicleMake(db.Model):
    """
    Model representing a vehicle make.
    """

    __tablename__ = "vehicleMake"

    vehicleMakeId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    makeType = db.Column(db.String(50))
    loadCapacity = db.Column(db.Numeric(10, 2))
    costPerKm = db.Column(db.Numeric(10, 2))
    numberOfLoaders = db.Column(db.Integer)
    loaderPayment = db.Column(db.Numeric(10, 2))
    driverPayment = db.Column(db.Numeric(10, 2))
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Back references
    vehicles = db.relationship("Vehicle", back_populates="vehicleMake")

    def __repr__(self):
        return (
            f"VehicleMake(vehicleMakeId = {self.vehicleMakeId}, "
            + f"makeType = {self.makeType})"
        )

    @classmethod
    def create(cls, details={}):
        """
        Create a new vehicle make.
        """
        vehicleMake = cls(
            makeType=details.get("makeType"),
            loadCapacity=details.get("loadCapacity"),
            costPerKm=details.get("costPerKm"),
            numberOfLoaders=details.get("numberOfLoaders"),
            loaderPayment=details.get("loaderPayment"),
            driverPayment=details.get("driverPayment"),
        )
        db.session.add(vehicleMake)
        db.session.commit()

        return vehicleMake

    def updateDetails(self, details):
        """
        Updates vehicle make
        """
        for key, value in details.items():
            setattr(self, key, value)

        db.session.add(self)
        db.session.commit()

    def getDetails(self):
        return {
            "vehicleMakeId": self.vehicleMakeId,
            "makeType": self.makeType,
            "loadCapacity": self.loadCapacity,
            "costPerKm": self.costPerKm,
            "numberOfLoaders": self.numberOfLoaders,
            "loaderPayment": self.loaderPayment,
            "driverPayment": self.driverPayment,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }
