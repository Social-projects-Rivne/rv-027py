import os

from sqlalchemy_utils.functions.database import drop_database

from config import Config

db_credentials = Config.db_credentials

if 'DATABASE_URL' in os.environ:
    db_credentials = os.environ['DATABASE_URL']

# Dropping our test base.
drop_database(db_credentials)

print 'DB dropped'
