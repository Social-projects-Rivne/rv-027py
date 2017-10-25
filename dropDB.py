from sqlalchemy_utils.functions.database import drop_database

#Credentals for PostgresSQL Server. 
dbCredentals = 'postgresql+psycopg2://login:pass@localhost/test'

#Dropping our test base.
drop_database(dbCredentals)

print 'DB dropped'
