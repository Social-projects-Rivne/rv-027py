# rv-027py

### Installation

 For installing required libs and frameworks execute next commands:
```
pip install -r requirements.txt
```
### Configuration

Copy config.py.example and rename this file to config.py
```
Set db credentials
```

### Migrations

1) Initialize migration 
```
manage.py db init
```
2) Create migrations files  
```
manage.py db migrate
```
3) Create tables from migrations  
```
manage.py db upgrade
```
