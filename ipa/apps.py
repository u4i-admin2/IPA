import logging

from django.apps import AppConfig

from ipa.cloudfront import register_request_cloudfront_invalidation_signal_handlers


logger = logging.getLogger(__name__)


class IpaConfig(AppConfig):
    name = 'ipa'
    verbose_name = 'IPA/AeA'

    has_run = False

    def ready(self):
        u"""
        Runs once when app is initialized.
        https://stackoverflow.com/a/16111968/7949868
        """

        register_request_cloudfront_invalidation_signal_handlers()
