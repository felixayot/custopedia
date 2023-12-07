"""Defines a class to retrieve some of the environment variables
   implemented in the flask app.
"""
import os
from dotenv import load_dotenv


basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    """Represents a few environment variables required for the flask app."""
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'custopedia.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
