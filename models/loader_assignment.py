from datetime import datetime

from sqlalchemy.exc import IntegrityError

from app import db


class LoaderAssignment(db.Model):
    """
    Model representing a loader assignment.
    """

    __tablename__ = "loader_assignment"

    assignmentId = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assignmentDate = db.Column(db.DateTime, nullable=False)
    dateCreated = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdated = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # Foreign Keys
    loaderId = db.Column(db.Integer, db.ForeignKey("loader.loaderId"), nullable=False)
    tripId = db.Column(db.Integer, db.ForeignKey("trip.tripId"), nullable=False)

    # Back references
    loader = db.relationship("Loader", back_populates="loader_assignments")
    trip = db.relationship("Trip", back_populates="loader_assignments")

    def __repr__(self):
        return f"LoaderAssignment(assignmentId = {self.assignmentId}, assignmentDate = {self.assignmentDate})"

    @classmethod
    def create(cls, details={}):
        """
        Create a new loader assignment.
        """
        assignment = cls(
            loaderId=details.get("loaderId"),
            tripId=details.get("tripId"),
            assignmentDate=details.get("assignmentDate"),
        )
        db.session.add(assignment)
        db.session.commit()

        return assignment

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
            "assignmentId": self.assignmentId,
            "loaderId": self.loaderId,
            "tripId": self.tripId,
            "assignmentDate": self.assignmentDate,
            "dateCreated": self.dateCreated,
            "lastUpdated": self.lastUpdated,
        }

