from datetime import datetime

from app import db


class Role(db.Model):
    """This class is used for role table in database."""

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Text, nullable=False)


class User(db.Model):
    """This class is used for user table in database."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    alias = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    role_id = db.Column(db.ForeignKey(u'roles.id'), index=True)
    avatar = db.Column(db.Text)
    delete_date = db.Column(db.TIMESTAMP)

    role = db.relationship(u'Role')

    def set_delete_date(self):
        self.delete_date = datetime.now()
