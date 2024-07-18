from datetime import datetime

from app import db


class Goods(db.Model):
    """
    Model representing goods.
    """

    __tablename__ = "goods"

    goodId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goodDescription = db.Column(db.String(255), nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Back references
    orderGoods = db.relationship("OrderGood", back_populates="goods")

    def __repr__(self):
        return (
            f"Goods(goodId = {self.goodId}, goodDescription = "
            + f"{self.goodDescription})"
        )

    @classmethod
    def create(cls, details={}):
        """
        Create new goods.
        """
        goods = cls(goodDescription=details.get("goodDescription"))
        db.session.add(goods)
        db.session.commit()

        return goods

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
            "goodId": self.goodId,
            "goodDescription": self.goodDescription,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }
