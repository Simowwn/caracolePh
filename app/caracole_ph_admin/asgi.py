"""
ASGI config for caracoleph_admin project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

environment = os.environ.get("ENVIRONMENT", "DEV")

if environment == "PROD":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "caracole_ph_admin.settings.prod")
else:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "caracole_ph_admin.settings.dev")

application = get_asgi_application()
