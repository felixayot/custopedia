"""Defines updated ticket model for the app."""
from app import db
from datetime import datetime


class UpdatedTicket(db.Model):
    """Represents an updated ticket in the app."""
    id = db.Column(db.Integer, primary_key=True)
    original_ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.id"),
                                   nullable=False)
    description = db.Column(db.Text, index=True, nullable=False)
    file_attachments = db.Column(db.String(45))
    updated_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now)
    original_ticket = db.relationship("Ticket", backref="updated", lazy=True,
                                      overlaps="original, updated_ticket")


    def __repr__(self):
        """Returns the official string representation of an instance
           of the UpdatedTicket class.
        """
        return ("***Update ID: {}***\n***Ticket Number: {}***\n***Title: {}***"
                .format(self.id, self.original_ticket_id, self.original.title))
