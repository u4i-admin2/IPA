/**
 * GH 2019-08-19: In order to support multiple profileCharts on AeA
 * pages, some state is stored in $rootScope:
 *
 * - $rootScope.profileChartsHoveredEntity
 * - $rootScope.profileChartsSelectedEntity
 * - $rootScope.profileChartsSelectedEntityInfo
 *
 * AFAIK it would be better to use an AngularJS isolate scope for this
 * directive and explicitly pass in this shared state from a parent
 * component. We can’t do this because isolate scopes require
 * template/templateUrl [1], but we can’t have Angular render the
 * template since it includes Django template tags.
 *
 * [1]: https://docs.angularjs.org/api/ng/service/$compile#-scope-
 */

UFIF.directive('profileChart', function() {
    return {
        scope: true,
        controller: function($scope, $rootScope, $http, $element) {
            $scope.variant = $element.attr('data-profile-chart-variant');

            /**
             * GH 2019-08-19: The “Selected [entity]” section is only
             * displayed in the primary profileChart. It would be better
             * to move this into its own directive but this way is
             * easier to implement without refactoring.
             */
            $scope.isPrimary = ($element.attr('data-profile-chart-is-primary') === 'true');

            var $toolTipHolderElement = $($element[0].querySelector('.toolTipHolder'));

            $(document).mousemove(function(event) {
                $toolTipHolderElement.css('top', event.pageY - $toolTipHolderElement.height() - 15);
                $toolTipHolderElement.css('left', event.pageX - 15);
            });

            $scope.type = type;
            $scope.lang = ipa.lang;

            $scope.entityType = null;

            if (ipa.site === 'aea') {
                $scope.entityType = 'report';
            } else if (ipa.site === 'ipa') {
                $scope.entityType = 'prisoner';
            }

            if ($scope.type === 'judge') {
                if ($scope.variant === 'humanRightsViolations') {
                    $scope.chartData = $scope.viewData.humanrights_violations;
                } else if ($scope.variant === 'proceduralViolations') {
                    $scope.chartData = $scope.viewData.behaviours;
                }

                $scope.chartEntityHoverInfo = $scope.viewData.chart_entity_hover_info;
            } else if ($scope.type === 'prison') {
                if (ipa.site === 'aea') {
                    if ($scope.variant === 'humanRightsViolations') {
                        $scope.chartData = $scope.viewData.humanrights_violations;
                    } else if ($scope.variant === 'proceduralViolations') {
                        $scope.chartData = $scope.viewData.procedural_violations;
                    }
                } else if (ipa.site === 'ipa') {
                    if ($scope.variant === 'mistreatments') {
                        $scope.chartData = $scope.viewData.mistreatments;
                    }
                }

                $scope.chartEntityHoverInfo = $scope.viewData.chart_entity_hover_info;
            }

            $rootScope.profileChartsHoveredEntity = ($rootScope.profileChartsHoveredEntity || "");
            $rootScope.profileChartsSelectedEntityInfo = null;
            $scope.order = ['arrest_year', 'arrest_month', 'arrest_day'];

            $scope.hoverEntity = function(entity) {
                $rootScope.profileChartsHoveredEntity = entity;
                $toolTipHolderElement.show();
                $scope.entityInfoHover = $scope.chartEntityHoverInfo[entity];
            };
            $scope.hoverOutEntity = function() {
                $rootScope.profileChartsHoveredEntity = "";
                $toolTipHolderElement.hide();
            };

            $scope.getEntity = function(entity) {
                $rootScope.profileChartsSelectedEntity = entity;

                var req = {
                    method: 'GET',
                    url: "/" + $scope.lang + '/' + $scope.entityType + '-summary/' + entity + "/"
                };

                $http(req).success(function(response) {
                    response.picture_resized = (
                      response.picture_resized
                        ? response.picture_resized // jshint ignore:line
                        : ipa.staticPrefix + 'public/img/profile_temp.png?v=2019-08-28'
                    );

                    $rootScope.profileChartsSelectedEntityInfo = response;
                }).error(function(error) {
                    console.log(error);
                });
            };

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
                        var fine = value.fine ? (ipa.lang == 'en' ? 'Fine $' : 'fine $') + value.fine : '';
                        var lashes = value.number_of_lashes ? value.number_of_lashes + (ipa.lang == 'en' ? ' Lashes' : ' ﺽﺮﺒﻫ ﺵﻼﻗ') : '';

                        highsentence = [
                            year,
                            death_penalty,
                            exile,
                            life,
                            fine,
                            lashes
                        ];


                        highsentence = [
                            year,
                            death_penalty,
                            exile,
                            life
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
        }
    };
});
