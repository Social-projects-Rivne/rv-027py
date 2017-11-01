import os
from flask import Flask, render_template
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap


config_object = 'config.DevelopmentConfig'

if 'APP_SETTINGS' in os.environ:
	config_object = os.environ['APP_SETTINGS']

app = Flask(__name__)
app.config.from_object(config_object)
db = SQLAlchemy(app)
Bootstrap(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)






