"""This module creates Users model."""
# pylint: disable=too-few-public-methods

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.sql.functions import func
from backend.app import bcrypt, db


class Role(db.Model):
    """Role table in the database"""

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Text, nullable=False)


class User(db.Model):
    """User table in the database"""

    ROLE_ADMIN = 1
    ROLE_MODERATOR = 2
    ROLE_USER = 3

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    alias = db.Column(db.Text)
    email = db.Column(db.Text)
    hashed_password = db.Column(db.Text)
    role_id = db.Column(db.ForeignKey(u'roles.id'), index=True)
    avatar = db.Column(db.Text)
    delete_date = db.Column(db.TIMESTAMP)
    role = db.relationship(u'Role')

    @hybrid_property
    def password(self):
        """Getting the password."""
        return self.hashed_password

    @password.setter
    def _set_password(self, plaintext):
        """Hashing password before being stored."""
        self.hashed_password = bcrypt.generate_password_hash(plaintext)

    def check_password(self, plaintext):
        """Checking the password form database."""
        return bcrypt.check_password_hash(self.hashed_password, plaintext)

    # pylint: disable=no-self-use
    # This needs to be checked because no self is used in function
    def is_last_admin(self):
        """Checking for only one admin in users"""
        count = User.query.filter_by(
            role_id=User.ROLE_ADMIN, delete_date=None).count()
        if count > 1:
            return False
        return True

    def delete(self):
        """Setting deleting date for user"""
        if self.role_id == User.ROLE_ADMIN:
            if not self.is_last_admin():
                self.delete_date = func.current_timestamp()
                return True
        else:
            self.delete_date = func.current_timestamp()
            return True
        return False

    def restore(self):
        """Restoring user from deletion"""
        if self.delete_date:
            self.delete_date = None
            return True
        return False
