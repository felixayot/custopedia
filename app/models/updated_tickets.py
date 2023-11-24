from app import db
from datetime import datetime


class UpdatedTicket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_ticket_id = db.Column(db.Integer, db.ForeignKey("ticket.id"), nullable=False)
    description = db.Column(db.Text, index=True, nullable=False)
    file_attachments = db.Column(db.String(45))
    updated_at = db.Column(db.DateTime(timezone=True),
                           default=datetime.now)
    original_ticket = db.relationship("Ticket", backref="updated", lazy=True)


    def __repr__(self):
        return ("***Update ID: {}***\n***Ticket Number: {}***\n***Title: {}***"
                .format(self.id, self.original_ticket_id, self.original.title))
