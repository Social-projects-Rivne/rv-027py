import click
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

admin_app = Flask(__name__)
admin_app.config.from_object('config.DevelopmentConfig')
bcrypt = Bcrypt(admin_app)
db = SQLAlchemy(admin_app)
Bootstrap(admin_app)
CSRFProtect(admin_app)


from create_database import db_create
from drop_database import db_drop
from insert_db_data import db_insert_data
from views import views


@admin_app.cli.command()
def initdb():
    db_create()


@admin_app.cli.command()
def dropdb():
    db_drop()


@admin_app.cli.command()
def insertdata():
    db_insert_data()
