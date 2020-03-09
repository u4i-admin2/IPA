var judgeTags = [
    "Court And Branch: Name",
    "File Evidence: Data",
    "File Evidence: Description",
    "File Evidence: Thumbnail",
    "Judge: Biography",
    "Judge: Birth Year (Persian)",
    "Judge: Court and Branch",
    "Judge: Ethnicity",
    "Judge: Is Cleric?",
    "Judge: Judge Type",
    "Judge: Judge Type",
    "Judge: Picture",
    "Judge: Surname",
    "Judicial Position: Name",
    "Position: Court and Branch",
    "Position: Judge Type",
    "Position: Term Ended Year (Persian)",
    "Position: Term Started Year (Persian)",
    "Quote Evidence: Quote",
    "Quote Evidence: Source",
    "Sentence Type: Finality",
    "Timeline Event: Description",
    "Timeline Event: Persian Year Of Event",
    "Timeline Event: Year Of Event",
    "Type of Judicial Behaviour: Name"
]

var prisonerTags = [
    "Affiliated Organization: Name",
    "Arrest: Activity Persecuted For",
    "Arrest: Arrest Year (Persian)",
    "Arrest: Province of arrest",
    "Detention Status: Prison... currently in detention",
    "Detention: Detention Year (Persian)",
    "Detention: Prison",
    "Domestic Law Violated: Name",
    "File Evidence: Data",
    "File Evidence: Description",
    "File Evidence: File Name",
    "File Evidence: Thumbnail",
    "International Law Violated: Name",
    "Persecuted Activity: Name",
    "Prisoner: Birth Year (Persian)",
    "Prisoner: Detention Year (Persian)",
    "Prisoner: Ethnicity",
    "Prisoner: Needs attention",
    "Prisoner: Prisoner Picture",
    "Prisoner: Religion",
    "Prisoner: Surname",
    "Quote Evidence: Quote",
    "Quote Evidence: Source",
    "Relationship Type: Name",
    "Relationship: Alleged or confirmed?",
    "Relationship: Surname",
    "Relationship: Type",
    "Sentence Judicial Behavi...escription of Behaviour",
    "Sentence Judicial Behaviour: Type",
    "Sentence: Court",
    "Sentence: Death Penalty",
    "Sentence: Fine (Rials)",
    "Sentence: Judge",
    "Sentence: Number Of Lashes",
    "Sentence: Sentence Months",
    "Sentence: Sentence Years",
    "Sentence: Social Deprivation",
    "Timeline Event: Description",
    "Timeline Event: Persian Year Of Event"
]

var prisonTags = [
    "File Evidence: Data",
    "File Evidence: Description",
    "File Evidence: Thumbnail",
    "Prison Facility: Name",
    "Prison: Address",
    "Prison: Administered By",
    "Prison: Bio",
    "Prison: Capacity",
    "Prison: Day Of Opening",
    "Prison: Dean E-mail",
    "Prison: Dean Name",
    "Prison: Dean Telephone",
    "Prison: Estimated Capacity",
    "Prison: Latitude",
    "Prison: Medicine And Nutrition",
    "Prison: Persian Year Of Opening",
    "Prison: Physical Structure",
    "Prison: Size And Density",
    "Prison: Year Of Opening",
    "Quote Evidence: Quote",
    "Quote Evidence: Source",
    "Timeline Event: Persian Year Of Event"
]



var detentionStatus = [{
    text: '1',
    value: 1
}, {
    text: '2',
    value: 2
}, {
    text: '3',
    value: 3
}]

var gender = [{
    text: 'Female',
    value: 'F'
}, {
    text: 'Male',
    value: 'M'
}]

var is_detained = [{
    text: 'Detained',
    value: 0
}, {
    text: 'Released',
    value: 1
}]
var has_comments = [{
    text: 'Has Conflicts & Consideration',
    value: 1
}, {
    text: 'No Conflicts & Consideration',
    value: 0
}]

