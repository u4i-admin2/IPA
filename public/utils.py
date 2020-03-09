# -*- coding: utf-8 -*-

import json
import logging

from datetime import date
from types import NoneType
from urllib import urlencode

import attr

from core_types.models import Choice
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.db import connection
from django.core.urlresolvers import reverse
from django.utils.translation import (
    pgettext,
    ugettext_lazy as _,
)

from judges.models import Judge
from prisons.models import Prison
from prisoners.models import Prisoner

logger = logging.getLogger(__name__)

WA_PA_NUMERAL_MAP = {
    u'0': u'۰',
    u'1': u'۱',
    u'2': u'۲',
    u'3': u'۳',
    u'4': u'۴',
    u'5': u'۵',
    u'6': u'۶',
    u'7': u'۷',
    u'8': u'۸',
    u'9': u'۹',
}


def get_aea_current_detentions():
    """
    Return a mapping of {report_id: detention_id} for every prisoner that
    appears to currently be in detention.
    """
    c = connection.cursor()
    c.execute("""
    WITH ordered_detentions_by_report_id AS (
    SELECT
        report.id AS report_id,
        detention.id AS detention_id,
        ROW_NUMBER() OVER(
            PARTITION BY report.id
            ORDER BY detention.detention_year DESC,
                     detention.detention_month DESC,
                     detention.detention_day DESC
        ) AS row_number
    FROM report_reportdetention detention
    LEFT JOIN prisons_prison prison
        ON (prison.id = detention.prison_id)
    LEFT JOIN report_report report
        ON (report.id = detention.report_id)
    WHERE
        detention.detention_year IS NOT NULL
        AND prison.is_published IS TRUE
        AND report.is_published IS TRUE
        AND detention.is_published IS TRUE
    )
    SELECT
        report_id,
        detention_id
    FROM ordered_detentions_by_report_id
    WHERE row_number = 1
    """)
    return dict(c)


def get_ipa_current_detentions():
    """
    Return a mapping of {prisoner_id: detention_id} for every prisoner that
    appears to currently be in detention.
    """
    c = connection.cursor()
    c.execute("""
    WITH ordered_detentions_by_prisoner_id AS (
    SELECT
        prisoner.id AS prisoner_id,
        detention.id AS detention_id,
        ROW_NUMBER() OVER(
            PARTITION BY prisoner.id
            ORDER BY detention.detention_year DESC,
                     detention.detention_month DESC,
                     detention.detention_day DESC
        ) AS row_number
    FROM prisoners_prisonerdetention detention
    LEFT JOIN prisons_prison prison
        ON (prison.id = detention.prison_id)
    LEFT JOIN prisoners_prisonerarrest arrest
        ON (detention.arrest_id = arrest.id)
    LEFT JOIN prisoners_prisoner prisoner
        ON (prisoner.id = arrest.prisoner_id)
    LEFT JOIN prisoners_detentionstatus status
        ON (prisoner.detention_status_id = status.id)
    WHERE
        prison.is_published IS TRUE
        AND prisoner.is_published IS TRUE
        AND arrest.is_published IS TRUE
        AND detention.is_published IS TRUE
        AND prisoner.detention_status_id IS NOT NULL
        AND status.detained IS TRUE
    )
    SELECT
        prisoner_id,
        detention_id
    FROM ordered_detentions_by_prisoner_id
    WHERE row_number = 1
    """)
    return dict(c)


def values_counter(the_dict, the_key):
    if callable(the_key):
        try:
            the_key = the_key()
        except AttributeError:
            the_key = None

    if the_key is None:
        the_key = 'Unknown'
    try:
        the_dict[the_key] += 1
    except KeyError:
        the_dict[the_key] = 1


class SetEncoder(json.JSONEncoder):
    # because sets are not serializable
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


