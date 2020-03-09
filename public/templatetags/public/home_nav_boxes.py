# coding: utf-8

u"""Homepage nav boxes."""

import attr
import logging

from django.template.loader import render_to_string
from django.utils.translation import pgettext

from public.utils import (
    get_entity_counts,
    ipa_reverse,
    get_styles,
)

logger = logging.getLogger(__name__)


@attr.s(frozen=True, slots=True)
class NavBoxInfo(object):
    u"""
    Immutable object describing a homepage navigation box.
    """

    background_img_src = attr.ib(
        validator=attr.validators.instance_of(unicode)
    )
    count = attr.ib(
        validator=attr.validators.instance_of(int)
    )
    description = attr.ib(
        validator=attr.validators.instance_of(unicode)
    )
    href = attr.ib(
        validator=attr.validators.instance_of(unicode)
    )
    name = attr.ib(
        validator=attr.validators.instance_of(unicode)
    )


def home_nav_boxes(context):
    u"""
    Build the context for the home_nav_boxes inclusion tag.

    Args:
        context (RequestContext) (injected by decorator)

    Returns:
        dictionary: Template context
    """

    static_format_string = u'public/img/{file_name}'

    nav_box_infos = []

    entity_counts = get_entity_counts(context.request)

    # ==================
    # === Judges box ===
    # ==================
    nav_box_infos.append(
        NavBoxInfo(
            background_img_src=static_format_string.format(
                file_name=u'Judges-{site}.jpg'.format(
                    site=context.request.ipa_site
                )
            ),
            count=entity_counts.judge,
            description=pgettext(
                u'Home nav box',
                # Translators: Nav box description text (small text under divider)
                u'Click to explore the sentences handed down by some of Iran’s harshest judges'
            ),
            href=ipa_reverse(
                'public:judges',
            ),
            name=pgettext(
                u'Home nav box',
                # Translators: Nav box description title (large text beneath number)
                u'Judges'
            ),
        )
    )

    # =====================
    # === Prisoners box ===
    # =====================
    if context.request.ipa_site == 'ipa':
        nav_box_infos.append(
            NavBoxInfo(
                background_img_src=static_format_string.format(
                    file_name=u'Prisoners-{site}.jpg'.format(
                        site=context.request.ipa_site
                    )
                ),
                count=entity_counts.prisoner,
                description=pgettext(
                    u'Home nav box',
                    # Translators: Nav box description text (small text under divider)
                    u'Click to explore the lives and sentences of Iran’s political prisoners'
                ),
                href=ipa_reverse(
                    'public:prisoners',
                ),
                name=pgettext(
                    u'Home nav box',
                    # Translators: Nav box description title (large text beneath number)
                    u'Prisoners'
                ),
            )
        )

    # ==================
    # === Prison box ===
    # ==================
    nav_box_infos.append(
        NavBoxInfo(
            background_img_src=static_format_string.format(
                file_name=u'Prison-{site}.jpg'.format(
                    site=context.request.ipa_site
                )
            ),
            count=entity_counts.prison,
            description=pgettext(
                u'Home nav box',
                # Translators: Nav box description text (small text under divider)
                u'Click to explore the prisons that hold Iran’s political prisoners behind their bars'
            ),
            href=ipa_reverse(
                'public:prisons',
            ),
            name=pgettext(
                u'Home nav box',
                # Translators: Nav box description title (large text beneath number)
                u'Prisons'
            ),
        )
    )

    # ==============
    # === Render ===
    # ==============
    return render_to_string(
        'home_nav_boxes.html',
        {
            'nav_box_infos': nav_box_infos,
            'styles': get_styles('home_nav_boxes'),
        },
        context.request
    )
