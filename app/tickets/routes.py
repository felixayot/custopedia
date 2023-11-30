from flask import render_template, url_for, flash, redirect, Blueprint
from app import db
from app.tickets.forms import NewticketForm, UpdateticketForm
from app.models.tickets import Ticket
from app.models.updated_tickets import UpdatedTicket
from flask_login import current_user, login_required
from jinja2 import UndefinedError

tickets = Blueprint("tickets", __name__)


@tickets.route("/new_ticket", methods=["GET", "POST"], strict_slashes=False)
@login_required
def new_ticket():
    form = NewticketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data,
                        incident_type=form.incident_type.data,
                        product=form.product.data,
                        product_category=form.product_category.data,
                        description=form.description.data, owner=current_user)
        db.session.add(ticket)
        db.session.commit()
        flash("Your ticket has been submitted successfully with \
              reference number #{}. Our team will work on it \
              within 48 hours. You can track it's progress \
              in the Tickets History tab.".format(ticket.id), "success")
        return redirect(url_for("tickets.new_ticket"))
    return render_template("new_ticket.html",
                           title="Create a ticket", form=form)

@tickets.route("/ticket_history", strict_slashes=False)
@login_required
def ticket_history():
        tickets = Ticket.query.all()
        return render_template("ticket_history.html",
                               title="Ticket History", tickets=tickets)

@tickets.route("/ticket_history/<int:ticket_id>", strict_slashes=False)
@login_required
def view_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    try:
        updated_ticket = UpdatedTicket.query.get(ticket_id)
        return render_template("ticket.html", title=ticket.title, ticket=ticket, updated_ticket=updated_ticket)
    # Skip any SQLAlchemy errors if ticket has no update yet, or if ticket is new
    except (NameError, UndefinedError):
        pass
    return render_template("ticket.html", title=ticket.title, ticket=ticket) 

@tickets.route("/ticket_history/<int:ticket_id>/update", methods=["GET", "POST"], strict_slashes=False)
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = UpdateticketForm()
    if form.validate_on_submit():
        updated_ticket = UpdatedTicket(description=form.description.data, original=ticket)
        ticket.status = "Unassigned"
        db.session.add(updated_ticket)
        db.session.commit()
        flash("Your ticket has been updated!", "success")
        return redirect(url_for("tickets.view_ticket", ticket_id=ticket.id))
    return render_template("update_ticket.html", title="Update ticket", form=form)

@tickets.route("/ticket_history/<int:ticket_id>/resolve", methods=["GET", "POST"], strict_slashes=False)
@login_required
def resolve_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = UpdateticketForm()
    if form.validate_on_submit():
        updated_ticket = UpdatedTicket(description=form.description.data, original=ticket)
        ticket.status = "Resolved"
        db.session.add(updated_ticket)
        db.session.commit()
        flash("You have closed this ticket yourself! It will be marked as resolved.", "success")
        return redirect(url_for("tickets.view_ticket", ticket_id=ticket.id))
    return render_template("update_ticket.html", title="Update ticket", form=form)
