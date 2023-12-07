"""Defines ticket model for the app."""
from app import db
from datetime import datetime


class Ticket(db.Model):
    """Represents a ticket in the app."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(45), index=True, nullable=False)
    incident_type = db.Column(db.String(45), index=True, nullable=False)
    product = db.Column(db.String(45), index=True, nullable=False)
    product_category = db.Column(db.String(45), index=True, nullable=False)
    description = db.Column(db.Text, index=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    file_attachments = db.Column(db.String(45))
    created_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now)
    status = db.Column(db.String(30), index=True, default="Unassigned",
                             nullable=False)
    updated_ticket = db.relationship("UpdatedTicket",
                                     backref="original", lazy=True,
                                     overlaps="updated, original_ticket")

    def __repr__(self):
        """Returns the official string representation of an instance
           of the Ticket class.
        """
        return ("***Ticket Number: {}***\n***Title: {}***"
                .format(self.id, self.title))
