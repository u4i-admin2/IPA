from collections import defaultdict
from StringIO import StringIO
from django.db.models import Count, Max

from prisoners.models import PrisonerDetention, PrisonerArrest
from api.renderers import CsvRenderer
# import api.utils
from codecs import getwriter


def combine_date(year, month, day, question_mark=False):
    if year or month or day:
        bits = []
        for width, value in [(4, year), (2, month), (2, day)]:
            if value is None:
                if question_mark:
                    bits.append('?' * width)
            else:
                bits.append(unicode(value).rjust(width, '0'))

        return '/'.join(reversed(bits))


def groupby(lst, key=lambda x: x):
    dic = defaultdict(list)
    for item in lst:
        dic[key(item)].append(item)

    return dic.items()


FIELDS = [
    ('First Name (Farsi)', lambda d, c: u'{} {}'.format(d.forename_fa if d.forename_fa else '', d.surname_fa if d.surname_fa else '')),
    ('First Name (English)', lambda d, c: u'{} {}'.format(d.forename_en if d.forename_en else '', d.surname_en if d.surname_en else '')),
    ('Published', lambda d, c: d.is_published),
    ('Gender', lambda d, c: d.gender),
    ('Date of birth (Farsi)', lambda d, c: combine_date(d.dob_year_fa, d.dob_month_fa, d.dob_day_fa)),
    ('Date of birth (English)', lambda d, c: combine_date(d.dob_year, d.dob_month, d.dob_day)),
    ('Countries of citizenship', lambda d, c: ','.join(country.name_en for country in d.home_countries.all())),
    ('Ethnicity', lambda d, c: d.ethnicity and d.ethnicity.name_en),
    ('Religion', lambda d, c: d.religion and d.religion.name_en),

    ('Detained', lambda d, c: d.detention_status and d.detention_status.detained),
    ('Status (Farsi)', lambda d, c: d.detention_status and d.detention_status.name_fa),
    ('Status (English)', lambda d, c: d.detention_status and d.detention_status.name_en),
    ('Has quotes (y/n)', lambda d, c: d.quotes and d.quotes.count() > 0),
    ('Has additional evidences (y/n)', lambda d, c: d.files and d.files.count() > 0),
    ('Has profile picture (y/n)', lambda d, c: True if d.picture and d.picture.url is not None else False),
    ('Number of timeline records in Farsi', lambda d, c: len([t.description_fa for t in d.timeline.all() if t.description_fa and len(t.description_fa) > 0])),
    ('Number of timeline records in English', lambda d, c: len([t.description_en for t in d.timeline.all() if t.description_en and len(t.description_en) > 0])),
    ('Biography (Farsi)', lambda d, c: d.biography_fa),
    ('Biography (English)', lambda d, c: d.biography_en),
    ('Explanation (Farsi)', lambda d, c: d.explanation_fa),
    ('Explanation (English)', lambda d, c: d.explanation_en),
    ('Date of last detention (Farsi)', lambda d, c: combine_date(d.detention_year_fa, d.detention_month_fa, d.detention_day_fa)),
    ('Date of last detention (English)', lambda d, c: combine_date(d.detention_year, d.detention_month, d.detention_day)),
    ('Affiliated organization(s) (Farsi)', lambda d, c: ';'.join([org.organisation.name_fa for org in d.affiliations.all()])),
    ('Affiliated organization(s) (English)', lambda d, c: ';'.join([org.organisation.name_en for org in d.affiliations.all()])),
    ('Date of Arrest (Farsi)', lambda d, c: combine_date(
        c['arrest_by_prisoner'][d.id][c['arrest_num']].arrest_year_fa,
        c['arrest_by_prisoner'][d.id][c['arrest_num']].arrest_month_fa,
        c['arrest_by_prisoner'][d.id][c['arrest_num']].arrest_day_fa)
        if c['arrest_by_prisoner'].get(d.id) and len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] else ''),
    ('Date of Arrest (English)', lambda d, c: combine_date(
        c['arrest_by_prisoner'][d.id][c['arrest_num']].arrest_year,
        c['arrest_by_prisoner'][d.id][c['arrest_num']].arrest_month,
        c['arrest_by_prisoner'][d.id][c['arrest_num']].arrest_day)
        if c['arrest_by_prisoner'].get(d.id) and len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] else ''),
    ('Activity persecuted for (Farsi)', lambda d, c: (
        d.latest_activity_persecuted_for_name_fa if d.latest_activity_persecuted_for_name_fa else '')),
    ('Activity persecuted for (English)', lambda d, c: (
        d.latest_activity_persecuted_for_name_en if d.latest_activity_persecuted_for_name_en else '')),
    ('Second activities (Farsi)', lambda d, c: ';'.join([
        d.latest_secondary_activity_name_fa if d.latest_secondary_activity_name_fa else '',
        d.latest_tertiary_activity_name_fa if d.latest_tertiary_activity_name_fa else '']) if d.latest_secondary_activity_name_fa else ''),
    ('Second activities (English)', lambda d, c: ';'.join([
        d.latest_secondary_activity_name_en if d.latest_secondary_activity_name_en else '',
        d.latest_tertiary_activity_name_en if d.latest_tertiary_activity_name_en else '']) if d.latest_secondary_activity_name_en else ''),
    ('City of arrest (Farsi)', lambda d, c: c['arrest_by_prisoner'][d.id][c['arrest_num']].city.name_fa
     if c['arrest_by_prisoner'].get(d.id) and len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and c['arrest_by_prisoner'][d.id][c['arrest_num']].city else ''),
    ('City of arrest (English)', lambda d, c: c['arrest_by_prisoner'][d.id][c['arrest_num']].city.name_en
     if c['arrest_by_prisoner'].get(d.id) and len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and c['arrest_by_prisoner'][d.id][c['arrest_num']].city else ''),
    ('Charged with (Farsi)', lambda d, c: ';'.join([
        cw.name_fa for cw in c['arrest_by_prisoner'][d.id][c['arrest_num']].charged_with.all()])
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        c['arrest_by_prisoner'][d.id][c['arrest_num']].charged_with.count() > 0 else ''),
    ('Charged with (English)', lambda d, c: ';'.join([
        cw.name_en for cw in c['arrest_by_prisoner'][d.id][c['arrest_num']].charged_with.all()])
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        c['arrest_by_prisoner'][d.id][c['arrest_num']].charged_with.count() > 0 else ''),
    ('Domestic laws violated (Farsi)', lambda d, c: ';'.join([
        l.name_fa for l in c['arrest_by_prisoner'][d.id][c['arrest_num']].domestic_law_violated.all()])
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        c['arrest_by_prisoner'][d.id][c['arrest_num']].domestic_law_violated.count() > 0 else ''),
    ('Domestic laws violated (English)', lambda d, c: ';'.join([
        l.name_en for l in c['arrest_by_prisoner'][d.id][c['arrest_num']].domestic_law_violated.all()])
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        c['arrest_by_prisoner'][d.id][c['arrest_num']].domestic_law_violated.count() > 0 else ''),
    ('International laws violated (Farsi)', lambda d, c: ';'.join([
        l.name_fa for l in c['arrest_by_prisoner'][d.id][c['arrest_num']].international_law_violated.all()])
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        c['arrest_by_prisoner'][d.id][c['arrest_num']].international_law_violated.count() > 0 else ''),
    ('International laws violated (English)', lambda d, c: ';'.join([
        l.name_en for l in c['arrest_by_prisoner'][d.id][c['arrest_num']].international_law_violated.all()])
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        c['arrest_by_prisoner'][d.id][c['arrest_num']].international_law_violated.count() > 0 else ''),
    ('Judges (Farsi)', lambda d, c: ';'.join(
        [j.judge_name_fa() for j in d.get_judges_involved(c['arrest_by_prisoner'][d.id][c['arrest_num']]) if j is not None])
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        d.get_judges_involved(c['arrest_by_prisoner'][d.id][c['arrest_num']]) is not None else ''),
    ('Judges (English)', lambda d, c: ';'.join(
        [j.judge_name_en() for j in d.get_judges_involved(c['arrest_by_prisoner'][d.id][c['arrest_num']]) if j is not None])
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        d.get_judges_involved(c['arrest_by_prisoner'][d.id][c['arrest_num']]) is not None else ''),
    ('Judges behaviours (Farsi)', lambda d, c: ';'.join(
        [b.behaviour_type.name_fa for b in d.get_sentence_behaviours(c['arrest_by_prisoner'][d.id][c['arrest_num']]) if b is not None])
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        d.get_sentence_behaviours(c['arrest_by_prisoner'][d.id][c['arrest_num']]) is not None else ''),
    ('Judges behaviours (English)', lambda d, c: ';'.join(
        [b.behaviour_type.name_en for b in d.get_sentence_behaviours(c['arrest_by_prisoner'][d.id][c['arrest_num']]) if b is not None])
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        d.get_sentence_behaviours(c['arrest_by_prisoner'][d.id][c['arrest_num']]) is not None else ''),
    ('Death penalty (y/n)', lambda d, c: c['arrest_by_prisoner'][d.id][c['arrest_num']].has_death_penalty()
     if c['arrest_by_prisoner'].get(d.id) and
     len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] else ''),
    ('Life in prison (y/n)', lambda d, c: c['arrest_by_prisoner'][d.id][c['arrest_num']].has_life()
     if c['arrest_by_prisoner'].get(d.id) and
     len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] else ''),
    ('Exile (y/n)', lambda d, c: c['arrest_by_prisoner'][d.id][c['arrest_num']].has_exile()
     if c['arrest_by_prisoner'].get(d.id) and
     len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] else ''),
    ('Number of years (y/n)', lambda d, c: c['arrest_by_prisoner'][d.id][c['arrest_num']].number_of_years()
     if c['arrest_by_prisoner'].get(d.id) and
     len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] else ''),
    ('Number of months (y/n)', lambda d, c: c['arrest_by_prisoner'][d.id][c['arrest_num']].number_of_months()
     if c['arrest_by_prisoner'].get(d.id) and
     len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] else ''),
    ('File (in Rials) (y/n)', lambda d, c: c['arrest_by_prisoner'][d.id][c['arrest_num']].total_fine()
     if c['arrest_by_prisoner'].get(d.id) and
     len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] else ''),
    ('Number of lashes (y/n)', lambda d, c: c['arrest_by_prisoner'][d.id][c['arrest_num']].number_of_lashes()
     if c['arrest_by_prisoner'].get(d.id) and
     len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] else ''),
    ('Social deprivation', lambda d, c: c['arrest_by_prisoner'][d.id][c['arrest_num']].social_depravations()
     if c['arrest_by_prisoner'].get(d.id) and
     len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] else ''),
]

