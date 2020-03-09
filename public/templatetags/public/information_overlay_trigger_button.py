# coding: utf-8

u"""Information box"""

import logging

from django.template.loader import render_to_string
from public.utils import (
    get_styles,
)

logger = logging.getLogger(__name__)


def information_overlay_trigger_button(
    context,
    position_offset_x=0,
    position_offset_y=0,
    position_type=None,
    information_overlay_slug=None,
    text=None
):
    u"""
    Build the context for the information_overlay_trigger_button inclusion tag.

    Args:
        context (RequestContext) (injected by decorator)

    Returns:
        dictionary: Template context
    """

    # ==============
    # === Render ===
    # ==============
    return render_to_string(
        'information_overlay_trigger_button.html',
        {
            'position_offset_x': position_offset_x,
            'position_offset_y': position_offset_y,
            'position_type': position_type,
            'information_overlay_slug': information_overlay_slug,
            'styles': get_styles('information_overlay_trigger_button'),
            'text': text,
        },
        context.request
    )
