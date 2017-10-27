from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions.database import create_database, database_exists
from config import db_credentals


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_credentals
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Attachment(db.Model):
    """This class is used for Attachment table in database."""

    __tablename__ = 'Attachments'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.ForeignKey(u'Issues.id'), index=True)
    image_url = db.Column(db.Text)
    delete_date = db.Column(db.Date)

    issue = db.relationship(u'Issue')


class Category(db.Model):
    """This class is used for Category table in database."""

    __tablename__ = 'Category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text)
    favicon = db.Column(db.Text)


class IssueHistory(db.Model):
    """This class is used for IssueHistory table in database."""

    __tablename__ = 'Issue_History'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(u'Users.id'))
    issue_id = db.Column(db.ForeignKey(u'Issues.id'), index=True)
    status_id = db.Column(db.ForeignKey(u'Statuses.id'), index=True)
    transaction_date = db.Column(db.Date)
    delete_date = db.Column(db.Date)

    issue = db.relationship(u'Issue')
    status = db.relationship(u'Status')
    user = db.relationship(u'User')


class Issue(db.Model):
    """This class is used for Issues table in database."""

    __tablename__ = 'Issues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey(u'Users.id'), index=True)
    category_id = db.Column(db.ForeignKey(
        u'Category.id'), nullable=False, index=True)
    location = db.Column(db.Text)
    description = db.Column(db.Text)
    open_date = db.Column(db.Date)
    close_date = db.Column(db.Date)
    delete_date = db.Column(db.Date)

    category = db.relationship(u'Category')
    user = db.relationship(u'User')


class Role(db.Model):
    """This class is used for Role table in database."""

    __tablename__ = 'Roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Text, nullable=False)


class Status(db.Model):
    """This class is used for Status table in database."""

    __tablename__ = 'Statuses'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text)


class User(db.Model):
    """This class is used for User table in database."""

    __tablename__ = 'Users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    alias = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    role_id = db.Column(db.ForeignKey(u'Roles.id'), index=True)
    avatar = db.Column(db.Text)
    delete_date = db.Column(db.Date)

    role = db.relationship(u'Role')
