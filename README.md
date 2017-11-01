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

### Migrations and DB

1) Initialize migration (choose directory with migrations.py) & enter following command
```
migrations.py db init
```
2) Create migrations files  
```
migrations.py db migrate
```
3) Create tables from migrations  
```
migrations.py db upgrade
```
Create test records  
```
python create_database.py  
```

### Run application

For the start application execute  
```
python run.py  
```
