import os
from sqlalchemy_utils.functions.database import drop_database

# Dropping our test base.
drop_database(os.environ['DATABASE_URL'])

print 'DB dropped'
