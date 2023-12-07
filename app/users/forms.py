"""Defines classes for user forms for the app."""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, \
	EqualTo, ValidationError
from app.models.users import User


class RegisterForm(FlaskForm):
	"""Represents the user registration form."""
	first_name = StringField("First name*", validators=[DataRequired()])
	last_name = StringField("Last name*", validators=[DataRequired()])
	email = StringField("Email*", validators=[DataRequired(), Email()])
	phone_number = StringField("Mobile Phone*", validators=[DataRequired()])
	username = StringField("Username*", validators=[DataRequired(),
												Length(min=2, max=20)])
	password = PasswordField("Password*", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm password*",
								  validators=[DataRequired(),
					  EqualTo("password")])
	submit = SubmitField("Register")

	def validate_username(self, username):
		"""Checks if the username provided by the user in the form doesn't
		   already exist in the database.
		"""
		user = User.query.filter_by(username=username.data).first()
		if user:
			raise ValidationError("Username provided is already taken. Please provide a different one.")

	def validate_email(self, email):
		"""Checks if the email provided by the user in the form doesn't
		   already exist in the database.
		"""
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError("Email provided is already taken. Please provide a different one.")

	def validate_phone_number(self, phone_number):
		"""Checks if the phone number provided by the user in the form doesn't
		   already exist in the database.
		"""
		user = User.query.filter_by(phone_number=phone_number.data).first()
		if user:
			raise ValidationError("Phone number provided is already taken. Please provide a different one.")


class SigninForm(FlaskForm):
	"""Represents the user login form."""
	username = StringField("Username", validators=[DataRequired()])
	password = PasswordField("Password", validators=[DataRequired()])
	remember_me = BooleanField("Remember me")
	submit = SubmitField("Sign in")


class RequestResetForm(FlaskForm):
	"""Represents the user password reset request form."""
	email = StringField("Email",
                        validators=[DataRequired(), Email()])
	submit = SubmitField("Request Password Reset")

	def validate_email(self, email):
		"""Checks if the email provided by the user in the form
		   exists in the database.
		"""
		user = User.query.filter_by(email=email.data).first()
		if user is None:
			raise ValidationError("There is no account with that email. You must register first.")


class ResetPasswordForm(FlaskForm):
	"""Represents the user password reset form."""
	password = PasswordField("Password", validators=[DataRequired()])
	confirm_password = PasswordField("Confirm Password",
                                     validators=[DataRequired(), EqualTo("password")])
	submit = SubmitField("Reset Password")
