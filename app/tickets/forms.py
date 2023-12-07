"""Defines classes for ticket forms for the app."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, SelectField
from flask_wtf.file import FileField, FileAllowed
from wtforms.validators import DataRequired


class NewticketForm(FlaskForm):
	"""Represents the new ticket form."""
	title = StringField("Title*", validators=[DataRequired()])
	incident_type = SelectField("Incident type*",
							 choices=["Service request", \
				 "Complaint", "Compliment"])
	product = SelectField("Product*", choices=["Product One", \
											"Product Two", "Product Three"])
	product_category = SelectField(u"Product category*",
								choices=["Product category One", \
				 "Product category Two", "Product category Three"])
	description = TextAreaField("Description*", validators=[DataRequired()])
	file_attachments = FileField("Attach document",
							  validators=[FileAllowed(["pdf", "jpg", "png"])])
	submit = SubmitField("Submit your ticket")


class UpdateticketForm(FlaskForm):
	"""Represents the update ticket form."""
	description = TextAreaField("Description*", validators=[DataRequired()])
	file_attachments = FileField("Attach document",
							  validators=[FileAllowed(["pdf", "jpg", "png"])])
	submit = SubmitField("Submit your updated ticket")
