import logging
import re

from django.apps import AppConfig
from django.conf import settings
from django.template import base


class PublicConfig(AppConfig):
    name = 'public'
    verbose_name = 'Public frontend'

    def ready(self):
        u"""
        Runs once when app is initialized.
        https://stackoverflow.com/a/16111968/7949868
        """

        # Workaround for https://code.djangoproject.com/ticket/4444
        if getattr(settings, 'DEBUG', None) is True:
            django_server_logger = logging.getLogger('django.server')

            django_server_logger.addFilter(NoBrokenPipeFilter())

        # Hack to allow multi-line template tags
        # http://zachsnow.com/#!/blog/2016/multiline-template-tags-django/
        base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)


class NoBrokenPipeFilter(logging.Filter):
    def filter(self, record):
        if getattr(record, 'msg', '').startswith(u'- Broken pipe'):
            return False

        return True
