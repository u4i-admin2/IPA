# coding: utf-8

u"""Homepage showcase featured news item."""

import attr
import logging

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models.fields.files import ImageFieldFile
from django.template.loader import render_to_string

from public.utils import (
    get_styles,
)
from types import NoneType

logger = logging.getLogger(__name__)


@attr.s(frozen=True, slots=True)
class FeaturedNewsInfo(object):
    u"""
    Immutable object describing a prisoner showcase prisoner.
    """

    excerpt = attr.ib(
        validator=attr.validators.instance_of((unicode, NoneType))
    )
    link = attr.ib(
        validator=attr.validators.instance_of((str, unicode, NoneType))
    )
    photo_path = attr.ib(
        validator=attr.validators.instance_of((str, unicode, NoneType))
    )
    title = attr.ib(
        validator=attr.validators.instance_of((unicode, NoneType))
    )


def home_showcase_item_featured_news(
    context,
    featured_news
):
    u"""
    Build the context for the home_showcase_item_featured_news inclusion tag.

    Args:
        context (RequestContext) (injected by decorator)
        prisoner (Prisoner)

    Returns:
        dictionary: Template context
    """

    # -----------------------------
    # --- featured_news_title ---
    # -----------------------------
    featured_news_title = getattr(
        featured_news,
        'title',
        None
    )

    # -----------------------------
    # --- featured_news_excerpt ---
    # -----------------------------
    featured_news_excerpt = getattr(
        featured_news,
        'excerpt',
        None
    )

    # -------------------------------
    # --- featured_news_link ---
    # -------------------------------
    featured_news_link = getattr(
        featured_news,
        'link',
        None
    )

    # --------------------------------
    # --- featured_news_photo_path ---
    # --------------------------------
    featured_news_photo_path = (
        static('public/img/prison.png') + '?v=2019-08-28'
    )

    try:
        if (
            isinstance(featured_news.photo, ImageFieldFile) and
            type(featured_news.photo.url) in [str, unicode]
        ):
            featured_news_photo_path = featured_news.photo.url
    except ValueError:
        pass

    # ------------------------------------
    # --- Construct featured_news_info ---
    # ------------------------------------
    try:
        featured_news_info = FeaturedNewsInfo(
            excerpt=featured_news_excerpt,
            link=featured_news_link,
            photo_path=featured_news_photo_path,
            title=featured_news_title,
        )
    except TypeError as error:
        logger.warning(
            'Didn’t display featured news {featured_news_id} due to: {error}'.format(
                featured_news_id=featured_news.id,
                error=error,
            )
        )

        return ''

    # ==============
    # === Render ===
    # ==============
    return render_to_string(
        'home_showcase_item_featured_news.html',
        {
            'featured_news_info': featured_news_info,
            'styles': get_styles('home_showcase_item_featured_news'),
        },
        context.request
    )
