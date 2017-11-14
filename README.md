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
```
### Create database and test records (from the root)
```
python backend/create_database.py
python backend/insert_db_data.py
```

### Run Flask application (from the root)
```
python backend/run.py run
```

To drop database (from the root)
```
python backend/drop_database.py
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

### Create database and test records (from the root)
```
python backend/create_database.py
python backend/insert_db_data.py
```

### Django Settings
```
Rename file local_settings.py.example into local_settings.py and
fill it up with your database credentials.
```

### Run Django application (from the root)
```
python client/manage.py runall
```

### To enter admin panel
```
add '/admin' to the url
```
