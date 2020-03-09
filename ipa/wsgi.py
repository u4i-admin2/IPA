"""
WSGI config for ipa project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application

assert 'BUILD_ENV' in os.environ, 'BUILD_ENV not set in environment'
build_env = os.environ['BUILD_ENV']

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ipa.settings.' + build_env)

application = get_wsgi_application()