LIST_FIELDS = [
    # ('quote',
    #  (lambda d, c: d.quotes.all()), [
    #     ('quote_en', lambda d, c: d.quote_en),
    #     ('quote_fa', lambda d, c: d.quote_fa),
    #     ('source', lambda d, c: d.source),
    #  ]),

    # ('file',
    #  (lambda d, c: d.files.all()), [
    #     ('description_or_name', lambda d, c: d.description_en or d.name_en),
    #     ('url', lambda d, c: d.file and api.utils.absolute_urljoin(d.file.url)),
    #  ]),

    # ('comment', (lambda d, c: d.comments.all()), [
    #     ('comment', lambda d, c: d.comment)]),

    # ('source',
    #  (lambda d, c: d.sources.all()), [
    #     ('link', lambda d, c: d.link),
    #     ('name', lambda d, c: d.name),
    #     ('description', lambda d, c: d.description),
    #  ]),

    # ('relationship',
    #  (lambda d, c: d.relationships.all()), [
    #     ('forename_en', lambda d, c: d.forename_en),
    #     ('forename_fa', lambda d, c: d.forename_fa),
    #     ('surname_en', lambda d, c: d.surname_en),
    #     ('surname_fa', lambda d, c: d.surname_fa),
    #     ('relationship_type', lambda d, c: d.relationship_type.name_en),
    #  ]),

    # ('affiliation', (lambda d, c: d.affiliations.all()), [
    #     ('organisation', lambda d, c: d.organisation.name_en)]),

    # ('arrest', (lambda d, c: d.arrests.all()), [
    #     ('date', lambda d, c:
    #         combine_date(d.arrest_year, d.arrest_month, d.arrest_day)),
    #     ('city_or_province', lambda d, c:
    #         d.city.name_en if d.city else (
    #             (d.province.name_en if d.province else None))),
    #     ('case_id', lambda d, c:
    #         d.case_id and d.case_id.name_en),
    #     ('persecuted_for', lambda d, c:
    #         d.activity_persecuted_for.name_en if getattr(d, 'activity_persecuted_for') else ''),
    #     ('charged_with', lambda d, c:
    #         '|'.join(cw.name_en for cw in d.charged_with.all())),
    #     ('domestic_laws', lambda d, c:
    #         '|'.join(dm.name_en for dm in d.domestic_law_violated.all())),
    #     ('international_laws', lambda d, c:
    #         '|'.join(iw.name_en for iw in d.international_law_violated.all()))]),

    # ('sentence', (
    #     lambda d, c: c['sentences_by_prisoner'][d.id] if d.id in c['sentences_by_prisoner'] else ''), [
    #         ('judge', lambda d, c: d.judge and d.judge.surname_en),
    #         ('court', lambda d, c: d.court_and_branch and d.court_and_branch.name_en),
    #         ('judicial_behaviour', lambda d, c:
    #             '|'.join(b.behaviour_type.name_en for b in d.behaviours.all())),
    #         ('death_penalty', lambda d, c: d.death_penalty),
    #         ('fine', lambda d, c: d.fine),
    #         ('number_of_lashes', lambda d, c: d.number_of_lashes),
    #         ('months', lambda d, c: d.sentence_months),
    #         ('years', lambda d, c: d.sentence_years),
    #         ('type', lambda d, c:
    #             '|'.join(st.name_en for st in d.sentence_type.all())),
    #         ('social_depravation', lambda d, c: d.social_depravation)]),

    ('Detention', (
        lambda d, c: c['detentions_by_prisoner'][(d.id, c['arrest_by_prisoner'][d.id][c['arrest_num']].id)]
        if c['arrest_by_prisoner'].get(d.id) and
        len(c['arrest_by_prisoner'][d.id]) > c['arrest_num'] and
        (d.id, c['arrest_by_prisoner'][d.id][c['arrest_num']].id) in c['detentions_by_prisoner'] else ''), [
            ('Prison', lambda d, c: d.prison and d.prison.name_en),
            ('Date of Incarceration', lambda d, c: combine_date(d.detention_year, d.detention_month, d.detention_day)),
            ('Treatment', lambda d, c: '|'.join(pt.name_en for pt in d.treatment.all()))])
]


