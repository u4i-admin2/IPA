UFI.directive('judgeAdditionalInfo', function() {
    return {
        controller: function($scope, $http) {
            $scope.editFormerPositionStatus = false;
            $scope.judgeAddtionalInfo = {}

            $scope.addFormerPosition = function() {


                $scope.judgeAddtionalInfo.court_and_branch_id = $scope.judgeAddtionalInfo.courtandbranch_id
                $scope.judgeAddtionalInfo.judicial_position_id = $scope.judgeAddtionalInfo.judicialposition_id
                $scope.judgeAddtionalInfo.judge_id = varID

                if ($scope.date.sd) {

                    $scope.judgeAddtionalInfo.started_day = $scope.date.sd.day ? $scope.date.sd.day.value : null;
                    $scope.judgeAddtionalInfo.started_month = $scope.date.sd.month ? $scope.date.sd.month.value : null;
                    $scope.judgeAddtionalInfo.started_year = $scope.date.sd.year ? $scope.date.sd.year.text : null;

                    $scope.judgeAddtionalInfo.started_day_fa = $scope.date.sd.day_j ? $scope.date.sd.day_j.value : null;
                    $scope.judgeAddtionalInfo.started_month_fa = $scope.date.sd.month_j ? $scope.date.sd.month_j.value : null;
                    $scope.judgeAddtionalInfo.started_year_fa = $scope.date.sd.year_j ? $scope.date.sd.year_j.text : null;

                }
                if ($scope.date.ed) {

                    $scope.judgeAddtionalInfo.ended_day = $scope.date.ed.day ? $scope.date.ed.day.value : null;
                    $scope.judgeAddtionalInfo.ended_month = $scope.date.ed.month ? $scope.date.ed.month.value : null;
                    $scope.judgeAddtionalInfo.ended_year = $scope.date.ed.year ? $scope.date.ed.year.text : null;

                    $scope.judgeAddtionalInfo.ended_day_fa = $scope.date.ed.day_j ? $scope.date.ed.day_j.value : null;
                    $scope.judgeAddtionalInfo.ended_month_fa = $scope.date.ed.month_j ? $scope.date.ed.month_j.value : null;
                    $scope.judgeAddtionalInfo.ended_year_fa = $scope.date.ed.year_j ? $scope.date.ed.year_j.text : null;

                }

                if ($scope.editFormerPositionStatus) {


                    var req = {
                        method: 'PUT',
                        url: '/api/judges/judgeposition/' + $scope.currentFormerPosition + '/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.judgeAddtionalInfo,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                } else {
                    var req = {
                        method: 'POST',
                        url: '/api/judges/judgeposition/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.judgeAddtionalInfo,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {
                    $scope.formerPosition.$setPristine()
                    $scope.judgeAddtionalInfo = {};
                    $scope.editFormerPositionStatus = false;
                    updateView();


                }).error(function(error) {
                    console.log(error)
                });

            }

            $scope.editFormerPosition = function(id, ct) {
                $scope.currentFormerPosition = ct;

                $scope.editFormerPositionStatus = true;

                var position = $scope.current.positions[id];

                if (position.ended_year) {
                    $scope.date.ed = {
                        year_j: {
                            text: position.ended_year_fa,
                            value: position.ended_year_fa
                        }
                    }
                    $scope.date.sd = {

                        year_j: {
                            text: position.started_year_fa,
                            value: position.started_year_fa
                        }
                    }

                    $scope.onSelectDate('ed')
                    $scope.onSelectDate('sd')
                }
                $scope.judgeAddtionalInfo = {}

                $scope.judgeAddtionalInfo.judicialposition_fa = position.court_and_branch ? position.court_and_branch.name_fa : ''
                $scope.judgeAddtionalInfo.judicialposition = position.court_and_branch ? position.court_and_branch.name_en : ''
                $scope.judgeAddtionalInfo.courtandbranch_fa = position.judicial_position ? position.judicial_position.name_fa : ''
                $scope.judgeAddtionalInfo.courtandbranch = position.judicial_position ? position.judicial_position.name_en : ''


            }
            $scope.cancelEditPosition = function(e) {
                e.preventDefault()

                $scope.editFormerPositionStatus = false;

                $scope.judgeAddtionalInfo = {}
                $scope.date = {}
            }

        },
        templateUrl: ipa.staticPrefix + 'ui/templates/judgesAdditionalInfo.html'
    };
})
