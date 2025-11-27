"""
WSGI config for bookstore_project.

Expone el callable de WSGI como una variable de módulo llamada ``application``.
"""

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')

application = get_wsgi_application()
