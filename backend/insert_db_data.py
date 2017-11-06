import os

from app import db
from config import Config
from models.users import Role, User
from models.issues import Attachment, Category, Issue, IssueHistory, Status

db_credentials = Config.SQLALCHEMY_DATABASE_URI

if 'DATABASE_URL' in os.environ:
    db_credentials = os.environ['DATABASE_URL']

role = Role(role='admin')
role1 = Role(role='moderator')
role2 = Role(role='user')

category = Category(category='road accident', favicon='')
category1 = Category(category='infrastructure accident', favicon='')
category2 = Category(category='another accident', favicon='')

status1 = Status(status="new")
status2 = Status(status="working")
status3 = Status(status="closed")

user1 = User(name='Bob', alias='Bobby', email='bob@gmail.com',
             password='crypto', role_id=1)
user2 = User(name='Mark', alias='Marky', email='mark@gmail.com',
             password='123', role_id=2)
user3 = User(name='Maria', alias='Mary', email='maria@gmail.com',
             password='321', role_id=3)

issue1 = Issue(name='Road accident', user_id='2', category_id='1', location='',
               description='Car crash ...')
issue2 = Issue(name='Road accident', user_id='3', category_id='1', location='',
               description='Bus crash ...')
issue3 = Issue(name='Dog lost', user_id='3', category_id='3', location='',
               description='Poor puppy is lost')

attachment1 = Attachment(issue_id='1', image_url='some url1')
attachment2 = Attachment(issue_id='2', image_url='some url2')
attachment3 = Attachment(issue_id='3', image_url='some url3')

issueHistory1 = IssueHistory(user_id='1', issue_id='1', status_id='1',
                             transaction_date='2017/10/25')
issueHistory2 = IssueHistory(user_id='1', issue_id='1', status_id='2',
                             transaction_date='2017/10/27')
issueHistory3 = IssueHistory(user_id='3', issue_id='3', status_id='1',
                             transaction_date='2017/09/20')
issueHistory4 = IssueHistory(user_id='3', issue_id='3', status_id='2',
                             transaction_date='2017/09/25')
issueHistory5 = IssueHistory(user_id='3', issue_id='3', status_id='3',
                             transaction_date='2017/09/26')


def db_insert_data():
    db.session.add_all([role, role1, role2,
                        category, category1, category2,
                        status1, status2, status3,
                        user1, user2, user3,
                        issue1, issue2, issue3,
                        issueHistory1, issueHistory2, issueHistory3,
                        issueHistory4, issueHistory5
                        ])
    db.session.commit()

    print("Test data has been inserted into the database.")

if __name__ == '__main__':
    db_insert_data()
