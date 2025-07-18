"""
WSGI config for bitworks project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

# import os

# from django.core.wsgi import get_wsgi_application

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bitworks.settings')

# application = get_wsgi_application()


import os
        import sys

        # Add your project directory to the Python path
        sys.path.insert(0, os.path.dirname(__file__))

        # Set the DJANGO_SETTINGS_MODULE environment variable
        os.environ['DJANGO_SETTINGS_MODULE'] = 'your_project_name.settings' # Replace 'your_project_name'

        # Initialize Django
        import django
        django.setup()

        # Import the WSGI application
        from django.core.wsgi import get_wsgi_application
        application = get_wsgi_application()
