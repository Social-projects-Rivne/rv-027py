"""This module create database, if it not exists"""
# pylint: disable=no-name-in-module,import-error
import os

from sqlalchemy_utils.functions.database import (create_database,
                                                 database_exists)

from backend.app import db
from backend.config import Config


# Checking if database exists, and if not -> create it with all tables.

db_credentials = Config.SQLALCHEMY_DATABASE_URI

if 'DATABASE_URL' in os.environ:
    db_credentials = os.environ['DATABASE_URL']


def db_create():
    """Creating database, if it not exists"""
    if not database_exists(db_credentials):
        create_database(db_credentials)
        db.create_all()
        db.session.commit()
        print "Successfully created database and tables."
    else:
        print "The database already exists!"


if __name__ == '__main__':
    db_create()
