import os

from sqlalchemy_utils.functions.database import drop_database

from config import Config


db_credentials = Config.SQLALCHEMY_DATABASE_URI

if 'DATABASE_URL' in os.environ:
    db_credentials = os.environ['DATABASE_URL']


def db_drop():
    drop_database(db_credentials)
    print 'DB dropped'

if __name__ == '__main__':
    db_drop()
