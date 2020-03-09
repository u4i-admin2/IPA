# coding: utf-8

import logging
import re

from django.conf import (
    settings,
)
from django_hosts import (
    host,
    patterns,
)

logger = logging.getLogger(__name__)

host_patterns = patterns(
    '',
    host(
        (
            re.escape(settings.AEA_HOSTNAME) + r'(\:\d+)?'
        ),
        'ipa.urls_aea',
        name='aea'
    ),
    host(
        (
            re.escape(settings.IPA_HOSTNAME) + r'(\:\d+)?'
        ),
        'ipa.urls_ipa',
        name='ipa'
    ),
)
