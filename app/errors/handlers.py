"""Module for error handling in the flask app."""
from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(404)
def error_404(error):
    """Defines 404 error handling."""
    return render_template("errors/404.html"), 404


@errors.app_errorhandler(403)
def error_403(error):
    """Defines 403 error handling."""
    return render_template("errors/403.html"), 403


@errors.app_errorhandler(500)
def error_500(error):
    """Defines 500 error handling."""
    return render_template("errors/500.html"), 500