var religion = [{
    text: 'Sunni',
    value: 'Sunni'
}, {
    text: 'Yaresan',
    value: 'Yaresan'
}, {
    text: 'Christian (Evangelical, Convert)',
    value: 'Christian (Evangelical, Convert)'
}, {
    text: 'Bahá`í',
    value: 'Bahá`í'
}, {
    text: 'Ahl-e-Hagh',
    value: 'Ahl-e-Hagh'
}, {
    text: 'Shiaa',
    value: 'Shiaa'
}, {
    text: 'Jewish',
    value: 'Jewish'
}, {
    text: 'Christian (Armenian, Other Orthodox)',
    value: 'Christian (Armenian, Other Orthodox)'
}, {
    text: 'Unknown',
    value: 'Unknown'
}, {
    text: 'Dervish',
    value: 'Dervish'
}, {
    text: 'Zoroastrian',
    value: 'Zoroastrian'
}]

var ethnicity = [{
    text: 'Turkmen',
    value: 'Turkmen'
}, {
    text: 'Kurd',
    value: 'Kurd'
}, {
    text: 'Unknown',
    value: 'Unknown'
}, {
    text: 'Fars',
    value: 'Fars'
}, {
    text: 'Baluch',
    value: 'Baluch'
}, {
    text: 'Azeri',
    value: 'Azeri'
}, {
    text: 'Lor',
    value: 'Lor'
}, {
    text: 'Arab',
    value: 'Arab'
}]






var days = [{
    text: 'Unknown',
    value: '1'
}, {
    text: '01',
    value: '1'
}, {
    text: '02',
    value: '2'
}, {
    text: '03',
    value: '3'
}, {
    text: '04',
    value: '4'
}, {
    text: '05',
    value: '5'
}, {
    text: '06',
    value: '6'
}, {
    text: '07',
    value: '7'
}, {
    text: '08',
    value: '8'
}, {
    text: '09',
    value: '9'
}, {
    text: '10',
    value: '10'
}, {
    text: '11',
    value: '11'
}, {
    text: '12',
    value: '12'
}, {
    text: '13',
    value: '13'
}, {
    text: '14',
    value: '14'
}, {
    text: '15',
    value: '15'
}, {
    text: '16',
    value: '16'
}, {
    text: '17',
    value: '17'
}, {
    text: '18',
    value: '18'
}, {
    text: '19',
    value: '19'
}, {
    text: '20',
    value: '20'
}, {
    text: '21',
    value: '21'
}, {
    text: '22',
    value: '22'
}, {
    text: '23',
    value: '23'
}, {
    text: '24',
    value: '24'
}, {
    text: '25',
    value: '25'
}, {
    text: '26',
    value: '26'
}, {
    text: '27',
    value: '27'
}, {
    text: '28',
    value: '28'
}, {
    text: '29',
    value: '29'
}, {
    text: '30',
    value: '30'
}, {
    text: '31',
    value: '31'
}];


var months = [{
    text: 'Unknown',
    value: 'Unknown'
}, {
    text: 'January',
    value: '1'
}, {
    text: 'February',
    value: '2'
}, {
    text: 'March',
    value: '3'
}, {
    text: 'April',
    value: '4'
}, {
    text: 'May',
    value: '5'
}, {
    text: 'June',
    value: '6'
}, {
    text: 'July',
    value: '7'
}, {
    text: 'August',
    value: '8'
}, {
    text: 'September',
    value: '9'
}, {
    text: 'October',
    value: '10'
}, {
    text: 'November',
    value: '11'
}, {
    text: 'December',
    value: '12'
}];

var months_j = [{
    text: 'Unknown',
    value: 'Unknown'
}, {
    text: 'فروردین',
    value: '1'
}, {
    text: 'اردیبهشت',
    value: '2'
}, {
    text: 'خرداد',
    value: '3'
}, {
    text: 'تیر',
    value: '4'
}, {
    text: 'مرداد',
    value: '5'
}, {
    text: 'شهریور',
    value: '6'
}, {
    text: 'مهر',
    value: '7'
}, {
    text: 'آبان',
    value: '8'
}, {
    text: 'آذر',
    value: '9'
}, {
    text: 'دی',
    value: '10'
}, {
    text: 'بهمن',
    value: '11'
}, {
    text: 'اسفند',
    value: '12'
}];

