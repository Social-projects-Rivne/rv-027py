import click
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)
Bootstrap(app)


from create_database import db_create
from drop_database import db_drop
from insert_db_data import db_insert_data
from views import views


@app.cli.command()
def initdb():
    db_create()


@app.cli.command()
def dropdb():
    db_drop()


@app.cli.command()
def insertdata():
    db_insert_data()
