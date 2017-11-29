"""This module insert database data"""
# pylint: disable=no-name-in-module,import-error
import os

from backend.app import db
from backend.config import Config
from backend.models.users import Role, User
from backend.models.issues import (Attachment, Category,
                                   Issue, IssueHistory, Status)

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
status2 = Status(status="on moderation")
status3 = Status(status="open")
status4 = Status(status="closed")

user1 = User(name='Bob', alias='Bobby', email='bob@gmail.com',
             password='crypto', role_id='1')
user2 = User(name='Mark', alias='Marky', email='mark@gmail.com',
             password='123', role_id='2')
user3 = User(name='Maria', alias='Mary', email='maria@gmail.com',
             password='321', role_id='3')

issue1 = Issue(title='Road accident', user_id='2', category_id='1', location_lat='50.621945',
               location_lon='26.249314', description='Car crash ...', status='on moderation')
issue2 = Issue(title='Road accident', user_id='3', category_id='2', location_lat='50.623673',
               location_lon='26.250182', description='Bus crash ...', status='new')
issue3 = Issue(title='Dog lost', user_id='3', category_id='3', location_lat='50.622584',
               location_lon='26.252468', description='Some test data 3', status='new')
issue4 = Issue(title='Road accident', user_id='1', category_id='1', location_lat='50.622836',
               location_lon='26.246706', description='Some test data 4', status='new')
issue5 = Issue(title='Test case 5', user_id='2', category_id='2', location_lat='50.619977',
               location_lon='26.247521', description='Some test data 5', status='open')
issue6 = Issue(title='Test case 6', user_id='3', category_id='3', location_lat='50.619453',
               location_lon='26.251834', description='Some test data 6', status='open')
issue7 = Issue(title='Test case 7', user_id='1', category_id='1', location_lat='50.618500',
               location_lon='26.249838', description='Some test data 7', status='on moderation')
issue8 = Issue(title='Test case 8', user_id='2', category_id='2', location_lat='50.619242',
               location_lon='26.246233', description='Some test data 8', status='closed')


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
issueHistory6 = IssueHistory(user_id='2', issue_id='2', status_id='1',
                             transaction_date='2017/11/11')
issueHistory7 = IssueHistory(user_id='3', issue_id='3', status_id='4',
                             transaction_date='2017/11/17')


def db_insert_data():
    """This function insert database data"""
    db.session.add_all([role, role1, role2,
                        category, category1, category2,
                        status1, status2, status3, status4,
                        user1, user2, user3,
                        issue1, issue2, issue3,
                        issue4, issue5, issue6,
                        issue7, issue8,
                        issueHistory1, issueHistory2, issueHistory3,
                        issueHistory4, issueHistory5, issueHistory6,
                        issueHistory7,
                        attachment1, attachment2, attachment3])
    db.session.commit()

    print "Test data has been inserted into the database"


if __name__ == '__main__':
    db_insert_data()
