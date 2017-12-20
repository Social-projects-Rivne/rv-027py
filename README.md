### Installing required libs and frameworks
```
pip install -r requirements.txt or requirements/dev.txt
```
### Configuration
```
Rename file config.py.example into config.py and 
fill config.py with your database credentials.
```
### Prepare Command Line Interface (use set on Windows)
```
export FLASK_APP=backend/app.py
export FLASK_DEBUG=1
```
### Create database and test records (from the root)
```
flask initdb
flask insertdata
```
### Provide migrations
```
python client/manage.py migrate
```
### Run Flask application (from the root)
```
flask run
```

### To drop database (from the root)
```
flask dropdb
```

### Django Settings
```
Rename file local_settings.py.example into local_settings.py and
fill it up with your database credentials.
```

### Run Django application (from the root)
```
python client/manage.py runserver
```
### Mail settings

on your google account enable settings (https://goo.gl/Lm1dm8)

