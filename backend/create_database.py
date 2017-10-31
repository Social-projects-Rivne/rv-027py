import os
from sqlalchemy_utils.functions.database import create_database, database_exists
from models.users import Role, User
from models.issues import Attachment, Category, Issue, IssueHistory, Status
from manage import db
from config import Config

#Checking if database exists, and if not -> create it with all tables.

db_credentials = Config.db_credentials

if 'DATABASE_URL' in os.environ:
    db_credentials = os.environ['DATABASE_URL']


if not database_exists(db_credentials):
    create_database(db_credentials)
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

user1 = User(name='Bob', alias='Bobby', email='bob@gmail.com', password='crypto', role_id='1', avatar=None, delete_date=None)
user2 = User(name='Mark', alias='Marky', email='mark@gmail.com', password='123', role_id='2', avatar=None, delete_date=None)
user3 = User(name='Maria', alias='Mary', email='maria@gmail.com', password='321', role_id='3', avatar=None, delete_date=None)

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