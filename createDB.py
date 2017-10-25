from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils.functions.database import create_database, database_exists


#Credentals for PostgresSQL Server. You mast have superuser with 'login' nickname and 'pass' password.
dbCredentals = 'postgresql+psycopg2://login:pass@localhost/test'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = dbCredentals
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
    category_id = db.Column(db.ForeignKey(u'Category.id'), nullable=False, index=True)
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


#Checking if database exists, and if not -> create it with all tables.
if not database_exists(dbCredentals):
	create_database(dbCredentals)  
	db.create_all()
	db.session.commit()


#Creating some test data.
role = Role(role='admin')
role1 = Role(role='moderator')
role2 = Role(role='user')

category = Category(category='road accident', favicon='')
category1 = Category(category='infrastructure accident', favicon='')
category2 = Category(category='another accident', favicon='')

status1 = Status(status="new")
status2 = Status(status="working")
status3 = Status(status="closed")

user1 = User(name='Bob', alias='Bobby', email='bob@gmail.com', password='crypto', role_id = '1', avatar=None, delete_date=None)
user2 = User(name='Mark', alias='Marky', email='mark@gmail.com', password='123', role_id = '2', avatar=None, delete_date=None)
user3 = User(name='Maria', alias='Mary', email='maria@gmail.com', password='321', role_id = '3', avatar=None, delete_date=None)

issue1 = Issue(name='Road accident', user_id='2', category_id='1', location='', description='Car crash ...', 
                open_date='2017/10/25', close_date=None, delete_date=None)
issue2 = Issue(name='Road accident', user_id='3', category_id='1', location='', description='Bus crash ...', 
                open_date='2016/01/12', close_date='2016/01/20', delete_date=None)
issue3 = Issue(name='Dog lost', user_id='3', category_id='3', location='', description='Poor puppy is lost', 
                open_date='2017/09/20', close_date='2017/09/25', delete_date='2017/09/26')

attachment1 = Attachment(issue_id='1', image_url='some url1', delete_date=None)
attachment2 = Attachment(issue_id='2', image_url='some url2', delete_date='2016/01/20')
attachment3 = Attachment(issue_id='3', image_url='some url3', delete_date='2017/09/26')

issueHistory1 = IssueHistory(user_id='1', issue_id='1', status_id='1', transaction_date='2017/10/25', delete_date=None)
issueHistory2 = IssueHistory(user_id='1', issue_id='1', status_id='2', transaction_date='2017/10/27', delete_date=None)
issueHistory3 = IssueHistory(user_id='3', issue_id='3', status_id='1', transaction_date='2017/09/20', delete_date=None)
issueHistory4 = IssueHistory(user_id='3', issue_id='3', status_id='2', transaction_date='2017/09/25', delete_date=None)
issueHistory5 = IssueHistory(user_id='3', issue_id='3', status_id='3', transaction_date='2017/09/26', delete_date=None)


#Insert test data into database.
db.session.add_all([role, role1, role2, 
                    category, category1, category2, 
                    status1, status2, status3,
                    user1, user2, user3,
                    issue1, issue2, issue3,
                    issueHistory1, issueHistory2, issueHistory3, issueHistory4, issueHistory5
                    ])
db.session.commit()


print "Ok"