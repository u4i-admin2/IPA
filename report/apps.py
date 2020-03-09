# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class ReportConfig(AppConfig):
    name = 'report'
    verbose_name = 'Report'

    def ready(self):
        import api.search
        import api.viewsets
        import report.serializers
        api.viewsets.register(self.name)
        api.search.register(self.get_model('Report'),
                            report.serializers.ReportSerializer)
