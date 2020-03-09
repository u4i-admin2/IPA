# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class NewsConfig(AppConfig):
    name = 'news'
    verbose_name = 'News'

    def ready(self):
        import api.viewsets
        api.viewsets.register(self.name)
