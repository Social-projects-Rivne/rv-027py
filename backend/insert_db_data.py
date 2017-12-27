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

category = Category(category='Road accident', favicon='')
category1 = Category(category='Infrastructure accident', favicon='')
category2 = Category(category='Another accident', favicon='')
category3 = Category(category='Accident with animals', favicon='')

status1 = Status(status="new")
status2 = Status(status="on moderation")
status3 = Status(status="open")
status4 = Status(status="closed")
status5 = Status(status="deleted")
status6 = Status(status="pending close")

user1 = User(name='Bob', alias='Bobby', email='bob@gmail.com',
             password='crypto', role_id='1')
user2 = User(name='Mark', alias='Marky', email='mark@gmail.com',
             password='123', role_id='2')
user3 = User(name='Maria', alias='Mary', email='maria@gmail.com',
             password='321', role_id='3')
user4 = User(name='Petya', alias='Petya', email='petya@gmail.com',
             password='321', role_id='3')
user5 = User(name='Tom', alias='Tom', email='tom@gmail.com',
             password='321', role_id='3')
user6 = User(name='Jerry', alias='Jerry', email='jerry@gmail.com',
             password='321', role_id='2')
user7 = User(name='Olivia', alias='Olivia', email='olivia@gmail.com',
             password='321', role_id='3')
user8 = User(name='Jack Sparrow', alias='Jack', email='jack@gmail.com',
             password='321', role_id='1')
user9 = User(name='Leo', alias='Leo', email='leo1991@gmail.com',
             password='321', role_id='3')
user10 = User(name='Amelia', alias='Ameli', email='amelia@gmail.com',
              password='321', role_id='2')
user11 = User(name='Harry', alias='Harry', email='harry@gmail.com',
              password='321', role_id='3')
user12 = User(name='Maximus', alias='Max', email='max@gmail.com',
              password='321', role_id='3')

issue1 = Issue(title='Car crash', user_id='2', category_id='1', location_lat='50.620226734521204',
               location_lon='26.239514350891117', description='Two cars find one way in same moment of time ....', status='on moderation',
               open_date='2017/11/15')
issue2 = Issue(title='Trolleybus is broken', user_id='3', category_id='1', location_lat='50.6190831458868',
               location_lon='26.252110004425052', description='It is very heavy traffic in this place', status='new',
               open_date='2017/11/16')
issue3 = Issue(title='Prohibited parking', user_id='3', category_id='1', location_lat='50.61954603035055',
               location_lon='26.25116586685181', description='As you see prohibited parking detecting', status='new',
               open_date='2017/11/17')
issue4 = Issue(title='Stolen car wheels', user_id='1', category_id='1', location_lat='50.61487613411816',
               location_lon='26.25116586685181', description='My car wheels have been stolen by some bastards ', status='open',
               open_date='2017/11/18')
issue5 = Issue(title='Heavy traffic', user_id='2', category_id='1', location_lat='50.61320139365915',
               location_lon='26.239514350891117', description='All cars are here, because Soborna street is closed', status='closed',
               open_date='2017/11/19', close_date='2017/11/25')
issue6 = Issue(title='No electricity', user_id='3', category_id='2', location_lat='50.6250186130551',
               location_lon='26.253225803375248', description='There is no electricity in that place after storm', status='open',
               open_date='2017/11/20')
issue7 = Issue(title='No water', user_id='1', category_id='2', location_lat='50.62209181346729',
               location_lon='26.283631324768066', description='We dont have water for two days. Rivnevodocanal cant say nothing about it', status='open',
               open_date='2017/11/21')
issue8 = Issue(title='Gas smell', user_id='2', category_id='2', location_lat='50.62229601469869',
               location_lon='26.231789588928226', description='we have strong gas smell here, call 104', status='closed',
               open_date='2016/11/22', close_date='2017/01/15')
issue9 = Issue(title='Fire alarm', user_id='3', category_id='2', location_lat='50.62601232218674',
               location_lon='26.25416994094849', description='Somebody fire that building, you can see some foto ...', status='open',
               open_date='2017/11/23')
issue10 = Issue(title='Broken tree', user_id='1', category_id='3', location_lat='50.615978979420014',
                location_lon='26.26311779022217', description='Old tree finally falls, you cant run and walk there', status='open',
                open_date='2017/11/24')
issue11 = Issue(title='Street musician', user_id='2', category_id='3', location_lat='50.62004975238461',
                location_lon='26.24080181121826', description='Very beautiful music', status='on moderation',
                open_date='2017/11/26')
issue12 = Issue(title='Bad company', user_id='3', category_id='3', location_lat='50.607700200565034',
                location_lon='26.231789588928226', description='I can see very suspicious there every day, beware', status='closed',
                open_date='2014/11/27', close_date='2014/12/01')
issue13 = Issue(title='Beer fest', user_id='1', category_id='3', location_lat='50.617095413757845',
                location_lon='26.255307197570804', description='Beer fest is running here, come on', status='on moderation',
                open_date='2017/11/28')
issue14 = Issue(title='Prankers', user_id='2', category_id='3', location_lat='50.63607074324129',
                location_lon='26.268010139465332', description='Some prankers offer to buy brick, but I have two already', status='open',
                open_date='2017/11/29')
