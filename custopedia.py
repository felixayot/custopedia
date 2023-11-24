from app import create_app, db
from app.models.users import User
from app.models.tickets import Ticket
from app.models.updated_tickets import UpdatedTicket


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": User, "Ticket": Ticket, "UpdatedTicket": UpdatedTicket}
