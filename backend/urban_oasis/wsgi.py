"""
WSGI config for urban_oasis project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'urban_oasis.settings')

application = get_wsgi_application()
