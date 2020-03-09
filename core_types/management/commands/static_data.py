# -- coding: utf-8 --
SENTENCES = {
    '10401': {'EN': '0 to 1', 'FA': '۰ تا ۱'},
    '10402': {'EN': '1+ to 3', 'FA': '۱+ تا ۳'},
    '10403': {'EN': '3+ to 5', 'FA': '۳+ تا ۵'},
    '10404': {'EN': '5+ to 10', 'FA': '۵+ تا ۱۰'},
    '10405': {'EN': '10+', 'FA': '+۱۰'},
    '10406': {'EN': 'Life imprisonment', 'FA': 'حبس ابد'},
    '10407': {'EN': 'Fine', 'FA': 'جریمه نقدی'},
    '10408': {'EN': 'Exile', 'FA': 'تبعید'},
    '10409': {'EN': 'Flogging', 'FA': 'شلاق'},
    '10410': {'EN': 'Death', 'FA': 'اعدام'},
}


# 'Other' was removed (won't migrate)
# Now there are 2 divisions for Christian (record this fact in profile)
RELIGIONS = {
    '10051': {'EN': 'Ahl-e-Hagh', 'FA': 'اهل حق'},
    '10052': {'EN': 'Bahá`í', 'FA': 'بهائی'},
    '10053': {'EN': 'Christian', 'FA': 'مسیحی‌'},
    '10054': {'EN': 'Dervish', 'FA': 'درویش'},
    '10055': {'EN': 'Jewish', 'FA': 'یهودی'},
    '10056': {'EN': 'Shiaa', 'FA': 'شیعه'},
    '10057': {'EN': 'Sunni', 'FA': 'سنّی'},
    '10058': {'EN': 'Yaresan', 'FA': 'یارسان'},
    '10059': {'EN': 'Zoroastrian', 'FA': 'زرتشتی'},
    '10060': {'EN': 'Other', 'FA': 'دیگر'},
    '10061': {'EN': 'Unknown', 'FA': 'نامشخص'}
}


# Other was removed (won't migrate)
ETHNICITIES = {
    '10071': {'EN': 'Arab', 'FA': 'عرب'},
    '10072': {'EN': 'Azeri', 'FA': 'آذری'},
    '10073': {'EN': 'Baluch', 'FA': 'بلوچ'},
    '10074': {'EN': 'Fars', 'FA': 'فارس'},
    '10075': {'EN': 'Kurd', 'FA': 'کرد'},
    '10076': {'EN': 'Lor', 'FA': 'لٔر'},
    '10077': {'EN': 'Turkmen', 'FA': 'ترکمن'},
    '10078': {'EN': 'Other', 'FA': 'دیگر'},
    '10079': {'EN': 'Unknown', 'FA': 'نامشخص'},
}


# 10312 and 10309 were merged in new schema
CHARGED_WITH = {
    '10301': {'EN': 'Agitating the public consciousness(clause 698)',
              'FA': 'تشویش اذهان عمومی‌(----- ------ ماده‌ ۶۹۸'},
    '10302': {'EN': 'Assembly and collusion against national security (Clause 610)',
              'FA': 'اجتماع و تبانی علیه امنیت ملی‌-- ------- ماده‌ ۶۱۰'},
    '10303': {'EN': 'Disruption of public order (Clause 618)',
              'FA': 'اخلال در نظم  عمومی‌'},
    '10304': {'EN': 'Enmity against God [Moharebeh] (Clauses 183  186 and 187)',
              'FA': 'محاربه -   ماده‌های ۱۸۳، ۱۸۶ و ۱۸۷'},
    '10305': {'EN': 'Espionage (clause 501)',
              'FA': 'جاسوسی ماده‌ ۵۰۱'},
    '10306': {'EN': 'Insulting Islam (clause 513)',
              'FA': 'اهانت به اسلام- ماده‌ ۵۱۳'},
    '10307': {'EN': 'Insulting the President (Clause 609)',
              'FA': 'اهانت به رئیس جمهور- ماده‌ ۶۰۹'},
    '10308': {'EN': 'Insulting the Supreme Leader (Clause 514)',
              'FA': 'اهانت به مقام رهبری- ماده‌ ۵۱۴'},
    '10309': {'EN': 'Relations, collaboration with, or membership in organizations that aim to disrupt national security (Clause 499)',
              'FA': 'عضویت در تشکیلاتی که قصد اخلال امنیت ملی‌ را دارند- ماده‌ ۴۹۹'},
    '10310': {'EN': 'Propaganda against the system (Clause 500)',
              'FA': 'تبلیغات علیه نظام - ماده‌ ۵۰۰'},
    '10311': {'EN': 'Refusing police orders (Clause 607)',
              'FA': 'تمرد از اوامر پلیس - ماده ۶۰۷'},
    '10312': {'EN': 'Relations, collaboration with, or membership in organizations that aim to disrupt national security (Clause 499)',
              'FA': 'وابستگی یا همکاری با تشکیلاتی که قصد اخلال امنیت ملی‌ را دارند - ماده ۴۹۹'},
    '10313': {'EN': 'Founding or leading an organization aimed to disrupt national security (Clause 498)',
              'FA': 'تشکیل یا اداره تشکل غیر قانونی به هدف  بر هم زدن امنیت کشور  - ماده ۴۹۸'},
    '10314': {'EN': 'Other', 'FA': 'Other'},
}


