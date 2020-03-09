# coding: utf-8

u"""Public-specific middleware (registered globally by necessity)."""

import logging
from django.conf import settings
from django.utils.cache import patch_cache_control
from public.utils import get_styles

logger = logging.getLogger(__name__)


class ResponseAndViewManipulationMiddleware(object):
    u"""
    Middleware that runs before Django calls view.
    """

    css_module_classname_mappings = None

    def process_view(self, request, view_func, view_args, view_kwargs):
        # =================================
        # === Populate request.ipa_site ===
        # =================================
        request.ipa_site = (
            {
                'ipa.urls_aea': 'aea',
                'ipa.urls_ipa': 'ipa',
            }
            .get(
                getattr(request, 'urlconf', None)
            )
        )

        if (
            not hasattr(request, 'resolver_match') or
            not hasattr(request.resolver_match, 'namespace') or
            request.resolver_match.namespace != 'public'
        ):
            return None

        # ===============================================================
        # === Clear get_styles.css_module_classname_mappings if debug ===
        # ===============================================================
        if (
            settings.DEBUG is True and
            hasattr(get_styles, 'css_module_classname_mappings')
        ):
            del get_styles.css_module_classname_mappings

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
            'public' in request.resolver_match.namespaces
        ):
            patch_cache_control(
                response,
                max_age=0,
                s_maxage=315360000,
                public=True,
            )

        return response
