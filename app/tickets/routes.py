"""Instantiates the Blueprint and defines the views for app tickets."""
import os
from flask import render_template, url_for, flash, redirect, \
    current_app, send_file, Blueprint
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
    """Defines the logic for user ticket creation
       and returns the create ticket page.
    """
    form = NewticketForm()
    if form.validate_on_submit():
        ticket = Ticket(title=form.title.data,
                        incident_type=form.incident_type.data,
                        product=form.product.data,
                        product_category=form.product_category.data,
                        description=form.description.data, owner=current_user)
        if form.file_attachments.data:
            file = save_file(form.file_attachments.data)
            ticket.file_attachments = file
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
    """Returns the tickets history/list page."""
    tickets = Ticket.query.all()
    return render_template("ticket_history.html",
                               title="Ticket History", tickets=tickets)

@tickets.route("/ticket_history/<int:ticket_id>", strict_slashes=False)
@login_required
def view_ticket(ticket_id):
    """Returns the page for a ticket identified by a given ticket id."""
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
    """Defines the logic for updating a ticket
       and returns the update ticket page.
    """
    ticket = Ticket.query.get_or_404(ticket_id)
    form = UpdateticketForm()
    if form.validate_on_submit():
        updated_ticket = UpdatedTicket(description=form.description.data,
                                       original=ticket)
        ticket.status = "Unassigned"
        if form.file_attachments.data:
            file = save_file(form.file_attachments.data)
            updated_ticket.file_attachments = file
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
    """Defines the logic for withdrawing/resolving a ticket
       and returns the resolve ticket page.
    """
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


@tickets.route("/file_attachments/<file>", strict_slashes=False)
@login_required
def view_file(file):
    """Returns a page displaying the file attachment queried by the user."""
    try:
        return send_file(os.path.join(current_app.root_path, "static/user_file_attachments", file))
    except Exception as e:
        return render_template("errors/404.html"), 404


def save_file(form_file):
    """Defines the logic to save a file attached by the user in the ticket."""
    fn = form_file.filename
    file_path = os.path.join(current_app.root_path, "static/user_file_attachments", fn)
    form_file.save(file_path)
    return fn


def send_new_ticket_email(user, ticket):
    """
    Sends an email to the user to notify
    them of the ticket they just raised.
    """
    msg = Message(subject="{}: Ticket number {}".format(ticket.title, ticket.id),
                sender="support@custopedia.com",
                recipients=[user.email])
    msg.body = f"""Your ticket has been submitted successfully with reference number #{ticket.id}. 

Our team will work on it within 48 hours. You can track it's progress here {url_for("tickets.ticket_history", _external=True)}

"""
    mail.send(msg)


def send_ticket_feedback_email(user, ticket):
    """Sends an email to the user to notify
       them that a ticket has been updated.
    """
    msg = Message(subject="{}: Ticket number {}".format(ticket.title, ticket.id),
                sender="support@custopedia.com",
                recipients=[user.email])
    msg.body = f"""Your ticket with reference number #{ticket.id} has an update.

Find more details here {url_for("tickets.view_ticket, ticket_id=ticket.id", _external=True)}

"""
    mail.send(msg)
