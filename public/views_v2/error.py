# coding: utf-8

import logging

from django.conf import settings
from django.shortcuts import render
from django.utils.translation import pgettext
from django.views import View

from public.utils import get_view_context_with_defaults

logger = logging.getLogger(__name__)


class Error(View):
    u"""View for error pages."""

    status = 500

    def get(self, request, *args, **kwargs):
        u"""Generate a error page response.

        Args:
            **error_message (unicode): The error message to display.
            **error_title (unicode): Error title
            **status (int): HTTP status code

        Returns:
            HttpResponse
        """

        if not isinstance(
            getattr(request, 'ipa_site', None),
            basestring,
        ):
            request_host = request.get_host()

            if settings.AEA_HOSTNAME in request_host:
                request.ipa_site = 'aea'
            else:
                request.ipa_site = 'ipa'

        # ---------------------
        # --- error_message ---
        # ---------------------
        error_message = None

        if 'error_message' in kwargs:
            error_message = kwargs['error_message']

        # --------------
        # --- status ---
        # --------------
        status = self.status

        if 'status' in kwargs:
            status = kwargs['status']

        # ---------------------
        # --- error_title ---
        # ---------------------
        error_title = ''

        if 'error_title' in kwargs:
            error_title = kwargs['error_title']
        elif status == 400:
            error_title = pgettext(
                u'Error title',
                # Translators: Appears if the server can’t deal with a
                # request because it contains bad/invalid data, e.g. if an
                # invalid review is submitted
                u'Bad request',
            )
        elif status == 404:
            error_title = pgettext(
                u'Error title',
                # Translators: Default error page title
                u'The page you are looking for does not exist',
            )

            error_message = pgettext(
                u'Error message',
                # Translators: Default error page title
                u'Please contact us if you think this is an error',
            )
        else:
            error_title = pgettext(
                u'Error title',
                # Translators: Appears if the server can’t deal with a
                # request because of an unexpected server issue.
                u'Internal server error',
            )

        # ------------------
        # --- page_title ---
        # ------------------

        page_title = u'{status}: {error_title}'.format(
            status=status,
            error_title=error_title
        )

        return render(
            request,
            'error.html',
            status=status,
            context=get_view_context_with_defaults(
                {
                    'error_message': error_message,
                    'head_description': None,
                    'head_image': None,
                    'head_title': page_title,
                    'page_title': page_title,
                },
                request,
            )
        )
