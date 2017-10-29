rename config.py.example to config.py and fill db_credentials with your's data

or

rename config.py.example to config.py and:
* for Unix:  
	* export APP_SETTINGS="config.DevelopmentConfig"  
	* export DATABASE_URL='postgresql://DBUSERNAME:DBPASSWORD@localhost/DBNAME'  

* for Windows:  
	* set APP_SETTINGS=config.DevelopmentConfig  
	* set DATABASE_URL=postgresql://DBUSERNAME:DBPASSWORD@localhost/DBNAME  



pip install -r requipments.txt  
python create_database.py  
python run.py  

