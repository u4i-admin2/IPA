# coding: utf-8

u"""Information box"""

import logging

from django.template.loader import render_to_string

from public.utils import (
    get_styles,
)
logger = logging.getLogger(__name__)


def information_overlay(
    context,
    slug=None,
    text=None,
    title=None,
):
    u"""
    Build the context for the information_overlay inclusion tag.

    Args:
        context (RequestContext) (injected by decorator)

    Returns:
        dictionary: Template context
    """

    # ==============
    # === Render ===
    # ==============
    return render_to_string(
        'information_overlay.html',
        {
            'slug': slug,
            'styles': get_styles('information_overlay'),
            'text': text,
            'title': title,
        },
        context.request
    )