MARITAL_STATUS = {
    '10011': {'EN': 'Single', 'FA': 'مجرّد'},
    '10012': {'EN': 'Married', 'FA': 'متاهل'},
    '10013': {'EN': 'Divorced', 'FA': 'مطلّق/ مطلقه'},
}


# activities prosecuted for
ACTIVITY_PERSECUTED_FOR = {
    '10602': {'EN': 'Human rights defender', 'FA': 'مدافع حقوق بشر'},
    '10603': {'EN': 'Human rights defender: lawyer', 'FA': 'وکیل مدافع حقوق بشر'},
    '10604': {'EN': 'Human rights defender: women rights', 'FA': 'مدافع حقوق بشر-حقوق زنان'},
    '10605': {'EN': 'Human rights defender: ethnic rights', 'FA': 'مدافع حقوق بشر-حقوق قومی'},
    '10606': {'EN': 'Human rights defender: labor rights', 'FA': 'مدافع حقوق بشر-حقوق کارگران'},
    '10607': {'EN': 'Political activist', 'FA': 'فعال سیاسی'},
    '10608': {'EN': 'Journalist or blogger', 'FA': 'خبرنگار یا وبلاگ نویس'},
    '10609': {'EN': 'Religious minority practitioner', 'FA': 'پیرو اقلیت مذهبی‌'},
    '10610': {'EN': 'Civic activist', 'FA': 'فعال مدنی'},
    '10611': {'EN': 'Student activist', 'FA': 'فعال دانشجویی'},
    '10612': {'EN': 'Artist or writer', 'FA': 'هنرمند یا نویسنده'},
}


ACTIVITIES_MAP = {
    '10602': 'Human Rights Defender',
    '10605': 'Human Rights Defender',
    '10606': 'Human Rights Defender',
    '10603': 'Human Rights Defender',
    '10604': "Women's Rights Activist",
    '10611': "Student Activist",
    '10609': 'Religious Minority Practitioner',
    '10607': 'Political Rights Activist',
    '10610': 'Civic Activist',
}


DOMESTIC_LAW_VIOLATED = {
    '10502': {'EN': 'Not presenting a legal warrant at the time of the arrest',
              'FA': 'عدم ارائه حکم قانونی‌ در زمان جلب'},
    '10503': {'EN': 'Not advising the arrestee of the allegations and the reasons for them after the arrest',
              'FA': 'عدم تفهیم اتهام و دلائل بازداشت بعد از جلب'},
    '10504': {'EN': 'Violation of Right to have proper Counsel and legal representation',
              'FA': 'نقض حق داشتن وکیل  و مشاور قانونی‌ ذی‌ صلاحیت'},
    '10505': {'EN': 'Long-term solitary confinement employment of unconventional methods',
              'FA': 'حبس انفرادیِ دراز مدت و اعمال روش‌های غیر متعارف'},
    '10506': {'EN': 'Physical and psychological torture',
              'FA': 'شکنجهٔ بدنی و روانی‌'},
    '10507': {'EN': 'Inability of the detainee to communicate with outside world (e.g. Family members)',
              'FA': 'عدم امکان تماس با جهان خارج، مثلا با خانواده'},
    '10508': {'EN': 'Deprivation of medical services',
              'FA': 'محرومیت از خدمات پزشکی‌'},
    '10509': {'EN': 'Other violations listed in section 8',
              'FA': 'تخلفات دیگرِ مذکور در بخش ۸'},
}

