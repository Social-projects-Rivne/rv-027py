import os

from flask_bootstrap import Bootstrap
from app_builder import app, db

from views import views

Bootstrap(app)

if __name__ == '__main__':
    app.run()
