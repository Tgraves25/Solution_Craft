# solution_craft/wsgi.py
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solution_craft.settings')

application = get_wsgi_application()
