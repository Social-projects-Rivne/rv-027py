import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

config_object = 'config.DevelopmentConfig'

if 'APP_SETTINGS' in os.environ:
	config_object = os.environ['APP_SETTINGS']

app = Flask(__name__)
app.config.from_object(config_object)
db = SQLAlchemy(app)





