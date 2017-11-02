# rv-027py

### Installing required libs and frameworks
```
pip install -r requirements.txt
```
### Configuration
```
Rename file config.py.example into config.py and 
fill config.py with your's database credentials.
```
### Prepare Command Line Interface
```
set FLASK_APP=app.py
set FLASK_DEBUG=1
```
### Create database and test records.  
```
flask initdb
flask insertdata 
```

### Run application
```
flask run 
```

To drop database (must do: Prepare Command Line Interface step)
```
flask dropdb 
```
