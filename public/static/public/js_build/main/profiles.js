UFIF.controller('prisoner', function($scope, $timeout, $http, $location, $sce) {

    $scope.url = $location.absUrl();

    // attach data to scope
    $scope.entityData = entityData;
    $scope.dLang = ipa.dLang;
    $scope.lang = ipa.lang;
    $scope.type = "prisoner";

    // calculate age
    $scope.calcAge = function(year, month, day) {
        if (year) {
            var _year = year ? year : 01;
            var _month = month ? month : 01;
            var _day = day ? day : 01;
            var dateString = _year + '-' + _month + '-' + _day;
            var birthday = +new Date(dateString);
            return ~~((Date.now() - birthday) / (31557600000));
        } else {
            return;
        }
    };

    var explanationBody = $scope.entityData['explanation_' + ipa.lang];

    $scope.explanationBody = (typeof explanationBody === 'string' && explanationBody.length > 0) ? $sce.trustAsHtml(explanationBody) : null;

    $scope.prisonerPrerenderedComponentHtml = window.prisonerPrerenderedComponentHtml;

    $scope.trustAsHtml = function(html) {
        return $sce.trustAsHtml(html);
    };

    // get highest judge sentance
    var judgeArray = ['research', 'primary', 'appeal', 'supreme'];

    $scope.getHighestsentance = function(sentences) {
        var highsentence = 0;
        var rate = 0;

        angular.forEach(sentences, function(value, key) {
            var jt = 0;
            if (value.judge) {
                jt = judgeArray.indexOf(value.judge.judge_type) > -1 ? judgeArray.indexOf(value.judge.judge_type) : 0;
            }
            if (rate <= jt) {

                var yearN = " Year";
                var monthN = " Month";

                if (ipa.lang == 'en') {
                    yearN = value.sentence_years > 1 ? " Years" : " Year";
                    monthN = value.sentence_months > 1 ? " Months" : " Month";
                } else {
                    yearN = value.sentence_years > 1 ? " سال" : " سال";
                    monthN = value.sentence_months > 1 ? " ماه" : " ماه";
                }

                var year = value.sentence_years ? value.sentence_years + yearN : '';
                var month = value.sentence_months ? value.sentence_months + monthN : '';

                var death_penalty = value.death_penalty ? (ipa.lang == 'en' ? 'Execution' : 'اعدام') : '';

                var exile = value.exiled ? (ipa.lang == 'en' ? 'Exile' : 'تبعید') : '';
                var life = value.life ? (ipa.lang == 'en' ? 'Life in Prison' : 'حبس ابد') : '';
                var fine = value.fine ? (ipa.lang == 'en' ? 'Fine ' : 'جریمه ') + value.fine  + (ipa.lang == 'en' ? ' IRR' : ' ﷼'): '';
                var lashes = value.number_of_lashes ? value.number_of_lashes + (ipa.lang == 'en' ? ' Lashes' : ' ضربه شلاق') : '';

                highsentence = [
                    year,
                    month,
                    death_penalty,
                    exile,
                    life,
                    fine,
                    lashes
                ];
                rate = jt;
            }
        });
        var Unknown = ipa.lang == 'en' ? 'Unknown' : '​نامعلوم';

        var highsentenceSentence = [];

        angular.forEach(highsentence, function(value, i) {
            if (value) {
                highsentenceSentence.push(value);
            }
        });

        return highsentenceSentence.join(ipa.commaCharacter + ' ');
    };





    matcher(".matcher");


});


UFIF.controller('prison', function($scope, $timeout, $http, $location, $sce) {
    $scope.url = $location.absUrl();
    $scope.viewData = viewData;
    $scope.type = "prison";
    $scope.entityData = JSON.parse(viewData.prison);

    $scope.dLang = ipa.dLang;
    $scope.lang = ipa.lang;

    var explanationBody = $scope.entityData[
        'explanation_' +
        (ipa.site === 'aea' ? 'aea_' : '') +
        ipa.lang
    ];

    $scope.explanationBody = (typeof explanationBody === 'string' && explanationBody.length > 0) ? $sce.trustAsHtml(explanationBody) : null;

    angular.forEach($scope.entityData.facilities_objs, function(value, key) {
        var icon = value.name_en.replace(/\s/g, '').replace(/\W+/g, "").toLowerCase();
        $('.' + icon).attr('class', $('.' + icon).attr('class') + ' on');
        $('.' + icon).attr('data-id', value.id);
    });


    $scope.selectedName = '';
    $scope.selectedInfo = '';


    $(document).on('click', '.facility', function() {

        var _this = $(this);

        var id = _this.attr('data-id');

        angular.forEach($scope.entityData.facilitylinks, function(value, key) {
            if (value.facility == id) {
                $('.facility').removeClass('selected');
                _this.addClass('selected');
                $scope.$apply(function() {
                    $scope.selectedInfo = value['description_' + ipa.lang];
                });
            }
        });

        angular.forEach($scope.entityData.facilities_objs, function(value, key) {
            if (value.id == id) {

                $scope.$apply(function() {
                    $scope.selectedName = value['name_' + ipa.lang];
                });
            }
        });
    });
    matcher(".matcher");

});

