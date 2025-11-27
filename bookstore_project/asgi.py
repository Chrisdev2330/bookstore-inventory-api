"""
ASGI config for bookstore_project.

Expone el callable de ASGI para servidores como Daphne o Uvicorn.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore_project.settings')

application = get_asgi_application()
