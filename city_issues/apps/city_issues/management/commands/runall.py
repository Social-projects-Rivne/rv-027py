from django.core.management.commands.runserver import BaseRunserverCommand
from django.core.servers.basehttp import get_internal_wsgi_application

from werkzeug.wsgi import DispatcherMiddleware

from app import admin_app

city_issues = get_internal_wsgi_application()


# Basically the idea was to connect the 2 apps and run them
# with Django web server
class Command(BaseRunserverCommand):
    def get_handler(self, *args, **options):
        application = DispatcherMiddleware(city_issues, {'/admin': admin_app})
        return application
