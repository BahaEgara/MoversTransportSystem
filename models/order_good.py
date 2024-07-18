from datetime import datetime

from app import db


class OrderGood(db.Model):
    """
    Model representing an order good.
    """

    __tablename__ = "orderGood"

    orderGoodId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    orderId = db.Column(
        db.Integer, db.ForeignKey("order.orderId"), nullable=False
    )
    goodId = db.Column(
        db.Integer, db.ForeignKey("goods.goodId"), nullable=False
    )
    quantity = db.Column(db.Numeric(10, 2), nullable=False)
    unitPrice = db.Column(db.Numeric(10, 2), nullable=False)
    subTotal = db.Column(db.Numeric(10, 2), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Back references
    order = db.relationship("Order", back_populates="orderGoods")
    goods = db.relationship("Goods", back_populates="orderGoods")

    def __repr__(self):
        return (
            f"OrderGood(orderGoodId = {self.orderGoodId}, "
            + f"quantity = {self.quantity})"
        )

    @classmethod
    def create(cls, details={}):
        """
        Create a new order good.
        """
        orderGood = cls(
            orderId=details.get("orderId"),
            goodId=details.get("goodId"),
            quantity=details.get("quantity"),
            unitPrice=details.get("unitPrice"),
            subTotal=details.get("subTotal"),
        )
        db.session.add(orderGood)
        db.session.commit()

        return orderGood

    def updateDetails(self, details):
        """
        Updates goods
        """
        for key, value in details.items():
            setattr(self, key, value)

        db.session.add(self)
        db.session.commit()

    def getDetails(self):
        return {
            "orderGoodId": self.orderGoodId,
            "orderId": self.orderId,
            "goodId": self.goodId,
            "quantity": self.quantity,
            "unitPrice": self.unitPrice,
            "subTotal": self.subTotal,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }
