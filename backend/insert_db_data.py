"""This module insert database data"""
# pylint: disable=no-name-in-module,import-error
import os

from backend.app import db
from backend.config import Config
from backend.models.users import Role, User
from backend.models.issues import (Attachment, Category, Comments,
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


issue1 = Issue(title='First issue', user_id='2', category_id='1', location_lat='50.621945',
               location_lon='26.249314', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ut vulputate tortor. Quisque a mauris lobortis, tempor nisi ac, volutpat libero. Ut eu magna finibus, tincidunt ligula eget, dictum enim. Vivamus lobortis semper lorem, sit amet tincidunt metus viverra a. Sed ullamcorper ullamcorper porttitor.', status='on moderation',
               open_date='2017/11/15')
issue2 = Issue(title='Road accident', user_id='3', category_id='2', location_lat='50.623673',
               location_lon='26.250182', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ut vulputate tortor. Quisque a mauris lobortis, tempor nisi ac, volutpat libero. Ut eu magna finibus, tincidunt ligula eget, dictum enim. Vivamus lobortis semper lorem, sit amet tincidunt metus viverra a. Sed ullamcorper ullamcorper porttitor.', status='new',
               open_date='2017/11/16')
issue3 = Issue(title='Dog lost', user_id='3', category_id='3', location_lat='50.622584',
               location_lon='26.252468', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ut vulputate tortor. Quisque a mauris lobortis, tempor nisi ac, volutpat libero. Ut eu magna finibus, tincidunt ligula eget, dictum enim. Vivamus lobortis semper lorem, sit amet tincidunt metus viverra a. Sed ullamcorper ullamcorper porttitor.', status='new',
               open_date='2017/11/17')
issue4 = Issue(title='Road accident', user_id='1', category_id='1', location_lat='50.622836',
               location_lon='26.246706', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ut vulputate tortor. Quisque a mauris lobortis, tempor nisi ac, volutpat libero. Ut eu magna finibus, tincidunt ligula eget, dictum enim. Vivamus lobortis semper lorem, sit amet tincidunt metus viverra a. Sed ullamcorper ullamcorper porttitor.', status='new',
               open_date='2017/11/18')
issue5 = Issue(title='Test case 5', user_id='2', category_id='2', location_lat='50.619977',
               location_lon='26.247521', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ut vulputate tortor. Quisque a mauris lobortis, tempor nisi ac, volutpat libero. Ut eu magna finibus, tincidunt ligula eget, dictum enim. Vivamus lobortis semper lorem, sit amet tincidunt metus viverra a. Sed ullamcorper ullamcorper porttitor.', status='open',
               open_date='2017/11/19')
issue6 = Issue(title='Test case 6', user_id='3', category_id='3', location_lat='50.619453',
               location_lon='26.251834', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ut vulputate tortor. Quisque a mauris lobortis, tempor nisi ac, volutpat libero. Ut eu magna finibus, tincidunt ligula eget, dictum enim. Vivamus lobortis semper lorem, sit amet tincidunt metus viverra a. Sed ullamcorper ullamcorper porttitor.', status='open',
               open_date='2017/11/20')
issue7 = Issue(title='Test case 7', user_id='1', category_id='1', location_lat='50.618500',
               location_lon='26.249838', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ut vulputate tortor. Quisque a mauris lobortis, tempor nisi ac, volutpat libero. Ut eu magna finibus, tincidunt ligula eget, dictum enim. Vivamus lobortis semper lorem, sit amet tincidunt metus viverra a. Sed ullamcorper ullamcorper porttitor.', status='on moderation',
               open_date='2017/11/21')
issue8 = Issue(title='Test case 8', user_id='2', category_id='2', location_lat='50.619242',
               location_lon='26.246233', description='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras ut vulputate tortor. Quisque a mauris lobortis, tempor nisi ac, volutpat libero. Ut eu magna finibus, tincidunt ligula eget, dictum enim. Vivamus lobortis semper lorem, sit amet tincidunt metus viverra a. Sed ullamcorper ullamcorper porttitor.', status='closed',
               open_date='2017/11/22')


attachment1 = Attachment(issue_id='1', image_url=None)
attachment2 = Attachment(issue_id='2', image_url=None)
attachment3 = Attachment(issue_id='3', image_url=None)


issueHistory1 = IssueHistory(user_id='1', issue_id='1', status_id='1',
                             transaction_date='2017/09/25')
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


comment1 = Comments(user_id='1', issue_id='1', date_public='2017/09/26', comment='Vestibulum et scelerisque felis. Nunc elementum commodo enim non maximus. Vestibulum sed molestie sem. Maecenas aliquam at eros at mattis. Maecenas vitae suscipit turpis, at iaculis sem. Donec sagittis mauris sapien.                       Duis ultricies odio ac libero tincidunt convallis eget non dui. Quisque condimentum vel justo eget ultrices. In efficitur laoreet velit. ')
comment2 = Comments(user_id='2', issue_id='1', date_public='2017/10/10', comment='Nunc elementum commodo enim non maximus. Vestibulum sed molestie sem. Maecenas aliquam at eros at mattis. Maecenas vitae suscipit turpis, at iaculis sem. Donec sagittis mauris sapien. Duis ultricies odio ac libero                          tincidunt convallis eget non dui. Quisque condimentum vel justo eget ultrices. In efficitur laoreet velit. ')
comment3 = Comments(user_id='3', issue_id='1', date_public='2017/11/06', comment='Maecenas vitae suscipit turpis, at iaculis sem. Donec sagittis mauris sapien. Duis ultricies odio ac libero tincidunt convallis eget non dui. Quisque condimentum vel justo eget ultrices. In efficitur laoreet velit. ')
comment4 = Comments(user_id='2', issue_id='3', date_public='2017/10/16', comment='Vivamus mauris massa, ullamcorper vel faucibus vitae, mollis at dolor. Vivamus fringilla ex ac pretium rhoncus. Integer dictum ligula est, vitae dictum metus condimentum tempus.')
comment5 = Comments(user_id='3', issue_id='3', date_public='2017/10/16', comment='Sed bibendum arcu eu nisi vestibulum, consectetur hendrerit mi pharetra. Vivamus mauris massa, ullamcorper vel faucibus vitae, mollis at dolor. Vivamus fringilla ex ac pretium rhoncus. Integer dictum ligula est, vitae                     dictum metus condimentum tempus.')


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
                        attachment1, attachment2, attachment3,
                        comment1, comment2, comment3, comment4, comment5])
    db.session.commit()

    print "Test data has been inserted into the database"


if __name__ == '__main__':
    db_insert_data()
