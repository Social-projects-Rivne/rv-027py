# import re
from app_builder import db


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
    delete_date = db.Column(db.Date)

    role = db.relationship(u'Role')

    # def data_validataion(self):
    #     """Validate the user's data"""
    #     self.name_check = re.match(r'^[\w]{4,32}$', self.name)
    #     self.alias_check = re.match(r'^[\w]{3,32}$', self.alias)
    #     self.email_check = re.match(r'^[^@]+@[^@]+.[^@]+$', self.email)
    #     self.role_id_check = re.match(r'^[1-3]$', self.role_id)
    #     if (self.name_check and self.alias_check and
    #             self.email_check and self.role_id_check):
    #         return True
    #     return False
