"""This module create instance of Flask and activate packages."""
# pylint: disable=wrong-import-position
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail


app = Flask(__name__)
app.config.from_object('backend.config.DevelopmentConfig')
db = SQLAlchemy(app)
Bootstrap(app)
CSRFProtect(app)
mail = Mail(app)


from backend.create_database import db_create
from backend.drop_database import db_drop
from backend.insert_db_data import db_insert_data
from backend.dowload_attachments import download_and_extract_attachments
# pylint: disable=unused-import
from backend.views import views


@app.cli.command()
def initdb():
    """Creating database"""
    db_create()


@app.cli.command()
def dropdb():
    """Dropping database"""
    db_drop()


@app.cli.command()
def insertdata():
    """Inserting data into database"""
    db_insert_data()


@app.cli.command()
def download_and_extract_images():
    """Download and extract images from Google Drive"""
    download_and_extract_attachments()
