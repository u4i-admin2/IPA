# coding: utf-8

u"""Homepage prisoner showcase."""

import attr
import logging

from datetime import date
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db.models.fields.files import ImageFieldFile
from django.template.loader import render_to_string
from django.utils.translation import pgettext
from easy_thumbnails.files import get_thumbnailer

from public.utils import (
    get_localized_choice_instance_name,
    get_styles,
    ipa_reverse,
)
from types import NoneType

logger = logging.getLogger(__name__)


@attr.s(frozen=True, slots=True)
class PrisonerInfo(object):
    u"""
    Immutable object describing a prisoner showcase prisoner.
    """

    age = attr.ib(
        validator=attr.validators.instance_of((int, NoneType))
    )
    biography = attr.ib(
        validator=attr.validators.instance_of((unicode, NoneType))
    )
    country = attr.ib(
        validator=attr.validators.instance_of((unicode, NoneType))
    )
    ethnicity = attr.ib(
        validator=attr.validators.instance_of((unicode, NoneType))
    )
    name = attr.ib(
        validator=attr.validators.instance_of((unicode, NoneType))
    )
    picture_path = attr.ib(
        validator=attr.validators.instance_of((str, unicode, NoneType))
    )
    religion = attr.ib(
        validator=attr.validators.instance_of((unicode, NoneType))
    )
    url = attr.ib(
        validator=attr.validators.instance_of((str, unicode, NoneType))
    )


def home_showcase_item_prisoner(
    context,
    prisoner
):
    u"""
    Build the context for the home_showcase_item_prisoner inclusion tag.

    Args:
        context (RequestContext) (injected by decorator)
        prisoner (Prisoner)

    Returns:
        dictionary: Template context
    """

    language_code = context.request.LANGUAGE_CODE

    prisoner_age = None
    prisoner_biography = None
    prisoner_country = None
    prisoner_ethnicity = None
    prisoner_name = None
    prisoner_picture_path = None
    prisoner_religion = None

    # --------------------
    # --- prisoner_age ---
    # --------------------

    try:
        prisoner_date_of_birth = date(
            prisoner.dob_year,
            prisoner.dob_month,
            prisoner.dob_day,
        )

        today_date = date.today()

        # Via https://stackoverflow.com/a/9754466/7949868
        prisoner_age = (
            today_date.year -
            prisoner_date_of_birth.year -
            (
                (
                    today_date.month,
                    today_date.day
                ) <
                (
                    prisoner_date_of_birth.month,
                    prisoner_date_of_birth.day
                )
            )
        )
    except TypeError:
        pass

    # --------------------------
    # --- prisoner_biography ---
    # --------------------------
    prisoner_biography = (
        prisoner.biography if language_code == 'en'
        else prisoner.biography_fa
    )

    # ------------------------
    # --- prisoner_country ---
    # ------------------------
    prisoner_country = get_localized_choice_instance_name(
        prisoner.home_countries.first(),
        language_code
    )

    # --------------------------
    # --- prisoner_ethnicity ---
    # --------------------------
    prisoner_ethnicity = get_localized_choice_instance_name(
        prisoner.ethnicity,
        language_code
    )

    # ---------------------
    # --- prisoner_name ---
    # ---------------------
    prisoner_name = (
        u'{forename} {surname}'
        .format(
            forename=(
                getattr(
                    prisoner,
                    'forename_{language_code}'.format(
                        language_code=language_code,
                    ),
                ) or ''
            ),
            surname=(
                getattr(
                    prisoner,
                    'surname_{language_code}'.format(
                        language_code=language_code,
                    ),
                ) or ''
            ),
        )
        .strip()
    )

    if prisoner_name == '':
        prisoner_name = pgettext(
            u'Home showcase (IPA prisoner)',
            # Translators: Used if prisoner has no forename and surname
            u'Name unknown'
        )

    # -----------------------------
    # --- prisoner_picture_path ---
    # -----------------------------
    try:
        if (
            isinstance(prisoner.picture, ImageFieldFile) and
            type(prisoner.picture.url) in [str, unicode]
        ):
            prisoner_picture_path = (
                get_thumbnailer(prisoner.picture)
                .get_thumbnail({
                    'size': (200, 200)
                })
                .url
            )
    except ValueError:
        prisoner_picture_path = None

    if prisoner_picture_path is None:
        if prisoner.gender == 'M':
            prisoner_picture_path = (
                static('public/img/prisoner_male.png') + '?v=2019-08-28'
            )
        elif prisoner.gender == 'F':
            prisoner_picture_path = (
                static('public/img/prisoner_female.png') + '?v=2019-08-28'
            )

    # -------------------------
    # --- prisoner_religion ---
    # -------------------------
    prisoner_religion = get_localized_choice_instance_name(
        prisoner.religion,
        language_code
    )

    prisoner_url = ipa_reverse(
        'public:prisoner',
        p_pk=prisoner.id,
    )

    # -------------------------------
    # --- Construct prisoner_info ---
    # -------------------------------
    try:
        prisoner_info = PrisonerInfo(
            age=prisoner_age,
            biography=prisoner_biography,
            country=prisoner_country,
            ethnicity=prisoner_ethnicity,
            name=prisoner_name,
            picture_path=prisoner_picture_path,
            religion=prisoner_religion,
            url=prisoner_url,
        )
    except TypeError as error:
        logger.warning(
            'Didn’t display prisoner {prisoner_id} due to: {error}'.format(
                prisoner_id=prisoner.id,
                error=error,
            )
        )

        return ''

    # ==============
    # === Render ===
    # ==============
    return render_to_string(
        'home_showcase_item_prisoner.html',
        {
            'prisoner_info': prisoner_info,
            'styles': get_styles('home_showcase_item_prisoner'),
        },
        context.request
    )