INTL_LAW_VIOLATED = {
    '10531': {'EN': 'Not presenting a legal warrant at the time of the arrest (Article 9 UDHR, Article 9 ICCPR)',
              'FA': 'عدم ارائه حکم قانونی‌ در زمان جلب-ماده ۹ از بیانیه جهانی‌ حقوق بشر---ماده ۹ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی'},
    '10532': {'EN': 'Not advising the individual of the reason for arrest at the time of arrest (Article 9 ICCPR)',
              'FA': 'عدم تفهیم اتهامات و دلائل بازداشت بعد از جلب---ماده ۹ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی'},
    '10533': {'EN': 'Violation of the right to legal counsel (Article 11 UDHR,  Article 14 ICCPR)',
              'FA': 'نقض حق داشتن مشاورقانونی-ماده ۱۱ از بیانیه جهانی‌ حقوق بشر---ماده ۱۴ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی'},
    '10534': {'EN': 'Long-term solitary confinement  employment of unconventional methods (Article 7 ICCPR)',
              'FA': 'حبس انفرادیِ دراز مدت و اعمال روش‌های غیر متعارف---ماده ۷ از عهد نامهٔ بین المللی حقوق مدنی و سیاسی'},
    '10535': {'EN': 'Physical and psychological torture (Article 2 CAT, Article 7 ICCPR, Article 2 UDHR)',
              'FA': 'شکنجهٔ بدنی و روانی‌-- ماده ۷ از عهدنامه بین المللی حقوق مدنی و سیاسی--ماده ۲ از بیانیه جهانی‌ حقوق ---ماده ۲ از کمیته مبارزه با شکنجه'},
    '10536': {'EN': 'Incommunicado detention (Body of Principles)',
              'FA': 'حبس انفرادی بدون امکان تماس با دیگران  -- مجموعه  مبادی و اصول'},
    '10537': {'EN': 'Medical Neglect (Body of Principles)',
              'FA': 'مسامحه در درمان -- مجموعه  مبادی و اصول'},
}


DETENTION_STATUS = {
    '10111': {'EN': 'Yes, details unclear', 'FA': 'بله، جزئیات مبهم است'},
    '10112': {'EN': 'Yes, house arrest', 'FA': 'بله، حبس خانگی'},
    '10113': {'EN': 'Yes, no trial', 'FA': 'بله، بدون دادگاه'},
    '10114': {'EN': 'Yes, convicted by court trial', 'FA': 'بله، با حکم دادگاه'},
    '10115': {'EN': 'Yes, appeal process completed', 'FA': 'بله، با تکمیل فرآیند تجدیدنظر'},
    '10116': {'EN': 'Yes, on furlough', 'FA': 'بله، در مرخصی'},
    '10117': {'EN': 'No, details unclear', 'FA': 'نه، جزئیات مبهم است'},
    '10118': {'EN': 'No: convicted by court trial', 'FA': 'نه: محکوم در دادگاه'},
    '10119': {'EN': 'No, appeal process completed', 'FA': 'نه، فرآیند تجدیدنظر پایان یافته'},
    '10120': {'EN': 'No, suspended sentence', 'FA': 'نه، حکم تعلیقی'},
    '10121': {'EN': 'No, on furlough', 'FA': 'نه، در مرخصی'},
    '10122': {'EN': 'No, released on bail (not sentenced yet)', 'FA': 'نه، آزاد به قید وثيقه (بدون صدور حکم)'},
    '10123': {'EN': 'No, sentence completed', 'FA': 'نه، پایان محکومیت'},
    '10124': {'EN': 'No, exiled', 'FA': 'نه، در تبعید'},
    '10125': {'EN': 'No, executed', 'FA': 'نه، اعدام شده'},
    '10126': {'EN': 'No, passed away', 'FA': 'نه، فوت شده'},
}


PROSECUTION_INFO = {
    '10421': {'EN': 'Multiple arrests', 'FA': 'بازداشت مکرر'},
    '10422': {'EN': 'Multiple sentences', 'FA': 'احکام متعدد'},
    '10423': {'EN': 'Currently without legal representation', 'FA': 'فعلا بدون وکیل مدافع'},
}


TREATMENT_IN_PRISON = {
    '10451': {'EN': 'Solitary confinement', 'FA': 'حبس انفرادی'},
    '10452': {'EN': 'Family visits denied', 'FA': 'محرومیت از ملاقات با خانواده'},
    '10453': {'EN': 'Furlough denied', 'FA': 'محرومیت از مرخصی'},
    '10454': {'EN': 'Access to phone denied', 'FA': 'محرومیت از استفاده از تلفن'},
    '10455': {'EN': 'Access to health-care denied', 'FA': 'محرومیت از خدمات درمانی'},
    '10456': {'EN': 'Torture', 'FA': 'شکنجه'},
    '10457': {'EN': 'National exile', 'FA': 'تبعید درون مرزی'},
    '10458': {'EN': 'Pressure on family', 'FA': 'اعمال فشار بر خانواده'},
    '10459': {'EN': 'Hunger strike', 'FA': 'اعتصاب غذا'},
}
