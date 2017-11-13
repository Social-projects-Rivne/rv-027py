"""This module create instance of Flask and activate packages."""
# pylint: disable=wrong-import-position
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
Bootstrap(app)
CSRFProtect(app)


from create_database import db_create
from drop_database import db_drop
from insert_db_data import db_insert_data
# pylint: disable=unused-import
from views import views


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
