import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module (replace 'myproject' with your actual project name)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitworks.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()