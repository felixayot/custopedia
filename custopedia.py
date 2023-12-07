"""Creates an instance of the flask app
   and a shell context with the db schemas.
"""
from app import create_app, db
from app.models.users import User
from app.models.tickets import Ticket
from app.models.updated_tickets import UpdatedTicket


app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Returns a dictionary of the database schemas in the flask shell."""
    return {"db": db, "User": User, "Ticket": Ticket, "UpdatedTicket": UpdatedTicket}
