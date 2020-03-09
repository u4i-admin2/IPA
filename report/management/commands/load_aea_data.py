# coding: utf-8
#
import csv
from django.core.management.base import BaseCommand
from django.db import transaction
from report.models import Report, ReportSentence, ReportDetention, ReportSentenceBehaviour
from judges.models import Judge, JudicialPosition, BehaviourType
from prisons.models import Prison
from core_types.models import City, Province, Ethnicity


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('type', nargs='+', type=str)
        parser.add_argument('filename', nargs='+', type=str)

    def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
        csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
        for row in csv_reader:
            yield [unicode(cell, 'utf-8') for cell in row]

    @transaction.atomic
    def add_report(self, row):
        human_right_map = {
            u'صدور حکم اعدام': 1,
            u'صدور حکم شلاق': 2,
            u'صدور حکم قطع عضو': 3
        }

        domestic_law_map = {
            u'حبس انفرادیِ دراز مدت و اعمال روش‌های غیر متعارف': 1,
            u'محرومیت از خدمات پزشکی‌': 2,
            u'نقض حق داشتن وکیل  و مشاور قانونی‌ ذی‌ صلاحیت': 3,
            u'عدم امکان تماس با جهان خارج، مثلا با خانواده': 4,
            u'عدم تفهیم اتهام و دلائل بازداشت بعد از جلب': 5,
            u'شکنجهٔ بدنی و روانی‌': 6,
            u'عدم ارائه حکم قانونی‌ در زمان جلب': 7
        }

        intl_law_map = {
            u'حبس انفرادیِ دراز مدت و اعمال روش‌های غیر متعارف---ماده ۷ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی': 1,
            u'عدم ارائه حکم قانونی‌ در زمان جلب-ماده ۹ از بیانیه جهانی‌ حقوق بشر---ماده ۹ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی': 2,
            u'حبس انفرادی بدون امکان تماس با دیگران  -- مجموعه  مبادی و اصول': 3,
            u'مسامحه در درمان -- مجموعه  مبادی و اصول': 4,
            u'نقض حق داشتن مشاورقانونی-ماده ۱۱ از بیانیه جهانی‌ حقوق بشر---ماده ۱۴ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی': 5,
            u'شکنجهٔ بدنی و روانی‌-- ماده ۷ از عهدنامه بین المللی حقوق مدنی و سیاسی--ماده ۲ از بیانیه جهانی‌ حقوق ---ماده ۲ از کمیته مبارزه با شکنجه': 6,
            u'عدم تفهیم اتهامات و دلائل بازداشت بعد از جلب---ماده ۹ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی': 7,
        }

        judge_violations_map = {
            u'عدم رعایت شأن و کرامت انسانی متهم در دادگاه': 1,
            u'عدم دسترسی متهم به وکیل مدافع': 2,
            u'ضرب و شتم متهم در دادگاه': 3,
            u'شکنجه و بدرفتاری فیزیکی با زندانی': 4,
            u'حبس انفرادی': 5,
            u'جلوگیری از ملاقات متهم با خانواده': 6,
            u'تبعید به زندان خارج از شهر محل سکونت': 7,
            u'بدرفتاری و تحت فشار قراردادن خانواده متهم': 8
        }

        newr = Report.objects.create(
            is_published=True,
            abstract_text_fa=row['abstract_text_fa'].decode('utf-8'),
            victim_count=row['victim_count'],
            partial_date=row['date_en'])

        if row['domestic_law_violated_1']:
            newr.domestic_law_violated.add(
                domestic_law_map[row['domestic_law_violated_1'].decode('utf-8')])
        if row['domestic_law_violated_2']:
            newr.domestic_law_violated.add(
                domestic_law_map[row['domestic_law_violated_2'].decode('utf-8')])

        if row['international_law_violated_1']:
            newr.international_law_violated.add(
                intl_law_map[row['international_law_violated_1'].decode('utf-8')])
        if row['international_law_violated_2']:
            newr.international_law_violated.add(
                intl_law_map[row['international_law_violated_2'].decode('utf-8')])

        if row['human_right_violated_1']:
            newr.human_right_violated.add(
                human_right_map[row['human_right_violated_1'].decode('utf-8')])
        if row['human_right_violated_2']:
            newr.human_right_violated.add(
                human_right_map[row['human_right_violated_2'].decode('utf-8')])

        if row['ipa.public.ipa_judge_behaviour_type']:
            behaviour = BehaviourType.objects.get(
                pk=judge_violations_map[
                    row['ipa.public.ipa_judge_behaviour_type'].decode('utf-8')])

        if row['judges_1']:
            sentence = ReportSentence.objects.create(
                is_published=True,
                execution=(row['execution'] == 'TRUE'),
                flogging=(row['flogging'] == 'TRUE'),
                amputation=(row['amputation'] == 'TRUE'),
                judge=Judge.objects.filter(
                    surname_fa=row['judges_1']).first(),
                report=newr)
            if row['ipa.public.ipa_judge_behaviour_type']:
                ReportSentenceBehaviour.objects.create(
                    is_published=True,
                    judge_behaviour=behaviour,
                    report_sentence=sentence)

        if row['judges_2']:
            sentence = ReportSentence.objects.create(
                is_published=True,
                execution=(row['execution'] == 'TRUE'),
                flogging=(row['flogging'] == 'TRUE'),
                amputation=(row['amputation'] == 'TRUE'),
                judge=Judge.objects.filter(
                    surname_fa=row['judges_2']).first(),
                report=newr)
            if row['ipa.public.ipa_judge_behaviour_type']:
                ReportSentenceBehaviour.objects.create(
                    is_published=True,
                    judge_behaviour=behaviour,
                    report_sentence=sentence)

        if row['judges_3']:
            sentence = ReportSentence.objects.create(
                is_published=True,
                execution=(row['execution'] == 'TRUE'),
                flogging=(row['flogging'] == 'TRUE'),
                amputation=(row['amputation'] == 'TRUE'),
                judge=Judge.objects.filter(
                    surname_fa=row['judges_3']).first(),
                report=newr)
            if row['ipa.public.ipa_judge_behaviour_type']:
                ReportSentenceBehaviour.objects.create(
                    is_published=True,
                    judge_behaviour=behaviour,
                    report_sentence=sentence)

        if row['judges_4']:
            sentence = ReportSentence.objects.create(
                is_published=True,
                execution=(row['execution'] == 'TRUE'),
                flogging=(row['flogging'] == 'TRUE'),
                amputation=(row['amputation'] == 'TRUE'),
                judge=Judge.objects.filter(
                    surname_fa=row['judges_4']).first(),
                report=newr)
            if row['ipa.public.ipa_judge_behaviour_type']:
                ReportSentenceBehaviour.objects.create(
                    is_published=True,
                    judge_behaviour=behaviour,
                    report_sentence=sentence)

        if row['judges_5']:
            sentence = ReportSentence.objects.create(
                is_published=True,
                execution=(row['execution'] == 'TRUE'),
                flogging=(row['flogging'] == 'TRUE'),
                amputation=(row['amputation'] == 'TRUE'),
                judge=Judge.objects.filter(
                    surname_fa=row['judges_5']).first(),
                report=newr)
            if row['ipa.public.ipa_judge_behaviour_type']:
                ReportSentenceBehaviour.objects.create(
                    is_published=True,
                    judge_behaviour=behaviour,
                    report_sentence=sentence)

        if row['judges_6']:
            sentence = ReportSentence.objects.create(
                is_published=True,
                execution=(row['execution'] == 'TRUE'),
                flogging=(row['flogging'] == 'TRUE'),
                amputation=(row['amputation'] == 'TRUE'),
                judge=Judge.objects.filter(
                    surname_fa=row['judges_6']).first(),
                report=newr)
            if row['ipa.public.ipa_judge_behaviour_type']:
                ReportSentenceBehaviour.objects.create(
                    is_published=True,
                    judge_behaviour=behaviour,
                    report_sentence=sentence)

        if row['prison']:
            year_fa = None
            month_fa = None
            day_fa = None
            year = None
            month = None
            day = None
            rowplit = row['date_fa'].split('/')
            if len(rowplit) == 1:
                year_fa = rowplit[0]
            else:
                year_fa = rowplit[0]
                month_fa = rowplit[1]
                day_fa = rowplit[2]
            rowplit = row['date_en'].split('/')
            if len(rowplit) == 1:
                year = rowplit[0]
            else:
                year = rowplit[0]
                month = rowplit[1]
                day = rowplit[2]

            ReportDetention.objects.create(
                is_published=True,
                report=newr,
                prison=Prison.objects.get(
                    name_fa=row['prison']),
                detention_year=year,
                detention_month=month,
                detention_day=day,
                detention_year_fa=year_fa,
                detention_month_fa=month_fa,
                detention_day_fa=day_fa)

    def handle(self, **options):

        filename = options['filename'][0]

        with open(filename) as input:
            rows = csv.DictReader(input, delimiter=',')
            if options['type'][0].lower() == 'judge':
                for row in rows:
                    judge = Judge.objects.filter(
                        surname_fa=row['surname_fa'],
                        forename_fa=row['forename_fa'])

                    if len(judge) == 1:
                        continue
                    elif len(judge) > 1:
                        print('\t\tFOUND more than one {} {}'.format(row['surname_fa'], row['forename_fa']))
                    else:
                        print('\t\tNOT FOUND {}'.format(row['surname_fa']))
                        newj = Judge.objects.create(
                            is_published=True,
                            forename_en=row['forename_en'],
                            forename_fa=row['forename_fa'].decode('utf-8'),
                            surname_en=row['surname_en'],
                            surname_fa=row['surname_fa'].decode('utf-8'),
                            dob_year=row['dob_year'] if row['dob_year'] else None,
                            dob_month=row['dob_month'] if row['dob_month'] else None,
                            dob_day=row['dob_day'] if row['dob_day'] else None,
                            dob_year_fa=row['dob_year_fa'] if row['dob_year_fa'] else None,
                            dob_month_fa=row['dob_month_fa'] if row['dob_month_fa'] else None,
                            dob_day_fa=row['dob_day_fa'] if row['dob_day_fa'] else None,
                            dob_is_estimate=(row['dob_is_estimate'] == 'true') if row['dob_is_estimate'] else None,
                            birth_city=City.objects.get(id=row['birth_city_id']) if row['birth_city_id'] else None,
                            birth_province=Province.objects.get(id=row['birth_province_id']) if row['birth_province_id'] else None,
                            ethnicity=Ethnicity.objects.get(id=row['ethnicity_id']) if row['ethnicity_id'] else None,
                            is_cleric=(row['is_cleric'] == 'true') if row['is_cleric'] else None,
                            judge_type=row['judge_type'],
                            judicial_position=JudicialPosition.objects.get(id=row['judge_judicial_position_id']) if row['judge_judicial_position_id'] else None,
                            court_and_branch=None,
                            biography_en=row['biography_en'].decode('utf-8'),
                            biography_fa=row['biography_fa'].decode('utf-8'),
                            mistreatments_count=0,
                            aea_mistreatments_count=0)
                        print('CREATED New Judge {} by id {}'.format(row['surname_fa'], str(newj.id)))

            if options['type'][0].lower() == 'prison':
                for row in rows:
                    prison = Prison.objects.filter(
                        name_fa=row['name_fa'])
                    if len(prison) == 1:
                        continue
                    elif len(prison) > 1:
                        print('\t\tFOUND more than one {}'.format(row['name_fa']))
                    else:
                        print('\t\tNOT FOUND {}'.format(row['name_fa']))
                        newp = Prison.objects.create(
                            is_published=True,
                            name_fa=row['name_fa'].decode('utf-8'),
                            name_en=row['name_en'],
                            address_en=row['address_en'],
                            address_fa=row['address_fa'].decode('utf-8'),
                            dean_name_en=row['dean_name_en'],
                            dean_name_fa=row['dean_name_fa'].decode('utf-8'),
                            dean_email=row['dean_email'],
                            dean_phone=row['dean_phone'],
                            capacity=row['capacity'] if row['capacity'] else None,
                            capacity_is_estimate=(row['capacity_is_estimate'] == 'TRUE'),
                            latitude=float(row['latitude']) if row['latitude'] else None,
                            longitude=float(row['longitude']) if row['longitude'] else None,
                            opened_year=row['opened_year'] if row['opened_year'] else None,
                            opened_month=row['opened_month'] if row['opened_month'] else None,
                            opened_day=row['opened_day'] if row['opened_day'] else None,
                            opened_year_fa=row['opened_year_fa'] if row['opened_year_fa'] else None,
                            opened_month_fa=row['opened_month_fa'] if row['opened_month_fa'] else None,
                            opened_day_fa=row['opened_day_fa'] if row['opened_day_fa'] else None,
                            administered_by=row['administered_by'],
                            physical_structure_en=row['physical_structure_en'],
                            physical_structure_fa=row['physical_structure_fa'].decode('utf-8'),
                            size_and_density_en=row['size_and_density_en'],
                            size_and_density_fa=row['size_and_density_fa'].decode('utf-8'))
                        print('CREATED New Prison {} by id {}'.format(row['name_fa'], str(newp.id)))

            if options['type'][0].lower() == 'report':
                for row in rows:
                    self.add_report(row)