issue15 = Issue(title='Dog lost', user_id='3', category_id='4', location_lat='50.63979957034144',
                location_lon='26.265778541564945', description='My lovely Rex disappeared in the dark, please help me find it.', status='closed',
                open_date='2017/11/30', close_date='2017/12/10')
issue16 = Issue(title='Cat lost', user_id='1', category_id='4', location_lat='50.61943711676894',
                location_lon='26.283631324768066', description='Big dark cat, cats nickname is Rambo, please return it for reward', status='open',
                open_date='2017/12/01')
issue17 = Issue(title='Dog found', user_id='2', category_id='4', location_lat='50.63895584704026',
                location_lon='26.206941604614258', description='Hungry and sick, anybody know it ?', status='open',
                open_date='2017/12/02')
issue18 = Issue(title='Poor puppies', user_id='3', category_id='4', location_lat='50.63127999106349',
                location_lon='26.20951652526856', description='We have four puppies to your lonely heart', status='new',
                open_date='2017/12/03')
issue19 = Issue(title='Ugly hounds', user_id='1', category_id='4', location_lat='50.634083729153225',
                location_lon='26.263289451599125', description='Beware, its dangerous to go there', status='deleted',
                open_date='2017/12/04')


attachment1 = Attachment(issue_id='1', image_url='uploads/Car crash/car-crash.jpg')
attachment2 = Attachment(issue_id='2', image_url='uploads/Trolleybus is broken/trolleybus-broken.jpg')
attachment3 = Attachment(issue_id='3', image_url='uploads/Prohibited parking/prohibited-parking.jpg')
attachment4 = Attachment(issue_id='4', image_url='uploads/Stolen car wheels/stolen-wheels.jpg')
attachment5 = Attachment(issue_id='5', image_url='uploads/Heavy traffic/heavy-traffic.jpg')
attachment6 = Attachment(issue_id='6', image_url='uploads/No electricity/no-electricity.jpg')
attachment7 = Attachment(issue_id='7', image_url='uploads/No water/no-water.jpg')
attachment8 = Attachment(issue_id='8', image_url='uploads/Gas smell/gas-smell.jpg')
attachment9 = Attachment(issue_id='9', image_url='uploads/Fire alarm/fire-alarm.jpg')
attachment10 = Attachment(issue_id='10', image_url='uploads/Broken tree/broken-tree.jpg')
attachment11 = Attachment(issue_id='11', image_url='uploads/Street musician/street-musician.jpg')
attachment12 = Attachment(issue_id='12', image_url='uploads/Bad company/bad-company.jpg')
attachment13 = Attachment(issue_id='13', image_url='uploads/Beer fest/beer-fest.jpg')
attachment14 = Attachment(issue_id='14', image_url='uploads/Prankers/prankers.jpg')
attachment15 = Attachment(issue_id='15', image_url='uploads/Dog lost/dog-lost.jpg')
attachment16 = Attachment(issue_id='16', image_url='uploads/Cat lost/lost-cat.jpg')
attachment17 = Attachment(issue_id='17', image_url='uploads/Dog found/dog-found.jpg')
attachment18 = Attachment(issue_id='18', image_url='uploads/Poor puppies/poor-puppies.jpg')
attachment19 = Attachment(issue_id='19', image_url='uploads/Ugly hounds/ugly-hounds.jpg')


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


comment1 = Comments(user_id='1', issue_id='1',
                    date_public='2017/09/26', comment='It is good that no one was hurt', status='public')
comment2 = Comments(user_id='2', issue_id='1',
                    date_public='2017/10/10', comment='Smashed car headlights', status='public')
comment3 = Comments(user_id='3', issue_id='1',
                    date_public='2017/11/06', comment='Good', status='private')
comment4 = Comments(user_id='2', issue_id='3', date_public='2017/10/16',
                    comment='Photo is low quality, please upload other', status='internal')
comment5 = Comments(user_id='3', issue_id='3', date_public='2017/10/16',
                    comment='Ok, I take a picture and upload it', status='internal')


def db_insert_data():
    """This function insert database data"""
    db.session.add_all([role, role1, role2,
                        category, category1, category2, category3,
                        status1, status2, status3, status4, status5, status6,
                        user1, user2, user3, user4, user5, user6, user7, user8,
                        user9, user10, user11, user12,
                        issue1, issue2, issue3,
                        issue4, issue5, issue6,
                        issue7, issue8, issue9,
                        issue10, issue11, issue12,
                        issue13, issue14, issue15,
                        issue16, issue17, issue18,
                        issue19,
                        issueHistory1, issueHistory2, issueHistory3,
                        issueHistory4, issueHistory5, issueHistory6,
                        issueHistory7,
                        attachment1, attachment2, attachment3, attachment4,
                        attachment5, attachment6, attachment7, attachment8,
                        attachment9, attachment10, attachment11, attachment12,
                        attachment13, attachment14, attachment15, attachment16,
                        attachment17, attachment18, attachment19,
                        comment1, comment2, comment3, comment4, comment5])
    db.session.commit()

    print "Test data has been inserted into the database"


if __name__ == '__main__':
    db_insert_data()
