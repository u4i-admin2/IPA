UFI.directive('judgesBasicInfo', function() {
    return {
        controller: function($scope, $http) {
            if (method == 'POST') {
                $('.judgeBasicInfoHolder').hide()
                $('.basicInfo').show()
            }


            $scope.addBiography = function() {

                var req = {
                    method: method,
                    url: '/api/judges/judge/' + id,
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
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {

                    $('.bioHolder').toggle()
                    $('.formBio').toggle()
                    updateView();


                }).error(function(error) {
                    console.log(error)
                });


            }
            $scope.editBio = function() {
                $scope.judgeAddtionalInfo = $scope.current;
                $('.bioHolder').toggle()
                $('.formBio').toggle()

            }

            $scope.editJudge = function(e) {
                e.preventDefault()

                $scope.judgeBasicInfo = {}
                $scope.judgeBasicInfo = $scope.current
                delete $scope.judgeBasicInfo.picture

                $scope.judgeBasicInfo.ethnicity_fa = $scope.current.ethnicity != null ? $scope.current.ethnicity.name_fa : null;
                $scope.judgeBasicInfo.ethnicity = $scope.current.ethnicity != null ? $scope.current.ethnicity.name_en : null;
                $scope.judgeBasicInfo.city_fa = $scope.current.birth_city != null ? $scope.current.birth_city.name_fa : null;
                $scope.judgeBasicInfo.city = $scope.current.birth_city != null ? $scope.current.birth_city.name_en : null;

                $('.judgeBasicInfoHolder').toggle()
                $('.basicInfo').toggle()


                if ($scope.judgeBasicInfo.dob_year_fa) {

                    $scope.date.dob = {
                        day_j: {
                            text: $scope.judgeBasicInfo.dob_day_fa,
                            value: $scope.judgeBasicInfo.dob_day_fa
                        },
                        month_j: {
                            text: $scope.judgeBasicInfo.dob_month_fa,
                            value: $scope.judgeBasicInfo.dob_month_fa
                        },
                        year_j: {
                            text: $scope.judgeBasicInfo.dob_year_fa,
                            value: $scope.judgeBasicInfo.dob_year_fa
                        }
                    }
                    $scope.onSelectDate_j('dob')
                }

            }

            $scope.saveBasicInfo = function() {


                if ($scope.date.dob) {

                    $scope.judgeBasicInfo.dob_day = $scope.date.dob.day ? $scope.date.dob.day.value : null;
                    $scope.judgeBasicInfo.dob_month = $scope.date.dob.month ? $scope.date.dob.month.value : null;
                    $scope.judgeBasicInfo.dob_year = $scope.date.dob.year ? $scope.date.dob.year.text : null;

                    $scope.judgeBasicInfo.dob_day_fa = $scope.date.dob.day_j ? $scope.date.dob.day_j.value : null;
                    $scope.judgeBasicInfo.dob_month_fa = $scope.date.dob.month_j ? $scope.date.dob.month_j.value : null;
                    $scope.judgeBasicInfo.dob_year_fa = $scope.date.dob.year_j ? $scope.date.dob.year_j.text : null;

                }

                $scope.judgeBasicInfo.birth_city_id = $scope.judgeBasicInfo.city_id;
                $scope.judgeBasicInfo.birth_province_id = $scope.judgeBasicInfo.province_id;

                var req = {
                    method: method,
                    url: '/api/judges/judge/' + id,
                    fields: {
                        csrfmiddlewaretoken: token
                    },
                    headers: {
                        'X-CSRFToken': token
                    },
                    data: $scope.judgeBasicInfo,
                    params: {
                        csrfmiddlewaretoken: token
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {

                    id = response.id + '/'
                    varID = response.id
                    method = 'PUT';
                    $scope.method = 'PUT';
                    updateView();
                    $('.judgeBasicInfoHolder').toggle()
                    $('.basicInfo').toggle()

                }).error(function(error) {
                    console.log(error)
                });


            }

        },
        templateUrl: ipa.staticPrefix + 'ui/templates/judgesBasicInfo.html'
    };
})
