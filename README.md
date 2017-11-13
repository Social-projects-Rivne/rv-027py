# For the guys:

### Installing required libs and frameworks
```
pip install -r requirements.txt
```
### Configuration
```
Rename file config.py.example into config.py and 
fill config.py with your database credentials.
```
### Prepare Command Line Interface
On Windows use **set** instead of **export**
```
export  FLASK_APP=backend/app.py
export  FLASK_DEBUG=1
```
### Create database and test records  
```
flask initdb
flask insertdata 
```

### Run Flask application
```
flask run 
```

To drop database (must do: Prepare Command Line Interface step)
```
flask dropdb 
```

### Django Settings
```
Rename file local_settings.py.example into local_settings.py and
fill it up with your database credentials.
```

### Run Django application
```
python manage.py runserver
```

#
# For the girls:

### Installing required libs and frameworks
```
pip install -r requirements.txt
```
### Flask Configuration
```
Rename file config.py.example into config.py and
fill config.py with your database credentials.
```

### Create database and test records
```
flask initdb
flask insertdata
```

### Django Settings
```
Rename file local_settings.py.example into local_settings.py and
fill it up with your database credentials.
```

### Run Django application
```
python manage.py runall
```

### To enter admin panel
```
add /admin to the url
```