def judge_paragraph(language, **kwargs):
    firstname = kwargs.get('forename', '')
    surname = kwargs.get('surname', '')
    religion = kwargs.get('religion', '')
    gender = kwargs.get('gender', '')
    arrest_date = kwargs.get('arrest_date', '')
    sentence_years = kwargs.get('sentence_years', '')
    lashes = kwargs.get('lashes', '')
    activity = kwargs.get('activity', '')

    if gender == 'm':
        if language == 'en':
            gender = "male"
        else:
            gender = u"مرد"
    elif gender == 'f':
        if language == 'en':
            gender = "female"
        else:
            gender = u"زن"

    if religion == _("Unknown"):
        religion = None

    text = u""

    if language == 'en':
        if firstname or surname:
            text += '%s  %s ' % (firstname, surname)

        if (gender and not religion) or (religion and not gender):
            text += 'a %s ' % (gender or religion)

        if gender and religion:
            text += 'a %s %s ' % (gender, religion)

        if arrest_date and text != '':
            text += 'who was arrested on %s ' % (arrest_date)

        if arrest_date and sentence_years and lashes:
            text += 'and sentenced to %s in prison and %s ' % (sentence_years, lashes)

        if activity:
            text += 'for being a %s ' % (activity)
    else:
        if firstname or surname:
            text += '%s  %s ' % (firstname, surname)

        if (gender and not religion) or (religion and not gender):
            text += u'یک %s ' % (gender or religion)

        if gender and religion:
            text += u'یک %s %s ' % (gender, religion)

        if arrest_date and text != '':
            text += u'بازداشت شده در %s ' % (arrest_date)

        if arrest_date and sentence_years and lashes:
            text += u'و محکوم به %s زندان %s ' % (sentence_years, lashes)

        if activity:
            text += u'فعالت منجر به پیگرد قانونی %s ' % (activity)
    return text


def get_styles(module_name):
    if not hasattr(get_styles, 'has_shown_got_style_mappings_log'):
        get_styles.has_shown_got_style_mappings_log = False

    if not hasattr(get_styles, 'css_module_classname_mappings'):
        try:
            with open('static/css-module-classname-mappings.json') as f:
                get_styles.css_module_classname_mappings = json.load(f)

                if not get_styles.has_shown_got_style_mappings_log:
                    logger.info('Got style mappings from static/css-module-classname-mappings.json')

                    get_styles.has_shown_got_style_mappings_log = True
        except IOError:
            get_styles.css_module_classname_mappings = {}

            raise IOError('Couldn’t open static/css-module-classname-mappings.json, which is required for CSS modules. You probably need to run `gulp dev` or `gulp`.')

    try:
        return get_styles.css_module_classname_mappings[module_name]
    except KeyError:
        raise KeyError('Requested CSS module doesn\'t exist.')


def ipa_reverse(viewname, **kwargs):
    u"""
    Augmented replacement for Django’s django.urls.reverse that renders URLs
    with both path arguments (i.e. Django URL named group arguments) and query
    string arguments (which Django’s URL helpers don’t handle).

    Path arguments should be prefixed with `p_`; query string arguments should
    be prefixed with `q_`.

    The arguments are prefixed and mixed rather than separated into
    dictionaries because this function is also wrapped as path_url template tag
    and template tags can’t take dict arguments. It would probably be confusing
    if ipa_reverse and ipa_url took different kwargs.

    e.g.:

    ipa_reverse(
        'public:prisoner',
        p_pk=2149,
        q_foo='bar',
    )
    /en/prisoner/2149/?foo=bar

    Arguments:
        viewname (str): Django URL pattern name
        **kwargs: Mixed path and query string arguments

    Returns:
        path_and_query_string (str) (absolute path and query string, doesn’t
            include hostname)
    """
    path_args = {}
    query_string_args = {}

    for key in kwargs:
        if key.startswith('p_'):
            path_args[key.replace('p_', '')] = kwargs[key]
            continue
        elif key.startswith('q_'):
            query_string_args[key.replace('q_', '')] = kwargs[key]
            continue

    path_and_query_string = reverse(viewname, kwargs=path_args)

    if len(query_string_args) > 0:
        path_and_query_string += ('?' + urlencode(query_string_args))

    return path_and_query_string


def get_localized_choice_instance_name(choice_instance, language_code):
    if not isinstance(choice_instance, Choice):
        return None

    return getattr(
        choice_instance,
        'name_{language_code}'.format(
            language_code=language_code,
        ),
        None
    )


@attr.s(frozen=True, slots=True)
class EntityCounts(object):
    u"""
    Immutable object describing a homepage navigation box.
    """

    judge = attr.ib(
        validator=attr.validators.instance_of(int)
    )
    prison = attr.ib(
        validator=attr.validators.instance_of(int)
    )
    prisoner = attr.ib(
        validator=attr.validators.instance_of((int, NoneType))
    )