class PrisonerCsvRenderer(CsvRenderer):
    """
    All renderers should extend this class, setting the `media_type`
    and `format` attributes, and override the `.render()` method.
    """
    def add_list_columns(self, fields, prefix, idx, get_list_func, attr_funcs):
        list_cache = {}

        def close_attr_func(func):
            def wrapped(d, c):
                lst = list_cache.get((id(d), id(c['arrest_num'])))
                if lst is None:
                    lst = list_cache[(id(d), id(c['arrest_num']))] = list(get_list_func(d, c))
                if len(lst) > idx:
                    return func(lst[idx], c)
            return wrapped

        for attrname, attrfunc in attr_funcs:
            field_name = '%s %d %s' % (prefix, idx + 1, attrname)
            fields.append((field_name, close_attr_func(attrfunc)))

    def build_field_func_list(self):
        fields = []
        fields += FIELDS
        for idx in xrange(6):
            for prefix, getfunc, attrs in LIST_FIELDS:
                self.add_list_columns(fields, prefix, idx, getfunc, attrs)

        return fields

    def get_rows(self, queryset):
        # Pre-cache some stuff to avoid gigabytes of repetitve SQL queries.
        context = {
            # 'sentences_by_prisoner': {
            #     key: list(rows) for key, rows in groupby(
            #         (PrisonerSentence.objects
            #             .all()
            #             .order_by('arrest__prisoner_id')
            #             .select_related('arrest')
            #             .select_related('judge')
            #             .select_related('court_and_branch')
            #             .prefetch_related('behaviours')
            #             .prefetch_related('behaviours__behaviour_type')
            #             .prefetch_related('sentence_type')),
            #         lambda row: row.arrest.prisoner_id)},
            'detentions_by_prisoner': {
                key: list(rows) for key, rows in groupby(
                    (PrisonerDetention.objects
                        .all()
                        .select_related('arrest')
                        .select_related('prison')
                        .prefetch_related('treatment')),
                    lambda row: (row.arrest.prisoner_id, row.arrest.id))},
            'arrest_by_prisoner': {
                key: list(rows) for key, rows in groupby(
                    (PrisonerArrest.objects
                        .all()
                        .annotate(pcount=Count('prisoner')) \
                        .select_related('prisoner')
                        .prefetch_related('charged_with')
                        .prefetch_related('domestic_law_violated')
                        .prefetch_related('international_law_violated')
                        .order_by('-arrest_year', '-arrest_month', '-arrest_day')),
                    lambda row: row.prisoner_id)},
            'arrest_num': 1
        }

        fields = self.build_field_func_list()
        max_arrests = PrisonerArrest \
            .objects \
            .values('prisoner') \
            .annotate(pcount=Count('prisoner')) \
            .aggregate(max_arrests=Max('pcount'))['max_arrests']

        for arrest in xrange(max_arrests):
            yield ['Arrest {}'.format(arrest + 1), ]
            context['arrest_num'] = arrest
            yield [name for name, func in fields]
            for row in queryset:
                if (context['arrest_by_prisoner'].get(row.id) and
                        len(context['arrest_by_prisoner'].get(row.id)) <= arrest):
                    continue
                yield [func(row, context) for name, func in fields]
            yield []
            yield []
            yield []

    def render(self, data, media_type=None, renderer_context=None):

        queryset = data
        strio = StringIO()
        StreamWriter = getwriter('utf-8')
        buffer = StreamWriter(strio)
        for row in self.get_rows(queryset):
            for i, col in enumerate(row):
                if i:
                    buffer.write(u',')
                if col is None:
                    buffer.write(u'')
                elif col is True:
                    buffer.write(u'Y')
                elif col is False:
                    buffer.write(u'N')
                else:
                    buffer.write(u'"')
                    if isinstance(col, basestring):
                        buffer.write(
                            col.replace(u'"', u'""'))
                    else:
                        buffer.write(str(col))

                    buffer.write(u'"')
            buffer.write(u'\n')

        return buffer
