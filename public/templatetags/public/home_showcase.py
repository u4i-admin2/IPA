# coding: utf-8

u"""Homepage prisoner showcase."""

import logging

from django.template.loader import render_to_string
from django.utils.translation import pgettext

from prisoners.models import Prisoner
from public.utils import (
    get_styles,
)
from news.models import FeaturedNews

logger = logging.getLogger(__name__)


def home_showcase(context, item_type):
    u"""
    Build the context for the home_showcase inclusion tag.

    Args:
        context (RequestContext) (injected by decorator)

    Returns:
        dictionary: Template context
    """

    if item_type == 'prisoner':
        items = list(
            (
                Prisoner.published_objects
                .filter(
                    featured=True,
                )
            )
        )

        title = pgettext(
            u'Home showcase (IPA prisoner)',
            u'Prisoner showcase'
        )

    elif item_type == 'featured_news':
        items = list(
            (
                FeaturedNews.published_objects
                .filter(
                    language=context.request.LANGUAGE_CODE,
                    featured=True,
                )
            )
        )

        title = pgettext(
            u'Home showcase (AeA featured news)',
            u'Featured news showcase'
        )

    # ==============
    # === Render ===
    # ==============
    return render_to_string(
        'home_showcase.html',
        {
            'items': items,
            'item_type': item_type,
            'styles': get_styles('home_showcase'),
            'title': title,
        },
        context.request
    )
