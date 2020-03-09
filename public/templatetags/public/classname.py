# coding: utf-8

u"""Get style."""

from django import template
import logging

logger = logging.getLogger(__name__)

register = template.Library()


def classname(context, style_name):
    try:
        return context['styles'][style_name]
    except KeyError:
        logger.warning(
            u'Couldn’t find style {style_name}'.format(
                style_name=style_name
            )
        )

    return ''
