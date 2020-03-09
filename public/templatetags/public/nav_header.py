# coding: utf-8

u"""Nav header."""

import attr
import logging
import re

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.translation import pgettext

from public.utils import (
    get_styles,
    ipa_reverse,
)

logger = logging.getLogger(__name__)


@attr.s(frozen=True, slots=True)
class TextLink(object):
    u"""
    Immutable object describing a prisoner showcase prisoner.
    """

    href = attr.ib(
        validator=attr.validators.instance_of((str, unicode))
    )
    text = attr.ib(
        validator=attr.validators.instance_of(unicode)
    )
    is_boxed = attr.ib(
        default=False,
        validator=attr.validators.instance_of(bool)
    )
    is_external = attr.ib(
        default=False,
        validator=attr.validators.instance_of(bool)
    )


def nav_header(context):
    u"""
    Build the context for the nav_header inclusion tag.

    Args:
        context (RequestContext) (injected by decorator)

    Returns:
        dictionary: Template context
    """

    request = context.request

    primary_links = []

    if request.ipa_site == 'ipa':
        primary_links += (
            TextLink(
                href=ipa_reverse(
                    'public:prisoners',
                ),
                text=pgettext(
                    u'Navigation header',
                    # Translators: Prisoners page link
                    u'Prisoners'
                ),
            ),
        )

    primary_links += (
        TextLink(
            href=ipa_reverse(
                'public:prisons',
            ),
            text=pgettext(
                u'Navigation header',
                # Translators: Prisons page link
                u'Prisons'
            ),
        ),
        TextLink(
            href=ipa_reverse(
                'public:judges',
            ),
            text=pgettext(
                u'Navigation header',
                # Translators: Judges page link
                u'Judges'
            ),
        ),
        TextLink(
            href=u'https://prisonatlas.com/',
            text=pgettext(
                u'Navigation header',
                # Translators: Blog (prisonatlas.com) link
                u'Blog'
            ),
            is_external=True,
        ),
    )

    secondary_links = [
        TextLink(
            href=(
                {
                    'en': u'https://united4iran.org/en/act-now.html',
                    'fa': u'https://united4iran.org/fa/act-now.html',
                }[request.LANGUAGE_CODE]
            ),
            text=pgettext(
                u'Navigation header',
                # Translators: Act now (united4iran.org) link
                u'Act now'
            ),
            is_boxed=True,
        ),
        TextLink(
            href=ipa_reverse(
                'public:about',
            ),
            text=pgettext(
                u'Navigation header',
                # Translators: About page link
                u'About'
            ),
        ),
    ]

    if request.LANGUAGE_CODE == 'en':
        secondary_links += (
            TextLink(
                href=re.sub(
                    r'^\/en',
                    '/fa',
                    request.get_full_path(),
                ),
                text=u'فارسی',
            ),
        )
    elif request.LANGUAGE_CODE == 'fa':
        secondary_links += (
            TextLink(
                href=re.sub(
                    r'^\/fa',
                    '/en',
                    request.get_full_path(),
                ),
                text=u'English',
            ),
        )

    u"""
    GH 2019-08-28: The href replacement code is necessary since the hostname exposed to Django may not be the public hostname (depending on how our servers are configured).

    A previous iteration of this code simply replaced settings.IPA_HOSTNAME with settings.AEA_HOSTNAME (or vice versa), but if the hostname exposed to Django was e.g. 'api.ipa.foo.dev' and the AeA hostname was 'aea.foo.dev', the AeA link would end up being rendered as 'api.aea.foo.dev'.

    Also note that I used this regular expression approach since it seemed to be the cleanest way to retain the scheme, port, and path of the reversed homepage URL. e.g. If we decided to build the URL from scratch, AFAIK we’d need custom code to exclude the port from the URL if it was 80 or 443 (in production) while retaining an explicit port 8000 for the Django development server.
    """
    sister_site_link_info = TextLink(
        href=re.sub(
            r'^(?P<protocol>https?:\/\/)(?P<hostname>[\w\.]*)(?P<port_and_path>:?\d*\/.*)$',
            r'\g<protocol>{hostname}\g<port_and_path>'.format(
                hostname=(
                    {
                        'aea': settings.IPA_HOSTNAME,
                        'ipa': settings.AEA_HOSTNAME,
                    }.get(request.ipa_site, '')
                )
            ),
            request.build_absolute_uri(
                ipa_reverse('public:homepage')
            ),
        ),
        text=(
            {
                'aea': pgettext(
                    u'Navigation header',
                    # Translators: Boxed IPA link
                    u'Political prisoners'
                ),
                'ipa': pgettext(
                    u'Navigation header',
                    # Translators: Boxed AeA link
                    u'Non-political prisoners'
                ),
            }.get(request.ipa_site, '')
        )
    )

    should_show_sister_site_link = settings.SHOW_SISTER_SITE_LINK

    # ==============
    # === Render ===
    # ==============
    return render_to_string(
        'nav_header.html',
        {
            'links_segments': (
                primary_links,
                secondary_links,
            ),
            'should_show_sister_site_link': should_show_sister_site_link,
            'sister_site_link_info': sister_site_link_info,
            'styles': get_styles('nav_header'),
        },
        request
    )
