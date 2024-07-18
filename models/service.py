from datetime import datetime

from app import db


class Service(db.Model):
    """
    Model representing a service.
    """

    __tablename__ = "service"

    serviceId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicleId = db.Column(
        db.Integer, db.ForeignKey("vehicle.vehicleId"), nullable=False
    )
    serviceDescription = db.Column(db.String(255))
    cost = db.Column(db.Numeric(10, 2), nullable=False)
    serviceDate = db.Column(db.DateTime, nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Back references
    vehicle = db.relationship("Vehicle", back_populates="services")

    def __repr__(self):
        return f"Service(serviceId = {self.serviceId}, cost = {self.cost})"

    @classmethod
    def create(cls, details={}):
        """
        Create a new service.
        """
        service = cls(
            vehicleId=details.get("vehicleId"),
            cost=details.get("cost"),
            serviceDate=details.get("serviceDate"),
            serviceDescription=details.get("serviceDescription"),
        )
        db.session.add(service)
        db.session.commit()

        return service

    def updateDetails(self, details):
        """
        Updates service
        """
        for key, value in details.items():
            setattr(self, key, value)

        db.session.add(self)
        db.session.commit()

    def getDetails(self):
        return {
            "serviceId": self.serviceId,
            "vehicleId": self.vehicleId,
            "cost": self.cost,
            "serviceDate": self.serviceDate,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }
