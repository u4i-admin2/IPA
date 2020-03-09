# coding: utf-8

u"""
Alternate runserver command — run using `python manage.py
runserver_quiet`

Required as a workaround since django.server logging can’t be overridden
in Django < 1.10

Via https://stackoverflow.com/a/39488571/7949868
"""

from django.core.servers.basehttp import WSGIRequestHandler

# Grab the original log_message method.
_log_message = WSGIRequestHandler.log_message


def log_message(self, *args):
    # Don't log if path starts with /static/
    if self.path.startswith(
        (
            '/static/',
            '/media/',
        )
    ):
        return
    else:
        return _log_message(self, *args)


# Replace log_message with our custom one.
WSGIRequestHandler.log_message = log_message

# Import the original runserver management command
from django.core.management.commands.runserver import (  # noqa: E402 F401
    Command
)