def get_entity_counts(request):
    if (
        hasattr(request, 'ipa_entity_counts') and
        isinstance(request.ipa_entity_counts, EntityCounts)
    ):
        return request.ipa_entity_counts

    # -------------------
    # --- judge_count ---
    # -------------------
    judge_count = (
        Judge.published_objects
        .count()
    )

    # --------------------
    # --- prison_count ---
    # --------------------
    prison_count_query_filter_args = {}

    if request.ipa_site == 'aea':
        prison_count_query_filter_args['administered_by__in'] = (
            settings.AEA_PRISON_ADMINISTERED_BY_WHITELIST
        )

    prison_count = (
        Prison.published_objects
        .filter(**prison_count_query_filter_args)
        .count()
    )

    # ----------------------
    # --- prisoner_count ---
    # ----------------------
    prisoner_count = None

    if request.ipa_site == 'ipa':
        prisoner_count = (
            Prisoner.published_objects
            .filter(
                detention_status__detained=True
            )
            .count()
        )

    # -----------------------------------
    # --- Return EntityCount instance ---
    # -----------------------------------

    request.ipa_entity_counts = EntityCounts(
        judge=judge_count,
        prison=prison_count,
        prisoner=prisoner_count,
    )

    return request.ipa_entity_counts


def get_view_context_with_defaults(context, request):
    # ------------------------
    # --- head_description ---
    # ------------------------
    if 'head_description' not in context:
        entity_counts = get_entity_counts(request)

        if request.ipa_site == 'aea':
            context['head_description'] = pgettext(
                u'Home',
                # Translators: Social media/search engine site description
                u'Prisons across Iran are serving out sentences issued by {judge_count} judges. Want to find out more? Explore Atlas Agahi.'
            ).format(
                judge_count=entity_counts.judge,
                prison_count=entity_counts.prison,
            )
        elif request.ipa_site == 'ipa':
            context['head_description'] = pgettext(
                u'Home',
                # Translators: Social media/search engine site description
                u'{prisoner_count} political prisoners are currently detained in {prison_count} prisons across Iran serving out sentences issued by {judge_count} judges. Want to find out more? Explore Iran Prison Atlas.'
            ).format(
                judge_count=entity_counts.judge,
                prison_count=entity_counts.prison,
                prisoner_count=entity_counts.prisoner,
            )

    if request.LANGUAGE_CODE == 'fa':
        context['head_description'] = replace_wa_numerals_with_pa_numerals(
            context['head_description']
        )

    # ------------------
    # --- head_image ---
    # ------------------
    if context.get('head_image', None) is None:
        context['head_image'] = request.build_absolute_uri(
            static('public/img/og_Intro_Screen_FB_2.png') + '?v=2019-08-28'
        )

    if not context['head_image'].startswith('http'):
        context['head_image'] = request.build_absolute_uri(
            context['head_image']
        )

    # ------------------
    # --- head_title ---
    # ------------------
    site_title = None

    if request.ipa_site == 'aea':
        site_title = pgettext(
            u'General',
            u'Atlas Agahi',
        )
    else:
        site_title = pgettext(
            u'General',
            u'Iran Prison Atlas',
        )

    page_title = context.get('head_title', None)

    if isinstance(site_title, unicode):
        if isinstance(page_title, basestring):
            if request.LANGUAGE_CODE == 'fa':
                page_title = replace_wa_numerals_with_pa_numerals(page_title)

            context['head_title_document'] = u'{page_title} — {site_title}'.format(
                page_title=page_title,
                site_title=site_title,
            )

            context['head_title_social'] = page_title
        else:
            context['head_title_document'] = site_title
            context['head_title_social'] = site_title

    return context


def replace_wa_numerals_with_pa_numerals(input):
    u"""
    Return input string with all Western Arabic numerals replaced by
    Perso-Arabic numerals.

    See https://en.wikipedia.org/wiki/Eastern_Arabic_numerals

    Args:
        input (str/unicode)
    Returns:
        unicode
    """

    input = unicode(input)

    for wa_numeral in WA_PA_NUMERAL_MAP:
        input = input.replace(wa_numeral, WA_PA_NUMERAL_MAP[wa_numeral])

    return input
