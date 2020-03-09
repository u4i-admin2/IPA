# coding: utf-8

u"""Get fully-qualified current URL."""

from django import template
import logging

logger = logging.getLogger(__name__)

register = template.Library()


def current_url_fully_qualified(context):
    return context.request.build_absolute_uri(
        context.request.path
    )
