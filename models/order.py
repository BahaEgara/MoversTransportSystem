from datetime import datetime

from app import db
from utilities.email import send_email


class Order(db.Model):
    """
    Model representing an order.
    """

    __tablename__ = "order"

    orderId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    retailerId = db.Column(
        db.Integer, db.ForeignKey("retailer.retailerId"), nullable=False
    )
    farmerId = db.Column(
        db.Integer, db.ForeignKey("farmer.farmerId"), nullable=False
    )
    tripId = db.Column(db.Integer, db.ForeignKey("trip.tripId"), nullable=True)
    orderDate = db.Column(db.Date, nullable=False)
    retailName = db.Column(db.String(100), nullable=False)
    locationAddress = db.Column(db.String(255), nullable=False)
    retailTelephone = db.Column(db.String(15), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Back references
    retailer = db.relationship("Retailer", back_populates="orders")
    farmer = db.relationship("Farmer", back_populates="orders")
    trip = db.relationship("Trip", back_populates="orders")
    orderGoods = db.relationship("OrderGood", back_populates="order")

    def __repr__(self):
        return (
            f"Order(orderId = {self.orderId}, retailName = {self.retailName})"
        )

    @classmethod
    def create(cls, details={}):
        """
        Create a new order.
        """
        order = cls(
            retailerId=details.get("retailerId"),
            farmerId=details.get("farmerId"),
            orderDate=details.get("orderDate"),
            retailName=details.get("retailName"),
            locationAddress=details.get("locationAddress"),
            retailTelephone=details.get("retailTelephone"),
        )
        db.session.add(order)
        db.session.commit()

        subject = f"Confirmation of Successful Order #{order.orderId} Creation"
        send_email(
            [order.farmer.emailAddress],
            subject,
            "emails/order_success",
            farmer=order.farmer,
        )
        return order

    def getDetails(self):
        return {
            "orderId": self.orderId,
            "retailerId": self.retailerId,
            "farmerId": self.farmerId,
            "orderDate": self.orderDate,
            "retailName": self.retailName,
            "locationAddress": self.locationAddress,
            "retailTelephone": self.retailTelephone,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }

    def delete(self):
        db.session.delete(self)
        db.session.commit()
