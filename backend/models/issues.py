"""This module creates Issues model."""
# pylint: disable=too-few-public-methods

import os

from flask import current_app
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

    def get_thumbnail_url(self):
        head, tail = os.path.split(self.image_url)
        thumb_name = "thumb-{}".format(tail)
        return "{}/{}".format(head, thumb_name)

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        delete_file(self.image_url)
        delete_file(self.get_thumbnail_url())
        directory_path = os.path.abspath(os.path.join(
            current_app.config['MEDIA_FOLDER'], self.image_url, os.pardir))
        if not os.listdir(directory_path) and os.path.exists(directory_path):
            os.rmdir(directory_path)

    def get_full_thumbnail_url(self):
        url = self.get_thumbnail_url()
        if current_app.config.get('MEDIA_URL'):
            return current_app.config['MEDIA_URL'] + url
        return '/media/' + url


def delete_file(url):
    file_path = os.path.abspath(os.path.join(
        current_app.config['MEDIA_FOLDER'], url))
    if os.path.exists(file_path):
        os.remove(file_path)


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
    transaction_date = db.Column(db.TIMESTAMP(timezone=True))

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
    open_date = db.Column(db.TIMESTAMP(timezone=True))
    close_date = db.Column(db.TIMESTAMP(timezone=True))
    delete_date = db.Column(db.TIMESTAMP(timezone=True))

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
    date_public = db.Column(db.TIMESTAMP(timezone=True))
    user_id = db.Column(db.ForeignKey(u'users.id'))
    issue_id = db.Column(db.ForeignKey(u'issues.id'), index=True)
    status = db.Column(db.Text)
    pre_deletion_status = db.Column(db.Text)

    issue = db.relationship(u'Issue')
    user = db.relationship(u'User')

    class Meta:
        """..."""
        app_label = 'city_issues'
        managed = False
        db_table = 'comments'


def get_all_issue_history(issue_id):
    """Method return all issue history and comments sorted by date."""
    all_history = db.session.query(
        IssueHistory).filter(IssueHistory.issue_id == issue_id).order_by(
            IssueHistory.transaction_date).all()
    comments = db.session.query(Comments).filter(
        Comments.issue_id == issue_id).order_by(Comments.date_public).all()
    list_history = []
    for history in all_history:
        list_history.append(['change_status', history.status.status, history.user.alias,
                             history.transaction_date.strftime('%Y-%m-%d %H:%M')])
    for comment in comments:
        list_history.append(['add_comment', comment.user.alias,
                             comment.comment, comment.date_public.strftime('%Y-%m-%d %H:%M')])
    list_history.sort(key=lambda history: history[3])
    return list_history
