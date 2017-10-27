pip install -r requipments.txt  

for Unix:  
export APP_SETTINGS="config.DevelopmentConfig"  
export DATABASE_URL='postgresql://DBUSERNAME:DBPASSWORD@localhost/DBNAME'  

for Windows:  
set APP_SETTINGS=config.DevelopmentConfig  
set DATABASE_URL=postgresql://DBUSERNAME:DBPASSWORD@localhost/DBNAME  

python create_database.py  
python manage.py  

