smallmedia.tilesVisLanguage = (function(){
  /* jshint -W100 */
  var my = {};

  var config = {
    language: 'en'
  };

  my.enToFaTable = {
    // Top menu
    'Verdicts': '​حکم‌ ها',
    'Amputations': 'Amputations',          // AeA | TODO: Needs translation!
    'Sentence (yrs)': '​محکومیت (سال)',     // IPA
    'Sentence (avg)': '​محکومیت (میانگین)', // IPA
    'Death Penalty': '​محکوم به اعدام',
    'Lashes': '​شلاق',
    'Misconduct': '​سوء رفتار',

    'JUDGE SELECTED': '​نام',
    'PRISONERS SENTENCED': '​محکومین زندانی',
    'View Profile': '​مشاهده پروفایل',
    'View All Prisoners': '​مشاهده همه زندانی‌ها',
    'Each icon on the left represents a prisoner. Hover over the key below or the diagram on the left to explore the prisoners sentenced by this judge. Click on the judge image or the ‘x’ to close this box.' : '​هر آیکون در سمت چپ نشان دهنده یک زندانی است. برای بررسی زندانیانی که توسط این قاضی محکوم شده اند با موس روی آیکون آنها بروید. برای بستن این بلوک روی عکس قاضی یا علامت x کلیک کنید.​',

    'UNKNOWN / NOT GUILTY': 'نامعلوم / تبرئه',
    'YEARS SENTENCED': '​سال‌های محکومیت',
    'EXECUTION': '​اعدام',
    'FINE': '​جریمه​',
    'EXILE': '​تبعید',
    'LASHES': '​شلاق‌',
    'LIFE IMPRISONMENT': '​حبس ابد',
    'YEARS SUSPENDED': '​سال‌های معلق​',

    'Unknown date of birth': '​تاریخ تولد نامعلوم',
    'Sentence': '​حکم',
    'years': '​سال',
    'months': '​ماه',
    'lashes': '​شلاق​',
    'Executed': '​اعدام شده',
    'Exiled': '​تبعید شده',
    'Life': '​حبس ابد​',
    'fine': '​جریمه',
    'Unknown / not guilty': 'نامعلوم / تبرئه',
    'Suspended': '​معلق',
    'Execution': '​ااعدام'
  };

  my.enFa = function(text) {
    if(config.language === 'en')
      return text;

    if(!_.has(my.enToFaTable, text))
      return text;

    return my.enToFaTable[text];
  };


  my.setLanguage = function(lang) {
    config.language = lang;
  };

  my.getLanguage = function() {
    return config.language;
  };

  return my;
}());
