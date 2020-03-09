# -- coding: utf-8 --
import unicodecsv
import os

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import IntegrityError

import judges.models
from prisons.models import (PrisonFacility,
                            Prison)

from prisoners.models import (RelationshipType,
                              ActivityPersecutedFor,
                              ChargedWith,
                              DomesticLawViolated,
                              InternationalLawViolated,
                              DetentionStatus,
                              PrisonTreatment)

from .. .models import (Religion, Ethnicity, City, Province)


class Command(BaseCommand):

    # Judicial positions
    judicial_positions = {
        'Prosecutor': 'دادستان',
        'Court assistant': 'معاون دادسرا',
        'Assistant Prosecutor': 'دادیار',
        'Assistant Prosecutor - Research': 'دادیار تحقیق؛',
        'Assistant Prosecutor - Assessment': 'دادیار اظهارنظر؛',
        'Assistant Prosecutor - Execution of convictions': 'دادیار اجرای احكام؛',
        'Assistant Prosecutor - Prison Supervision': 'دادیار ناظر زندان؛',
        'Prosecutor representative in court': 'دادیار نماینده دادستان در دادگاه.'
    }

    religions = {
        'Ahl-e-Hagh': 'اهل حق',
        u'Bahá`í': 'بهائی',
        'Christian (Armenian, Other Orthodox)': 'مسیحی ارمنی یا ارتدوکس',
        'Christian (Evangelical, Convert)': 'مسیحی پروتستان یا نوکیش',
        'Dervish': 'درویش',
        'Jewish': 'یهودی',
        'Shiaa': 'شیعه',
        'Sunni': 'سنّی',
        'Yaresan': 'یارسان',
        'Zoroastrian': 'زرتشتی',
        'Unknown': 'نامشخص'
    }

    ethnicities = {
        'Arab': 'عرب',
        'Azeri': 'آذری',
        'Baluch': 'بلوچ',
        'Fars': 'فارس',
        'Kurd': 'کرد',
        'Lor': 'لٔر',
        'Turkmen': 'ترکمن',
        'Unknown': 'نامشخص'
    }

    relationship_type = {
        'Parent of': 'Parent of',
        'Child of': 'Child of',
        'Sibling': 'Sibling',
        'Spouse': 'Spouse',
        'Extended Family': 'Extended Family',
    }

    activities = {
        "Children's Rights Activist": 'فعال دفاع از حقوق کودکان',  # new
        'Educational Rights Activist': 'فعال دفاع از حق تحصیل',  # new
        'Religious Minority Rights Activist': 'فعال دفاع از حقوق اقلیتهای مذهبی',  # new
        'Artist': 'هنرمند',   # new derived from 10612
        'Writer': 'نویسنده',  # new derived from 10612
        'Blogger': 'بلاگر',   # new derived from 10608
        'Journalist': 'روزنامه‌نگار',  # new derived from 10608
        'Civic Activist': 'فعال مدنی',  # original: 10610
        'Political Rights Activist': 'فعال سیاسی',  # original: 10607
        'Religious Minority Practitioner': 'فعال دفاع از حقوق اقلیتهای قومی',  # original: 10609
        'Student Activist': 'فعال دانشجوئی',  # original: 10611
        "Women's Rights Activist": 'فعال دفاع از حقوق زنان',  # original: 10604
        'Human Rights Defender': 'فعال حقوق بشر',  # combination 10602;10605;10606
    }

    charges = {
        'Agitating the public consciousness(clause 698)': 'تشویش اذهان عمومی‌(----- ------ ماده‌ ۶۹۸',
        'Assembly and collusion against national security (Clause 610)': 'اجتماع و تبانی علیه امنیت ملی‌-- ------- ماده‌ ۶۱۰',
        'Disruption of public order (Clause 618)': 'اخلال در نظم  عمومی‌',
        'Enmity against God [Moharebeh] (Clauses 183  186 and 187)': 'محاربه -   ماده‌های ۱۸۳، ۱۸۶ و ۱۸۷',
        'Espionage (clause 501)': 'جاسوسی ماده‌ ۵۰۱',
        'Insulting Islam (clause 513)': 'اهانت به اسلام- ماده‌ ۵۱۳',
        'Insulting the President (Clause 609)': 'اهانت به رئیس جمهور- ماده‌ ۶۰۹',
        'Insulting the Supreme Leader (Clause 514)': 'اهانت به مقام رهبری- ماده‌ ۵۱۴',
        'Propaganda against the system (Clause 500)': 'تبلیغات علیه نظام - ماده‌ ۵۰۰',
        'Refusing police orders (Clause 607)': 'تمرد از اوامر پلیس - ماده ۶۰۷',
        'Relations, collaboration with, or membership in organizations that aim to disrupt national security (Clause 499)': 'عضویت در سازمانها برهم زننده امنیت  ( ماده ۴۹۹)',  # 10312 and 10309 were merged into this one
        'Founding or leading an organization aimed to disrupt national security (Clause 498)': 'تشکیل یا اداره تشکل غیر قانونی به هدف  بر هم زدن امنیت کشور  - ماده ۴۹۸',
    }

    domestics = {
        'Not presenting a legal warrant at the time of the arrest': 'عدم ارائه حکم قانونی‌ در زمان جلب',
        'Not advising the arrestee of the allegations and the reasons for them after the arrest': 'عدم تفهیم اتهام و دلائل بازداشت بعد از جلب',
        'Violation of Right to have proper Counsel and legal representation': 'نقض حق داشتن وکیل  و مشاور قانونی‌ ذی‌ صلاحیت',
        'Long-term solitary confinement employment of unconventional methods': 'حبس انفرادیِ دراز مدت و اعمال روش‌های غیر متعارف',
        'Physical and psychological torture': 'شکنجهٔ بدنی و روانی‌',
        'Inability of the detainee to communicate with outside world (e.g. Family members)': 'عدم امکان تماس با جهان خارج، مثلا با خانواده',
        'Deprivation of medical services': 'محرومیت از خدمات پزشکی‌',
        'Other violations listed in section 8': 'تخلفات دیگرِ مذکور در بخش ۸',
    }

    internationals = {
        'Not presenting a legal warrant at the time of the arrest (Article 9 UDHR, Article 9 ICCPR)': 'عدم ارائه حکم قانونی‌ در زمان جلب-ماده ۹ از بیانیه جهانی‌ حقوق بشر---ماده ۹ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی',
        'Not advising the individual of the reason for arrest at the time of arrest (Article 9 ICCPR)': 'عدم تفهیم اتهامات و دلائل بازداشت بعد از جلب---ماده ۹ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی',
        'Violation of the right to legal counsel (Article 11 UDHR,  Article 14 ICCPR)': 'نقض حق داشتن مشاورقانونی-ماده ۱۱ از بیانیه جهانی‌ حقوق بشر---ماده ۱۴ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی',
        'Long-term solitary confinement  employment of unconventional methods (Article 7 ICCPR)': 'حبس انفرادیِ دراز مدت و اعمال روش‌های غیر متعارف---ماده ۷ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی',
        'Physical and psychological torture (Article 2 CAT, Article 7 ICCPR, Article 2 UDHR)': 'شکنجهٔ بدنی و روانی‌-- ماده ۷ از عهدنامه بین المللی حقوق مدنی و سیاسی--ماده ۲ از بیانیه جهانی‌ حقوق ---ماده ۲ از کمیته مبارزه با شکنجه',
        'Incommunicado detention (Body of Principles)': 'حبس انفرادی بدون امکان تماس با دیگران  -- مجموعه  مبادی و اصول',
        'Medical Neglect (Body of Principles)': 'مسامحه در درمان -- مجموعه  مبادی و اصول',
    }

    detention_status = {
        'Yes, details unclear': 'بله، جزئیات مبهم است',
        'Yes, house arrest': 'بله، حبس خانگی',
        'Yes, no trial': 'بله، بدون دادگاه',
        'Yes, convicted by court trial': 'بله، با حکم دادگاه',
        'Yes, appeal process completed': 'بله، با تکمیل فرآیند تجدیدنظر',
        'Yes, on furlough': 'بله، در مرخصی',
        'No, details unclear': 'نه، جزئیات مبهم است',
        'No: convicted by court trial': 'نه: محکوم در دادگاه',
        'No, appeal process completed': 'نه، فرآیند تجدیدنظر پایان یافته',
        'No, suspended sentence': 'نه، حکم تعلیقی',
        'No, on furlough': 'نه، در مرخصی',
        'No, released on bail (not sentenced yet)': 'نه، آزاد به قید وثيقه (بدون صدور حکم)',
        'No, sentence completed': 'نه، پایان محکومیت',
        'No, exiled': 'نه، در تبعید',
        'No, executed': 'نه، اعدام شده',
        'No, passed away': 'نه، فوت شده',
    }

    prison_treatment = {
        'Solitary confinement': 'حبس انفرادی',
        'Family visits denied': 'محرومیت از ملاقات با خانواده',
        'Furlough denied': 'محرومیت از مرخصی',
        'Access to phone denied': 'محرومیت از استفاده از تلفن',
        'Access to health-care denied': 'محرومیت از خدمات درمانی',
        'Torture': 'شکنجه',
        'National exile': 'تبعید درون مرزی',
        'Pressure on family': 'اعمال فشار بر خانواده',
        'Hunger strike': 'اعتصاب غذا',
    }

    prison_administrators = {
        'Ministry of Information': 'Ministry of Information',
        'Police': 'Police',
        'IRGC': 'IRGC',
        'Prisons Division of the Judiciary': 'Prisons Division of the Judiciary',
    }

    prison_facilities = {
        'Place Holder': 'Place Holder',
    }

    help = 'python manage.py core_types - installs all the core types'

    def handle(self, *args, **options):
        print('Creating core types'.ljust(100, '='))

        print('\nCreating judicial positions'.ljust(50, '='))
        for k, v in self.judicial_positions.iteritems():
            obj, created = judges.models.JudicialPosition.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        print('\nCreating religions'.ljust(50, '='))
        for k, v in self.religions.iteritems():
            obj, created = Religion.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        print('\nCreating ethnicities'.ljust(50, '='))
        for k, v in self.ethnicities.iteritems():
            obj, created = Ethnicity.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        print('\nCreating relationships'.ljust(50, '='))
        for k, v in self.relationship_type.iteritems():
            obj, created = RelationshipType.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        print('\nCreating persecuted activities'.ljust(50, '='))
        for k, v in self.activities.iteritems():
            obj, created = ActivityPersecutedFor.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        print('\nCreating charges'.ljust(50, '='))
        for k, v in self.charges.iteritems():
            obj, created = ChargedWith.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        print('\nCreating domestic violations'.ljust(50, '='))
        for k, v in self.domestics.iteritems():
            obj, created = DomesticLawViolated.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        print('\nCreating international violations'.ljust(50, '='))
        for k, v in self.internationals.iteritems():
            obj, created = InternationalLawViolated.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        print('\nCreating detention status'.ljust(50, '='))
        for k, v in self.detention_status.iteritems():
            obj, created = DetentionStatus.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        """
        print('\nCreating prison administrators'.ljust(50, '='))
        for k, v in self.prison_administrators.iteritems():
            obj, created = PrisonAdministrator.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))
        """

        print('\nCreating prison facilities'.ljust(50, '='))
        for k, v in self.prison_facilities.iteritems():
            obj, created = PrisonFacility.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        print('\nCreating prison treatments'.ljust(50, '='))
        for k, v in self.prison_treatment.iteritems():
            obj, created = PrisonTreatment.objects.get_or_create(
                name_en=k, name_fa=v, is_published=True)
            print('Created: %s: %s' % (created, obj))

        cursor = connections['wp'].cursor()

        # create the cities
        cities = {}
        print('\nCreating cities'.ljust(50, '='))
        cursor.execute("SELECT uid, en_lang, fa_lang\
          FROM wp_ppd_repository\
          WHERE uid BETWEEN %s AND %s", [11001, 11101])
        for row in cursor.fetchall():
            if row[1] == '' and row[2] == '':
                continue
            cities[row[1]] = row[2]

        for k, v in cities.iteritems():
            try:
                obj, created = City.objects.get_or_create(
                    name_en=k, name_fa=v, is_published=True)
                print('Created: %s: %s' % (created, obj))
            except:
                print('Failed to create: %s: %s' % (created, obj))

        # now we gonna load the provinces in
        print('\nCreating provinces, adding more cities, linking cities to provinces'.ljust(50, '='))
        """
        row[0] = Province EN
        row[1] = Province FA
        row[2] = City EN
        row[3] = City FA
        """
        this_dir = os.path.dirname(os.path.realpath(__file__))
        csv_path = os.path.join(this_dir, 'provinces_and_cities.csv')

        with open(csv_path, 'r') as csvfile:
            csv_reader = unicodecsv.reader(csvfile)

            csv_reader.next()  # Skip header...
            for row in csv_reader:
                prov_obj, prov_created = Province.objects.get_or_create(
                    name_en=row[0], name_fa=row[1])
                print('Created: %s: %s' % (prov_created, prov_obj))

                try:
                    city_obj, city_created = City.objects.get_or_create(
                        name_en=row[2], name_fa=row[3],
                        defaults={
                            'province': prov_obj,
                            'located_in_iran': True,
                        }
                    )
                except IntegrityError:
                    """
                    In this case, the import city is slightly different to a city we already have
                    """
                    city_obj, city_created = City.objects.get_or_create(
                        name_en=row[2],
                        defaults={
                            'province': prov_obj,
                            'located_in_iran': True,
                            'is_published': True,
                        }
                    )

                if city_created:
                    print('Created: %s' % (city_obj))
                else:
                    print('Updated: %s' % (city_obj))

        # now do the prisons
        # First prisons - let's build a dict of them
        prisons = {}
        print('\nCreating prisons'.ljust(50, '='))
        cursor.execute("SELECT uid, en_lang, fa_lang\
          FROM wp_ppd_repository\
          WHERE uid BETWEEN %s AND %s", [15001, 15076])

        for row in cursor.fetchall():
            if row[1] == '' and row[2] == '':
                continue
            prisons[row[1]] = row[2]

        for k, v in prisons.iteritems():
            try:
                obj, created = Prison.objects.get_or_create(
                    name_en=k, name_fa=v, is_published=True)
                print('Created: %s: %s' % (created, obj))
            except:
                print('Failed to create: %s: %s' % (created, obj))

        # Now judges, range -> 10341-10342 and 13001-13095?!
        # LOL! Let's build a dict of them too
        print('\nCreating judges'.ljust(50, '='))
        cursor.execute("SELECT uid, en_lang, fa_lang\
          FROM wp_ppd_repository\
          WHERE uid BETWEEN %s AND %s OR uid BETWEEN %s AND %s", [10341, 10390, 13001, 13095])

        for row in cursor.fetchall():
            # We want Judge name EN, judge name FA, jurisdiction EN, jurisdiction FA
            # We get back a tuple with 3 strings, from that we rip everything between ""
            # What we get is judge name and judge jurisdiction
            en_list = row[1].split('"')
            fa_list = row[2].split('"')

            # First create the court and branch
            if en_list[3] != '' and fa_list[3] != '':

                court_created = False

                try:
                    court_obj, court_created = judges.models.CourtAndBranch.objects.get_or_create(
                        name_en=en_list[3], name_fa=fa_list[3],
                        is_published=True)
                    print('Created court: %s: %s' % (court_created, court_obj))
                except:
                    print('Failed to create Court: %s: %s' % (court_created, court_obj))

            if en_list[1] != '' and fa_list[1] != '':

                try:
                    if court_created:
                        obj, created = judges.models.Judge.objects.update_or_create(
                            surname_en=en_list[1], surname_fa=fa_list[1],
                            defaults={'court_and_branch': court_obj})
                        print('Created judge: %s: %s' % (created, obj))
                    else:
                        obj, created = judges.models.Judge.objects.get_or_create(
                            surname_en=en_list[1], surname_fa=fa_list[1],
                            is_published=True)
                        print('Created judge: %s: %s' % (created, obj))
                except:
                    print('Failed to create Judge: %s: %s' % (created, obj))