var years_j = [{
    'text': 'Unknown'
}, {
    "text": "1397"
}, {
    "text": "1396"
}, {
    "text": "1395"
}, {
    "text": "1394"
}, {
    "text": "1393"
}, {
    "text": "1392"
}, {
    "text": "1391"
}, {
    "text": "1390"
}, {
    "text": "1389"
}, {
    "text": "1388"
}, {
    "text": "1387"
}, {
    "text": "1386"
}, {
    "text": "1385"
}, {
    "text": "1384"
}, {
    "text": "1383"
}, {
    "text": "1382"
}, {
    "text": "1381"
}, {
    "text": "1380"
}, {
    "text": "1379"
}, {
    "text": "1378"
}, {
    "text": "1377"
}, {
    "text": "1376"
}, {
    "text": "1375"
}, {
    "text": "1374"
}, {
    "text": "1373"
}, {
    "text": "1372"
}, {
    "text": "1371"
}, {
    "text": "1370"
}, {
    "text": "1369"
}, {
    "text": "1368"
}, {
    "text": "1367"
}, {
    "text": "1366"
}, {
    "text": "1365"
}, {
    "text": "1364"
}, {
    "text": "1363"
}, {
    "text": "1362"
}, {
    "text": "1361"
}, {
    "text": "1360"
}, {
    "text": "1359"
}, {
    "text": "1358"
}, {
    "text": "1357"
}, {
    "text": "1356"
}, {
    "text": "1355"
}, {
    "text": "1354"
}, {
    "text": "1353"
}, {
    "text": "1352"
}, {
    "text": "1351"
}, {
    "text": "1350"
}, {
    "text": "1349"
}, {
    "text": "1348"
}, {
    "text": "1347"
}, {
    "text": "1346"
}, {
    "text": "1345"
}, {
    "text": "1344"
}, {
    "text": "1343"
}, {
    "text": "1342"
}, {
    "text": "1341"
}, {
    "text": "1340"
}, {
    "text": "1339"
}, {
    "text": "1338"
}, {
    "text": "1337"
}, {
    "text": "1336"
}, {
    "text": "1335"
}, {
    "text": "1334"
}, {
    "text": "1333"
}, {
    "text": "1332"
}, {
    "text": "1331"
}, {
    "text": "1330"
}, {
    "text": "1329"
}, {
    "text": "1328"
}, {
    "text": "1327"
}, {
    "text": "1326"
}, {
    "text": "1325"
}, {
    "text": "1324"
}, {
    "text": "1323"
}, {
    "text": "1322"
}, {
    "text": "1321"
}, {
    "text": "1320"
}, {
    "text": "1319"
}, {
    "text": "1318"
}, {
    "text": "1317"
}, {
    "text": "1316"
}, {
    "text": "1315"
}, {
    "text": "1314"
}, {
    "text": "1313"
}, {
    "text": "1312"
}, {
    "text": "1311"
}, {
    "text": "1310"
}, {
    "text": "1309"
}, {
    "text": "1308"
}, {
    "text": "1307"
}, {
    "text": "1306"
}, {
    "text": "1305"
}, {
    "text": "1304"
}, {
    "text": "1303"
}, {
    "text": "1302"
}, {
    "text": "1301"
}, {
    "text": "1300"
}, {
    "text": "1299"
}, {
    "text": "1298"
}, {
    "text": "1297"
}, {
    "text": "1296"
}, {
    "text": "1295"
}, {
    "text": "1294"
}, {
    "text": "1293"
}, {
    "text": "1292"
}, {
    "text": "1291"
}, {
    "text": "1290"
}, {
    "text": "1289"
}, {
    "text": "1288"
}, {
    "text": "1287"
}, {
    "text": "1286"
}, {
    "text": "1285"
}, {
    "text": "1284"
}, {
    "text": "1283"
}, {
    "text": "1282"
}, {
    "text": "1281"
}, {
    "text": "1280"
}, {
    "text": "1279"
}]
var years = [{
    text: 'Unknown'
}, {
    text: '2021'
}, {
    text: '2020'
}, {
    text: '2019'
}, {
    text: '2018'
}, {
    text: '2017'
}, {
    text: '2016'
}, {
    text: '2015'
}, {
    text: '2014'
}, {
    text: '2013'
}, {
    text: '2012'
}, {
    text: '2011'
}, {
    text: '2010'
}, {
    text: '2009'
}, {
    text: '2008'
}, {
    text: '2007'
}, {
    text: '2006'
}, {
    text: '2005'
}, {
    text: '2004'
}, {
    text: '2003'
}, {
    text: '2002'
}, {
    text: '2001'
}, {
    text: '2000'
}, {
    text: '1999'
}, {
    text: '1998'
}, {
    text: '1997'
}, {
    text: '1996'
}, {
    text: '1995'
}, {
    text: '1994'
}, {
    text: '1993'
}, {
    text: '1992'
}, {
    text: '1991'
}, {
    text: '1990'
}, {
    text: '1989'
}, {
    text: '1988'
}, {
    text: '1987'
}, {
    text: '1986'
}, {
    text: '1985'
}, {
    text: '1984'
}, {
    text: '1983'
}, {
    text: '1982'
}, {
    text: '1981'
}, {
    text: '1980'
}, {
    text: '1979'
}, {
    text: '1978'
}, {
    text: '1977'
}, {
    text: '1976'
}, {
    text: '1975'
}, {
    text: '1974'
}, {
    text: '1973'
}, {
    text: '1972'
}, {
    text: '1971'
}, {
    text: '1970'
}, {
    text: '1969'
}, {
    text: '1968'
}, {
    text: '1967'
}, {
    text: '1966'
}, {
    text: '1965'
}, {
    text: '1964'
}, {
    text: '1963'
}, {
    text: '1962'
}, {
    text: '1961'
}, {
    text: '1960'
}, {
    text: '1959'
}, {
    text: '1958'
}, {
    text: '1957'
}, {
    text: '1956'
}, {
    text: '1955'
}, {
    text: '1954'
}, {
    text: '1953'
}, {
    text: '1952'
}, {
    text: '1951'
}, {
    text: '1950'
}, {
    text: '1949'
}, {
    text: '1948'
}, {
    text: '1947'
}, {
    text: '1946'
}, {
    text: '1945'
}, {
    text: '1944'
}, {
    text: '1943'
}, {
    text: '1942'
}, {
    text: '1941'
}, {
    text: '1940'
}, {
    text: '1939'
}, {
    text: '1938'
}, {
    text: '1937'
}, {
    text: '1936'
}, {
    text: '1935'
}, {
    text: '1934'
}, {
    text: '1933'
}, {
    text: '1932'
}, {
    text: '1931'
}, {
    text: '1930'
}, {
    text: '1929'
}, {
    text: '1928'
}, {
    text: '1927'
}, {
    text: '1926'
}, {
    text: '1925'
}, {
    text: '1924'
}, {
    text: '1923'
}, {
    text: '1922'
}, {
    text: '1921'
}, {
    text: '1920'
}, {
    text: '1919'
}, {
    text: '1918'
}, {
    text: '1917'
}, {
    text: '1916'
}, {
    text: '1915'
}, {
    text: '1914'
}, {
    text: '1913'
}, {
    text: '1912'
}, {
    text: '1911'
}, {
    text: '1910'
}, {
    text: '1909'
}, {
    text: '1908'
}, {
    text: '1907'
}, {
    text: '1906'
}, {
    text: '1905'
}, {
    text: '1904'
}, {
    text: '1903'
}, {
    text: '1902'
}, {
    text: '1901'
}]

