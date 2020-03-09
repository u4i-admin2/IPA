// @ts-check

/** @type {ipa.Judge.ViewDataAea | ipa.Judge.ViewDataIpa} */
var viewData = viewData;

(function () { 'use strict';

UFIF.controller(
    'judge',
    /**
     * @param {ipa.Judge.Scope} $scope
     */
    function($scope, $timeout, $http, $location, $sce) {
        // attach data to scope
        $scope.url = $location.absUrl();
        $scope.viewData = viewData;
        $scope.type = "judge";
        $scope.entityData = viewData.judge;
        $scope.dLang = ipa.dLang;
        $scope.lang = ipa.lang;
        $scope.positionOrder = ['ended_year'];

        var explanationBody = $scope.entityData[
            'explanation_' +
            (ipa.site === 'aea' ? 'aea_' : '') +
            ipa.lang
        ];

        $scope.explanationBody = (typeof explanationBody === 'string' && explanationBody.length > 0) ? $sce.trustAsHtml(explanationBody) : null;

        $scope.getJudgeSearch = function(judgeData, lang) {
            var otherLang = lang == 'fa' ? 'en' : 'fa';
            var firstName = judgeData['forename_' + lang] ? judgeData['forename_' + lang] + ' ' : (judgeData['forename_' + otherLang] ? judgeData['forename_' + otherLang] + ' ' : '');

            var lastName = judgeData['surname_' + lang];

            return '/' + lang + '/search/#/?data=prisoners&all_sentences_judges=' + firstName + lastName;
        };

        $scope.calcAge = function(year, month, day) {
            if (year) {
                var _year = year ? year : 1;
                var _month = month ? month : 1;
                var _day = day ? day : 1;
                var dateString = _year + '-' + _month + '-' + _day;
                var birthday = +new Date(dateString);
                return ~~((Date.now() - birthday) / (31557600000));
            } else {
                return;
            }
        };

        matcher(".matcher");
        matcher("._matcher");
    }
);

})();
