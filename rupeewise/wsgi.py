"""
WSGI config for rupeewise project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'rupeewise.settings')

application = get_wsgi_application()