var activity_persicuted = [{
    name_en: "Artist",
    name_fa: "هنرمند"
}, {
    name_en: "Blogger",
    name_fa: "بلاگر"
}, {
    name_en: "Children's Rights Activist",
    name_fa: "فعال دفاع از حقوق کودکان"
}, {
    name_en: "Civic Activist",
    name_fa: "فعال مدنی"
}, {
    name_en: "Educational Rights Activist",
    name_fa: "فعال دفاع از حق تحصیل"
}, {
    name_en: "Human Rights Defender",
    name_fa: "فعال حقوق بشر"
}, {
    name_en: "Journalist",
    name_fa: "روزنامه‌نگار"
}, {
    name_en: "Political Rights Activist",
    name_fa: "فعال سیاسی"
}, {
    name_en: "Religious Minority Rights Activist",
    name_fa: "فعال دفاع از حقوق اقلیتهای مذهبی"
}, {
    name_en: "Religious Minority Practitioner",
    name_fa: "فعال دفاع از حقوق اقلیتهای قومی"
}, {
    name_en: "Student Activist",
    name_fa: "فعال دانشجوئی"
}, {
    name_en: "Women's Rights Activist",
    name_fa: "فعال دفاع از حقوق زنان"
}, {
    name_en: "Writer",
    name_fa: "نویسنده"
}]




