"""This module creates Issues model."""
# pylint: disable=too-few-public-methods
from backend.app import db


class Attachment(db.Model):
    """Attachment table in the database."""

    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.ForeignKey(u'issues.id'), index=True)
    image_url = db.Column(db.Text)
    delete_date = db.Column(db.TIMESTAMP)

    issue = db.relationship(u'Issue')


class Category(db.Model):
    """Category table in the database."""

    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.Text)
    favicon = db.Column(db.Text)


class IssueHistory(db.Model):
    """IssueHistory table in the database."""

    __tablename__ = 'issue_History'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey(u'users.id'))
    issue_id = db.Column(db.ForeignKey(u'issues.id'), index=True)
    status_id = db.Column(db.ForeignKey(u'statuses.id'), index=True)
    transaction_date = db.Column(db.TIMESTAMP)
    delete_date = db.Column(db.TIMESTAMP)

    issue = db.relationship(u'Issue')
    status = db.relationship(u'Status')
    user = db.relationship(u'User')


class Issue(db.Model):
    """Issues table in the database."""

    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    user_id = db.Column(db.ForeignKey(u'users.id'), index=True)
    category_id = db.Column(db.ForeignKey(
        u'category.id'), nullable=False, index=True)
    location_lat = db.Column(db.Float)
    location_lon = db.Column(db.Float)
    status = db.Column(db.Text)
    description = db.Column(db.Text)
    open_date = db.Column(db.TIMESTAMP)
    close_date = db.Column(db.TIMESTAMP)
    delete_date = db.Column(db.TIMESTAMP)

    category = db.relationship(u'Category')
    user = db.relationship(u'User')


class Status(db.Model):
    """Status table in the database."""

    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text)
