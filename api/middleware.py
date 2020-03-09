# coding: utf-8

u"""API-specific middleware (registered globally by necessity)."""

import logging

from django.utils.cache import add_never_cache_headers

logger = logging.getLogger(__name__)


class ResponseManipulationMiddleware(object):
    u"""
    Middleware that runs before Django calls view.
    """

    def process_response(self, request, response):
        u"""
        Args:
            https://docs.djangoproject.com/en/1.10/topics/http/middleware/

        Returns:
            HttpResponse
        """

        if (
            hasattr(request, 'resolver_match') and
            hasattr(request.resolver_match, 'namespaces') and
            isinstance(request.resolver_match.namespaces, list) and
            'api' in request.resolver_match.namespaces
        ):
            add_never_cache_headers(response)

        return response
