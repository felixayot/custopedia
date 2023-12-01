from flask import render_template, url_for, flash, redirect, request, Blueprint
from app import db, mail
from app.users.forms import RegisterForm, SigninForm, RequestResetForm, ResetPasswordForm 
from app.models.users import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from flask_mail import Message
from werkzeug.routing.exceptions import BuildError

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"], strict_slashes=False)
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(first_name=form.first_name.data,
                    last_name=form.last_name.data, email=form.email.data,
                    phone_number=form.phone_number.data,
                    username=form.username.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created successfully! \
              Please sign in to proceed.", "success")
        return redirect(url_for("users.sign_in"))
    return render_template("register.html", title="Register", form=form)

@users.route("/sign_in", methods=["GET", "POST"], strict_slashes=False)
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not check_password_hash(user.password,
                                                        form.password.data):
            flash("Invalid username or password!", "danger")
            return redirect(url_for("users.sign_in"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.home")
        return redirect(next_page)
    return render_template("sign_in.html", title="Sign in", form=form)

@users.route("/sign_out", strict_slashes=False)
def sign_out():
    logout_user()
    return redirect(url_for("main.home"))


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message("Password Reset Request",
                  sender="noreply@custopedia.com",
                  recipients=[user.email])
    msg.body = f"""To reset your password, visit the following link:
{url_for("users.reset_token", token=token, _external=True)}

If you did not make this request, simply ignore this email and no changes will be made.
"""
    mail.send(msg)


@users.route("/reset_password", methods=["GET", "POST"])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        try:
            send_reset_email(user)
        except (BuildError, ConnectionRefusedError):
            pass
        flash("An email has been sent with instructions to reset your password.", "info")
        return redirect(url_for("users.login"))
    return render_template("reset_request.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)
    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password = hashed_password
        db.session.commit()
        flash("Your password has been changed successfully! You are now able to log in", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
