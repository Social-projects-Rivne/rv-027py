from sqlalchemy.ext.hybrid import hybrid_property
from manage import bcrypt, db


class Role(db.Model):
    """This class is used for role table in database."""

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.Text, nullable=False)


class User(db.Model):
    """This class is used for user table in database."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, unique=True)
    alias = db.Column(db.Text)
    email = db.Column(db.Text)
    password = db.Column(db.Text)
    role_id = db.Column(db.ForeignKey(u'roles.id'), index=True)
    avatar = db.Column(db.Text)
    delete_date = db.Column(db.Date)
    role = db.relationship(u'Role')

    # getting the password
    @hybrid_property
    def hash_password(self):
        return self.password

    # hashing password before being stored
    @hash_password.setter
    def set_hash_password(self, plaintext):
        self.password = bcrypt.generate_password_hash(plaintext)

    def is_correct_password(self, plaintext):
        return bcrypt.check_password_hash(self.password, plaintext)
