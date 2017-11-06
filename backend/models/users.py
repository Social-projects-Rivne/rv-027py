<<<<<<< HEAD
from sqlalchemy.ext.hybrid import hybrid_property
from app import bcrypt, db


class Role(db.Model):
    """Role table in the database"""
=======
from app import db


class Role(db.Model):

    """This class is used for role table in database."""
>>>>>>> origin/develop

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Text, nullable=False)


class User(db.Model):
<<<<<<< HEAD
    """User table in the database"""
=======

    """This class is used for user table in database."""
>>>>>>> origin/develop

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    alias = db.Column(db.Text)
    email = db.Column(db.Text)
<<<<<<< HEAD
    _password = db.Column(db.Text, nullable=False)
    role_id = db.Column(db.ForeignKey(u'roles.id'), index=True)
    avatar = db.Column(db.Text)
    delete_date = db.Column(db.TIMESTAMP)
    role = db.relationship(u'Role')

    # getting the password
    @hybrid_property
    def password(self):
        return self._password

    # hashing password before being stored
    @password.setter
    def _set_password(self, plaintext):
        self._password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self._password, plaintext)
=======
    password = db.Column(db.Text)
    role_id = db.Column(db.ForeignKey(u'roles.id'), index=True)
    avatar = db.Column(db.Text)
    delete_date = db.Column(db.TIMESTAMP)

    role = db.relationship(u'Role')
>>>>>>> origin/develop
