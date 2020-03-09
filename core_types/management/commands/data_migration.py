# -- coding: utf-8 --
"""
The point of this is to import all the prisoner info.
Currently, it just lists all the info.

Before running this you need to python manage.py core_types
"""

from __future__ import absolute_import
import logging
import os
import sys

import requests
import django.core.management.base
from django.db import connections
from django.db.models import Q
from django.conf import settings

import core_types.models
import judges.models
import prisoners.models
import prisons.models

from . import jalali
from . import static_data


LOG = logging.getLogger('data_migration')


class Command(django.core.management.base.BaseCommand):
    help = 'python manage.py prisoners - imports prisoners from wp'

    def get_meta_values(self, pris_id):
        record = {}
        cursor = connections['wp'].cursor()
        cursor.execute("SELECT meta_key, meta_value\
            FROM wp_postmeta\
            WHERE post_id = %s AND meta_value != ''", [pris_id])

        for row in cursor.fetchall():
            if row[0] not in record:
                record[row[0]] = row[1]
            else:
                try:
                    record[row[0]].append(row[1])
                except AttributeError:
                    # change string to list
                    ls = []
                    ls.append(record[row[0]])
                    ls.append(row[1])
                    record[row[0]] = ls
        return record

    GENDER_MAP = {
        '10021': 'F',
        '10022': 'M'
    }

    def get_gender(self, gender_code):
        return self.GENDER_MAP.get(gender_code, '')

    def get_values(self, dct, key):
        if key:
            return dct[key]['EN'], dct[key]['FA']
        else:
            return '', ''

    def get_multi_values(self, dct, key):
        if isinstance(key, list):
            en_items = []
            fa_items = []
            for k in key:
                en_items.append(dct[k]['EN'])
                fa_items.append(dct[k]['FA'])
            return en_items, fa_items
        elif key and key in dct:
            return [dct[key]['EN']], [dct[key]['FA']]
        else:
            return '', ''

    def try_int(self, s):
        if s.isdigit():
            return int(s, 10)

    def translate_date(self, dct, prefix, fa_dob):
        if not fa_dob:
            return

        # dob is in this format -> 1372-00-00
        # first split date into 3
        parts = map(self.try_int, fa_dob.split("-"))
        if len(parts) < 3:
            return None
        if not (parts[0] and parts[0] > 1000):
            return None

        dct[prefix + 'year_fa'] = parts[0]
        if parts[1] and parts[1] <= 12:
            dct[prefix + 'month_fa'] = parts[1]
        if parts[2] and parts[2] <= 31:
            dct[prefix + 'day_fa'] = parts[2]

        en_date = jalali.Persian(dct[prefix + 'year_fa'],
                                 dct.get(prefix + 'month_fa', 1),
                                 dct.get(prefix + 'day_fa', 1))

        dct[prefix + 'year'] = en_date.gregorian_year
        if parts[1]:
            dct[prefix + 'month'] = en_date.gregorian_month
        if parts[2]:
            dct[prefix + 'day'] = en_date.gregorian_day

    def get_city(self, city_code):
        """
        This is a lookup because there are loads of 'cities' and also,
        I'm not sure if they haven't just being putting anything here, ie countries, regions etc
        """
        if city_code == 'NO KEY':
            return 'NO KEY', 'NO KEY'
        cursor = connections['wp'].cursor()
        cursor.execute("SELECT en_lang, fa_lang\
            FROM wp_ppd_repository\
            WHERE uid = %s", [city_code])
        row = cursor.fetchone()
        return row[0], row[1]

    def get_free_text(self, record):
        lines = []

        def add(s, *args):
            lines.append(s % args)

        def add_one(label, s):
            if s:
                if not isinstance(s, unicode):
                    s = s.decode('utf-8')
                if s.strip():
                    add(label, s.strip())

        def add_list(label, vals):
            vals = filter(None, vals)
            if vals:
                add(label)
                for val in vals:
                    if not isinstance(val, unicode):
                        val = val.decode('utf-8')
                    add('   %s', val)

        en_marriage, fa_marriage = self.get_values(
            static_data.MARITAL_STATUS,
            record.get('10010'))

        add_one('EN - marital status: %s', en_marriage)
        add_one('FA - marital status: %s', fa_marriage.decode('utf-8'))

        add_one('EN - family status: %s', record.get('10014_en'))
        add_one('FA - family status: %s', record.get('10014_fa'))

        add_one('EN - bio: %s', record.get('10630_en'))
        add_one('FA - bio: %s', record.get('10630_fa'))

        add_one('EN - current sentence: %s', record.get('10414_en'))
        add_one('FA - current sentence: %s', record.get('10414_fa'))

        add_one('EN - prosecution details: %s', record.get('10428_en'))
        add_one('FA - prosecution details: %s', record.get('10428_fa'))

        add_one('EN - prison treatment: %s', record.get('10460_en'))
        add_one('FA - prison treatment: %s', record.get('10460_fa'))

        en_vals, fa_vals = self.get_multi_values(
            static_data.SENTENCES,
            record.get('10400'))

        add_list('EN - sentence info:', en_vals)
        add_list('FA - sentence info:', fa_vals)

        en_vals, fa_vals = self.get_multi_values(
            static_data.PROSECUTION_INFO,
            record.get('10420'))

        add_list('EN - prosecution info:', en_vals)
        add_list('FA - prosecution info:', fa_vals)

        sources = [record.get(str(i)) for i in xrange(10741, 10791)]
        add_list('Sources:', sources)
        return lines

    def _get_string_list(self, record, key):
        vals = record.get(key)
        if not vals:
            return []
        if isinstance(vals, basestring):
            return [vals]
        return vals

    # Must pop any old classes which don't map correctly.
    # 10612: Artist: u'\u0647\u0646\u0631\u0645\u0646\u062f'
    # 10612: Writer: u'\u0646\u0648\u06cc\u0633\u0646\u062f\u0647'
    # 10608: Blogger: u'\u0628\u0644\u0627\u06af\u0631'
    # 10608: Journalist: u'\u0631\u0648\u0632\u0646\u0627\u0645\u0647\u200c\u0646\u06af\u0627\u0631'
    def activities_from_rec(self, record, prisoner, comments):
        vals = self._get_string_list(record, '10601')
        if '10612' in vals:
            vals.remove('10612')
            comments.append('Previously marked as artist/writer, '
                            'but now this is 2 separate categories.')
            prisoner.needs_attention = True

        if '10608' in vals:
            vals.remove('10608')
            comments.append('Previously marked as blogger/journalist, '
                            'but now this is 2 separate categories.')
            prisoner.needs_attention = True

        names = [static_data.ACTIVITIES_MAP[v] for v in vals]
        elems = list(prisoners.models.ActivityPersecutedFor.objects.filter(
                     name_en__in=names))
        if len(elems) == 1:
            return elems[0]
        elif elems:
            LOG.error("got multiple activities persecuted for: %r", elems)
            return None
        return None

    def chargedwiths_from_rec(self, record):
        vals = self._get_string_list(record, '10300')
        if '10314' in vals:  # remove 'other'
            vals.remove('10314')
        names = [static_data.CHARGED_WITH[item]['EN'] for item in vals]
        return list(prisoners.models.ChargedWith.objects.filter(
            name_en__in=names))

    def domestics_from_rec(self, record):
        vals = self._get_string_list(record, '10501')
        names = [static_data.DOMESTIC_LAW_VIOLATED[item]['EN'] for item in vals]
        return list(prisoners.models.DomesticLawViolated.objects.filter(
            name_en__in=names))

    def intls_from_rec(self, record):
        vals = self._get_string_list(record, '10530')
        names = [static_data.INTL_LAW_VIOLATED[item]['EN'] for item in vals]
        return list(prisoners.models.InternationalLawViolated.objects.filter(
            name_en__in=names))

    def treatments_from_rec(self, record):
        vals = self._get_string_list(record, '10450')
        names = [static_data.TREATMENT_IN_PRISON[item]['EN'] for item in vals]
        return list(prisoners.models.PrisonTreatment.objects.filter(
            name_en__in=names))

    def handle(self, *args, **options):
        logging.basicConfig(level=logging.INFO)
        LOG.info('Starting prisoner import')

        # Prevent very expensive queries/updates running every time we do
        # basically anything.
        prisoners.models.Prisoner._is_updating_cache_fields = True

        # First of all, the PID means nothing!  The prisoner 'PID' is actually
        # the post title (see around line 423). So what we do is take the
        # post_title from each ppd and get all the meta values for that post in
        # a lovely python dictionary.
        #
        # I'm not sure but i think conflictd and considerations is empty but
        # either way it needs to be checked.
        #
        # kind of redundant, as we already have all prisons build but this will
        # help us map old id to prison name

        self.all_prisons = {}
        with connections['wp'].cursor() as cursor:
            cursor.execute("""
                SELECT uid, en_lang, fa_lang
                FROM wp_ppd_repository
                WHERE uid BETWEEN %s AND %s
            """, [15001, 15076])
            for row in cursor.fetchall():
                if row[1] or row[2]:
                    self.all_prisons[row[0]] = {'EN': row[1], 'FA': row[2]}

        self.all_judges = {}
        self.all_courts = {}
        with connections['wp'].cursor() as cursor:
            cursor.execute("""
                SELECT uid, en_lang, fa_lang
                FROM wp_ppd_repository
                WHERE
                    uid BETWEEN %s
                    AND %s OR uid BETWEEN %s AND %s
            """, [10341, 10390, 13001, 13095])

            for row in cursor.fetchall():
                en_list = row[1].split('"')
                fa_list = row[2].split('"')

                if en_list[1] != '' and fa_list[1] != '':
                    self.all_judges[row[0]] = {'EN': en_list[1], 'FA': fa_list[1]}

                if en_list[3] != '' and fa_list[3] != '':
                    self.all_courts[row[0]] = {'EN': en_list[3], 'FA': fa_list[3]}

        with connections['wp'].cursor() as cursor:
            # ok let's go
            cursor.execute("""
                SELECT ID, post_title, post_status
                FROM wp_posts
                WHERE
                    post_type = 'ppd_profile'
                    AND post_title != 'Auto Draft'
                """)

            for row in cursor.fetchall():
                # you need this one to get the meta data
                # print('Prisoner UID: %s' % int(row[0]))
                # you need this one to find the pris @ this url:
                # http://united4iran.org/political-prisoners-database/profiles/pid/
                # print('Prisoner ID: %s' % int(row[1]))

                record = self.get_meta_values(int(row[0]))
                comments = self.get_free_text(record)
                prisoner = self.make_prisoner(row, record, comments)
                self.make_arrest(record, prisoner, comments)
                self.make_sentences(record, prisoner, comments)
                self.make_detentions(record, prisoner, comments)

                prisoners.models.PrisonerComment.objects.create(
                    prisoner=prisoner,
                    comment=u'\n'.join(comments))

        LOG.info("That was %s ppd profiles" % str(cursor.rowcount))
        LOG.info("Updating summary fields...")

        prisoners.models.Prisoner._is_updating_cache_fields = False
        for prisoner in prisoners.models.Prisoner.objects.all():
            prisoner.update_summary_fields()

    def sql_row(self, sql, args=()):
        with connections['wp'].cursor() as c:
            c.execute(sql, args)
            for row in c:
                return row

    def get_image(self, url):
        destination = os.path.join(settings.MEDIA_ROOT, 'prisoner_pics')
        dest_path = destination + '/' + url.split("/")[-1]

        if os.path.exists(dest_path):
            LOG.debug('Already have image: %r', url)
            return '/'.join(dest_path.split("/")[-2:])

        # get actual img name 024.jpg
        response = requests.get(url)
        if response.status_code == 200:
            f = open(dest_path, 'wb')
            f.write(response.content)
            f.close()
            return '/'.join(dest_path.split("/")[-2:])
        elif response.status_code == 404:
            return None
        else:
            LOG.info('%r', response.status_code)
            LOG.info(url)
            LOG.info(dest_path)
            sys.exit()

    def import_profile_pic(self, row):
        """
        get profile pic from their server and attach it to pris

        Url is either like this:
        http://united4iran.org/wp-content/uploads/Mohsen-Mirdamadi.jpg
        OR like this:
        /data/b/o/bot.sk/sub/ppd/content/uploads/51430_01.jpg

        In case of the second instance, we rewrite the url (presuming this
        is what the code base does)
        """
        try:
            guid, = self.sql_row("""
                SELECT guid FROM wp_posts
                WHERE post_parent = %s AND post_type = 'attachment'
            """, [int(row[0])])
        except TypeError:
            return None

        if guid.startswith('http://united4iran.org'):
            url = guid
        elif 'data/b/o/bot.sk/sub/ppd' in guid or 'ppd.united4iran.org' in guid:
            start_url = 'http://united4iran.org/wp-content/'
            url = start_url + "/".join(guid.split("/")[-2:])
        else:
            LOG.warning('Img path doesnt fit expectations: %r', url)
            return None

        return self.get_image(url)

    def make_prisoner(self, row, record, comments):
        # Conflicts and considerations.
        comments.append(record.get('10731', ''))

        religion_en, religion_fa = self.get_values(static_data.RELIGIONS, record.get('10050'))
        ethnicity_en, ethnicity_fa = self.get_values(static_data.ETHNICITIES, record.get('10070'))

        if religion_en == 'Christian':
            comments.append('Prisoner is Christian, but the previous '
                            'system didn\'t define which type')

        religion = (core_types.models.Religion.objects.all()
                    .filter(name_en=religion_en, name_fa=religion_fa)
                    .first())

        ethnicity = (core_types.models.Ethnicity.objects.all()
                     .filter(name_en=ethnicity_en, name_fa=ethnicity_fa)
                     .first())

        # let's start with detention status
        status = None
        val = record.get('10110')
        if val:
            status = prisoners.models.DetentionStatus.objects.get(
                name_en=static_data.DETENTION_STATUS[val]['EN'])

        # In previous system data was only stored in farsi as string
        # In new system, we'll use approximatedatefield and store in gregorian
        # old dob is in this format -> 1372-00-00
        defaults = {}
        self.translate_date(defaults, 'dob_', record.get('10040'))

        # Create prisoner.
        return prisoners.models.Prisoner.objects.create(
            gender=self.get_gender(record.get('10020')),
            forename_en=record.get('10001_en'),
            forename_fa=record.get('10001_fa'),
            surname_en=record.get('10002_en'),
            surname_fa=record.get('10002_fa'),
            # no idea why there is both published and publish
            picture=self.import_profile_pic(row),
            religion=religion,
            ethnicity=ethnicity,
            is_published=row[2] in ('published', 'publish'),
            detention_status=status,
            **defaults)

    def make_arrest(self, record, prisoner, comments):
        defaults = {}
        self.translate_date(defaults, 'arrest_', record.get('10040'))

        # Sometimes the cities are provinces, so first check this is the case.
        # They'll have to manaully delete cities which are provinces but they
        # won't lose data like this.
        en_city, fa_city = self.get_city(record.get('11000'))

        province = (core_types.models.Province.objects.all()
                    .filter(name_en=en_city, name_fa=fa_city)
                    .first())

        city = (core_types.models.City.objects.all()
                .filter(name_en=en_city, name_fa=fa_city)
                .first())

        if (en_city or fa_city) and not (province or city):
            LOG.warning('Neither city or province found for (%r, %r)',
                        en_city, fa_city)

        activities = self.activities_from_rec(record, prisoner, comments)
        arrest = prisoners.models.PrisonerArrest.objects.create(
            prisoner=prisoner,
            is_published=prisoner.is_published,
            province=province,
            city=city,
            **defaults
        )

        arrest.charged_with = self.chargedwiths_from_rec(record)
        arrest.domestic_law_violated = self.domestics_from_rec(record)
        arrest.international_law_violated = self.intls_from_rec(record)
        arrest.activity_persecuted_for = activities
        arrest.save()

    def make_sentences(self, record, prisoner, comments):
        # judge. we're getting back lists of strings. Argghh this is annoying.
        # basically the get function just returns what's in wordpress db and
        # that can be anything. The getter function should have been rewritten
        # when this became apparent but i'm almost finished now hence if
        # fa_judge is None: etc.
        try:
            arrest = prisoner.arrests.all()[0]
        except IndexError:
            LOG.debug('%s: Making stub arrest to contain sentence info.',
                      prisoner)
            arrest = prisoners.models.PrisonerArrest.objects.create(
                prisoner=prisoner)

        try:
            en_judge, fa_judge = self.get_multi_values(
                self.all_judges,
                record.get('10340'))
        except KeyError:
            en_judge = fa_judge = None

        if en_judge and fa_judge:
            for en, fa in zip(en_judge, fa_judge):
                judge = judges.models.Judge.objects.get(
                    Q(surname_en=en) | Q(surname_fa=fa))
                prisoners.models.PrisonerSentence.objects.create(
                    arrest=arrest,
                    judge=judge)
        else:
            # this probably isn't a judge but actually a court
            en_court, fa_court = self.get_multi_values(
                self.all_courts,
                record.get('10340'))
            if en_court and fa_court:
                for en, fa in zip(en_court, fa_court):
                    court = judges.models.CourtAndBranch.objects.get(
                        Q(name_en=en) | Q(name_fa=fa))
                    prisoners.models.PrisonerSentence.objects.create(
                        arrest=arrest,
                        court_and_branch=court)

    def make_detentions(self, record, prisoner, comments):
        arrest = prisoner.arrests.all()[0]
        en_prison, fa_prison = self.get_values(self.all_prisons,
                                               record.get('10130'))
        prison = (prisons.models.Prison.objects.all()
                  .filter(name_en=en_prison, name_fa=fa_prison)
                  .first())

        detention = prisoners.models.PrisonerDetention.objects.create(
            arrest=arrest,
            is_published=prisoner.is_published,
            prison=prison)
        detention.treatment = self.treatments_from_rec(record)
        detention.save()
