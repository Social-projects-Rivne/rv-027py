from django.core.management.commands.runserver import BaseRunserverCommand
from django.core.servers.basehttp import get_internal_wsgi_application

from werkzeug.wsgi import DispatcherMiddleware

from app import admin_app


main_app = get_internal_wsgi_application()


class Command(BaseRunserverCommand):
    def get_handler(self, *args, **options):
        application = DispatcherMiddleware(main_app, {'/admin': admin_app})
        return application