angular.module("ui.select").run(["$templateCache", function($templateCache) {
    $templateCache.put("bootstrap/select.tpl.html", "<div class=\"ui-select-container ui-select-bootstrap dropdown\" ng-class=\"{open: $select.open}\"><div class=\"ui-select-match\"></div><input type=\"text\" autocomplete=\"off\" tabindex=\"-1\" aria-expanded=\"true\" aria-label=\"{{ $select.baseTitle }}\" aria-owns=\"ui-select-choices-{{ $select.generatedId }}\" aria-activedescendant=\"ui-select-choices-row-{{ $select.generatedId }}-{{ $select.activeIndex }}\" class=\"form-control ui-select-search\" placeholder=\"{{$select.placeholder}}\" ng-model=\"$select.search\" ng-show=\"$select.searchEnabled && $select.open\"><div class=\"ui-select-choices\"></div></div>");
    $templateCache.put("bootstrap/choices.tpl.html", "<ul class=\"ui-select-choices ui-select-choices-content dropdown-menu\" role=\"listbox\" ng-show=\"$select.items.length > 0\"><li class=\"ui-select-choices-group\" id=\"ui-select-choices-{{ $select.generatedId }}\"><div class=\"divider\" ng-show=\"$select.isGrouped && $index > 0\"></div><div ng-show=\"$select.isGrouped\" class=\"ui-select-choices-group-label dropdown-header\" ng-bind=\"$group.name\"></div><div id=\"ui-select-choices-row-{{ $select.generatedId }}-{{$index}}\" class=\"ui-select-choices-row\" ng-class=\"{active: $select.isActive(this), disabled: $select.isDisabled(this)}\" role=\"option\"><a href=\"javascript:void(0)\" class=\"ui-select-choices-row-inner\"></a></div></li></ul>");
    $templateCache.put("bootstrap/match.tpl.html", "<div class=\"ui-select-match\" ng-hide=\"$select.open\" ng-disabled=\"$select.disabled\" ng-class=\"{\'btn-default-focus\':$select.focus}\"><span tabindex=\"-1\" class=\"btn btn-default form-control ui-select-toggle\" aria-label=\"{{ $select.baseTitle }} activate\" ng-disabled=\"$select.disabled\" ng-click=\"$select.activate()\" style=\"outline: 0;\"><span ng-show=\"$select.isEmpty()\" class=\"ui-select-placeholder text-muted\">{{$select.placeholder}}</span> <span ng-hide=\"$select.isEmpty()\" class=\"ui-select-match-text pull-left\" ng-class=\"{\'ui-select-allow-clear\': $select.allowClear && !$select.isEmpty()}\" ng-transclude=\"\"></span> <i class=\"icon-arrow-combo pull-right\" ng-click=\"$select.toggle($event)\"></i> <a ng-show=\"$select.allowClear && !$select.isEmpty()\" aria-label=\"{{ $select.baseTitle }} clear\" style=\"margin-right: 10px\" ng-click=\"$select.clear($event)\" class=\"btn btn-xs btn-link pull-right\"><i class=\"glyphicon glyphicon-remove\" aria-hidden=\"true\"></i></a></span></div>");

}]);
