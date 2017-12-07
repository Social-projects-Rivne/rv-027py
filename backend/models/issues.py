"""This module creates Issues model."""
# pylint: disable=too-few-public-methods

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.functions import func

from backend.app import db


class Attachment(db.Model):
    """Attachment table in the database."""

    __tablename__ = 'attachments'

    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.ForeignKey(u'issues.id'), index=True)
    image_url = db.Column(db.Text)

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

    issue = db.relationship(u'Issue')
    status = db.relationship(u'Status')
    user = db.relationship(u'User')


class Issue(db.Model):
    """Issues table in the database."""

    __tablename__ = 'issues'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
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

    def delete(self):
        """Setting deleting date for issue"""
        if not self.delete_date:
            self.delete_date = func.current_timestamp()
            return True
        return False

    def restore(self):
        """Restoring issue from deletion"""
        if self.delete_date:
            self.delete_date = None
            return True
        return False


class Status(db.Model):
    """Status table in the database."""

    __tablename__ = 'statuses'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Text)


class Comments(db.Model):
    """
    Issues table in the database.
    """

    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    date_public = db.Column(db.TIMESTAMP)
    user_id = db.Column(db.ForeignKey(u'users.id'))
    issue_id = db.Column(db.ForeignKey(u'issues.id'), index=True)

    issue = db.relationship(u'Issue')
    user = db.relationship(u'User')

    class Meta:
        """..."""
        app_label = 'city_issues'
        managed = False
        db_table = 'comments'
