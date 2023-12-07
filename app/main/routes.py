"""Instantiates the Blueprint and defines the view for main page."""
from flask import render_template, Blueprint

main = Blueprint("main", __name__)

@main.route("/", strict_slashes=False)
@main.route("/home", strict_slashes=False)
def home():
    """Returns home page for the app."""
    return render_template("home.html", title="Home Page")
