"""This module create all tables."""
# pylint: disable=no-name-in-module,import-error
from backend.app import db


def db_create_tables():
    """Creating all tables."""
        db.create_all()
        print "Successfully created tables."
