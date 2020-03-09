# coding: utf-8

u"""Non-app-specific middleware (registered globally by necessity)."""

import logging

from django.conf import settings

from public.utils import ipa_reverse

logger = logging.getLogger(__name__)


class RevisionMiddleware:
    def process_response(self, request, response):
        revision = '{}b{}-{}'.format(
            str(settings.VERSION_NUM),
            str(settings.BUILD_NUM),
            str(settings.GIT_SHORT_SHA))
        response['X-Source-Revision'] = revision

        return response


class ResponseManipulationMiddleware(object):
    if hasattr(settings, 'AWS_S3_CUSTOM_DOMAIN'):
        s3_url = 'https://{s3_domain}'.format(
            s3_domain=settings.AWS_S3_CUSTOM_DOMAIN
        )
    else:
        s3_url = None

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
            (
                'api' in request.resolver_match.namespaces or
                'dashboard' in request.resolver_match.namespaces or
                'public' in request.resolver_match.namespaces or
                'ui' in request.resolver_match.namespaces
            ) and
            isinstance(settings.AWS_CLOUDFRONT_DISTRIBUTION_ID, basestring) and
            len(settings.AWS_CLOUDFRONT_DISTRIBUTION_ID) > 0 and
            isinstance(self.s3_url, basestring)
        ):
            response.content = response.content.replace(
                self.s3_url,
                ''
            )

            # Meta tags (e.g. og:url, og:image, twitter:image) should be
            # fully-qualified
            response.content = response.content.replace(
                'content="/',
                'content="{site_url}/'.format(
                    site_url=(
                        request
                        .build_absolute_uri(
                            ipa_reverse('public:homepage')
                        )
                        .replace('/en/', '')
                        .replace('/fa/', '')
                    ),
                ),
            )

        return response