UFIF.directive('prisonerAccordian', function() {
    return {
        controller: function($scope, $http, $timeout) {
            /**
             * @param {MouseEvent} event
             */
            $scope.openClose = function(event, id) {
                if (event.target.classList.contains(
                    'ipa-information-overlay-trigger-button'
                )) {
                    return;
                }

                console.log(id);
                $('.expandArea' + id).stop();
                // $('.arrest').removeClass('open');
                // $('.arrestArrow').removeClass('open');
                // $('.expandArea').slideUp();
                // add for toggle
                $('.expandArea' + id).slideToggle();
                $('.arrest' + id).toggleClass('open');
                $('.arrestArrow' + id).toggleClass('open');
            };

            $scope.showTip = function(i) {
                console.log(i);
                _this = $('.' + i);
                console.log(_this.position());
                _this.css({
                    top: -_this.height() - 10
                });
                _this.stop();
                _this.fadeToggle();
            };

            $scope.detentionDate = ['detention_year', 'detention_month', 'detention_day'];
            $scope.arrestDate = ['arrest_year ', 'arrest_month', 'arrest_day'];
            $scope.detentionOrder = true;
            $scope.arrestOrder = true;

        }
    };
});




// general


UFIF.directive('timeline', function() {
    return {
        controller: function($scope, $http, $sce) {
            var r1 = ipa.lang == 'en' ? 'Reverse Chronological' : 'از جدید به قدیم​';
            var r2 = ipa.lang == 'en' ? 'Chronological' : 'از جدید به قدیم​';
            $scope.reverseTile = r1;

            $scope.timeLimit = 7;
            $scope.addMoreTimeLine = function() {
                $scope.timeLimit += 7;
            };
            $scope.predicate = ['year', 'month', 'day'];
            $scope.reverse = true;

            $scope.reverseTimeline = function() {
                $scope.reverse = $scope.reverse ? false : true;
                $scope.reverseTile = $scope.reverse ? r1 : r2;
            };

            $scope.timelineItemsWithCurrentLanguageDescription = [];

            angular.forEach(
                $scope.entityData.timeline,
                function (timelineItem) {
                    if (typeof timelineItem['description_' + ipa.lang + '_html'] === 'string') {
                        timelineItem['description_' + ipa.lang + '_html'] = (
                            $sce.trustAsHtml(timelineItem['description_' + ipa.lang + '_html'])
                        );

                        $scope.timelineItemsWithCurrentLanguageDescription.push(timelineItem);
                    }
                }
            );

            $scope.timelineItemsVisible = function(lang) {
                return $scope.timelineItemsWithCurrentLanguageDescription
                    .filter(
                        function(item){
                            return !!item['description_' + lang];
                        }
                    )
                    .length;
            };
        }
    };
});

UFIF.directive('quotes', function() {
    return {
        controller: function($scope, $http) {
            $scope.entityData.quotesWithCurrentLocaleText = (
                $scope.entityData.quotes.filter(
                    function (quote) {
                        return (
                            typeof quote['name_' + ipa.lang] === 'string' &&
                            typeof quote['quote_' + ipa.lang] === 'string'
                        );
                    }
                )
            );

            $scope.quoteIndex = Math.floor(
                Math.random() * $scope.entityData.quotesWithCurrentLocaleText.length
            );
        }
    };
});

UFIF.directive('supportingEvidence', function() {
    return {
        controller: function($scope, $http, $timeout) {
            $scope.filter = {
                'file_type': ''
            };
            $scope.limit = 4;

            function resizeImages() {
                $timeout(function() {
                    $(".supporting-image").each(function(index) {
                        _this = $(this);
                        if (_this.width() < _this.height()) {
                            _this.addClass('taller');
                        } else {
                            _this.addClass('wider');
                        }
                        _this.fadeIn();
                    });
                    responsiveHelper();

                }, 1000);
            }
            $scope.filterEvidence = function(filter) {
                $scope.filter = {
                    'file_type': filter
                };
                console.log($scope.filter);
                resizeImages();
            };
            $scope.addMoreEvidence = function() {
                $scope.limit += 2;
                resizeImages();
            };

            resizeImages();


        }
    };
});
