from flask import render_template, url_for, flash, redirect, Blueprint
from app import db, mail
from app.tickets.forms import NewticketForm, UpdateticketForm
from app.models.tickets import Ticket
from app.models.updated_tickets import UpdatedTicket
from flask_login import current_user, login_required
from jinja2 import UndefinedError
from flask_mail import Message
from werkzeug.routing.exceptions import BuildError

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
        # Skip errors if email can't be sent for url build failure,
        #  or connection failure
        try:
            send_new_ticket_email(current_user, ticket)
        except (BuildError, ConnectionRefusedError):
            pass
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
        return render_template("ticket.html", title=ticket.title,
                               ticket=ticket, updated_ticket=updated_ticket)
    # Skip any SQLAlchemy & Jinja2 errors if ticket has no update yet,
    #  or if ticket is new
    except (NameError, UndefinedError):
        pass
    return render_template("ticket.html", title=ticket.title, ticket=ticket)

@tickets.route("/ticket_history/<int:ticket_id>/update",
               methods=["GET", "POST"], strict_slashes=False)
@login_required
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = UpdateticketForm()
    if form.validate_on_submit():
        updated_ticket = UpdatedTicket(description=form.description.data,
                                       original=ticket)
        ticket.status = "Unassigned"
        db.session.add(updated_ticket)
        db.session.commit()
        flash("Your ticket has been updated!", "success")
        try:
            send_ticket_feedback_email(current_user, ticket)
        except BuildError:
            pass
        return redirect(url_for("tickets.view_ticket", ticket_id=ticket.id))
    return render_template("update_ticket.html", title="Update ticket",
                           form=form)

@tickets.route("/ticket_history/<int:ticket_id>/resolve",
               methods=["GET", "POST"], strict_slashes=False)
@login_required
def resolve_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    form = UpdateticketForm()
    if form.validate_on_submit():
        updated_ticket = UpdatedTicket(description=form.description.data,
                                       original=ticket)
        ticket.status = "Resolved"
        db.session.add(updated_ticket)
        db.session.commit()
        flash("You have closed this ticket yourself! \
              It will be marked as resolved.", "success")
        try:
            send_ticket_feedback_email(current_user, ticket)
        except BuildError:
            pass
        return redirect(url_for("tickets.view_ticket", ticket_id=ticket.id))
    return render_template("update_ticket.html", title="Update ticket",
                           form=form)


def send_new_ticket_email(user, ticket):
    msg = Message(subject="{}: Ticket number {}".format(ticket.title, ticket.id),
                sender="support@custopedia.com",
                recipients=[user.email])
    msg.body = f""""Your ticket has been submitted successfully with \
              reference number #{ticket.id}. Our team will work on it \
              within 48 hours. You can track it's progress \
              here {url_for("tickets.ticket_history", _external=True)}

"""
    mail.send(msg)


def send_ticket_feedback_email(user, ticket):
    msg = Message(subject="{}: Ticket number {}".format(ticket.title, ticket.id),
                sender="support@custopedia.com",
                recipients=[user.email])
    msg.body = f""""Your ticket with reference number #{ticket.id} \
                has an update. Find more details
                here {url_for("tickets.view_ticket, ticket_id=ticket.id", _external=True)}

"""
    mail.send(msg)
