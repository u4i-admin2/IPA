// prisonerBasicInfo.js

UFI.directive('prisonerBasicInfo', function() {
    return {
        controller: function($scope, $http) {

            $scope.fadeItem = function(_class) {

                $('.' + _class).fadeToggle();
            }

            $scope.slideItem = function(_class, hiders) {

                $('.' + hiders).slideUp();
                if (!$('.' + _class).is(':visible')) {
                    $('.' + _class).slideToggle();

                }
            }

            if (method == 'POST') {
                $('.pBasicInfoHolder').toggle()
                $('.prisonerBasicInfoForm').toggle()

            } else {
                $http({
                    url: '/api/prisoners/prisoner/' + id,
                    method: 'GET'
                }).success(function(data) {


                    $scope.prisoner = data;
                }).error(function(err) {
                    "ERR", console.log(err)
                })
            }

            var holderR = null;
            var holderE = null;

            var editPrisonerMode = false;

            $scope.editPrisoner = function(e) {
                e.preventDefault();

                $scope.date.dob = {
                    day_j: {
                        text: $scope.current.dob_day_fa,
                        value: $scope.current.dob_day_fa
                    },
                    month_j: {
                        text: $scope.current.dob_month_fa,
                        value: $scope.current.dob_month_fa
                    },
                    year_j: {
                        text: $scope.current.dob_year_fa,
                        value: $scope.current.dob_year_fa
                    }
                }


                $scope.onSelectDate_j('dob')

                if (!editPrisonerMode) {
                    editPrisonerMode = true
                    holderR = holderR == null ? $scope.current.religion : holderR;
                    holderE = holderE == null ? $scope.current.ethnicity : holderE;


                    if (holderR) {
                        $scope.prisonerBasicInfo.religion_fa = holderR.name_fa;
                        $scope.prisonerBasicInfo.religion = holderR.name_en;
                    }
                    if (holderE) {
                        $scope.prisonerBasicInfo.ethnicity_fa = holderE.name_fa;
                        $scope.prisonerBasicInfo.ethnicity = holderE.name_en;
                    }
                } else {
                    editPrisonerMode = false;
                    $scope.current.religion = holderR
                    $scope.current.ethnicity = holderE
                }
                $scope.prisonerBasicInfo.country_array = $scope.current.home_countries_objs
                $scope.prisonerBasicInfo.home_countries_ids = $scope.current.home_countries_ids

                console.log(":)")
                $('.pBasicInfoHolder').toggle()
                $('.prisonerBasicInfoForm').toggle()

            }

            $scope.savePrisonerBasicInfo = function() {

                if ($scope.date.dob) {
                    $scope.prisonerBasicInfo.dob_day = $scope.date.dob.day ? $scope.date.dob.day.value : null;
                    $scope.prisonerBasicInfo.dob_month = $scope.date.dob.month ? $scope.date.dob.month.value : null;
                    $scope.prisonerBasicInfo.dob_year = $scope.date.dob.year ? $scope.date.dob.year.text : null;
                    $scope.prisonerBasicInfo.dob_day_fa = $scope.date.dob.day_j ? $scope.date.dob.day_j.value : null;
                    $scope.prisonerBasicInfo.dob_month_fa = $scope.date.dob.month_j ? $scope.date.dob.month_j.value : null;
                    $scope.prisonerBasicInfo.dob_year_fa = $scope.date.dob.year_j ? $scope.date.dob.year_j.text : null;

                }

                delete $scope.prisonerBasicInfo.picture

                var req = {
                    method: method,
                    url: '/api/' + idTag + 's/' + idTag + '/' + id,
                    fields: {
                        csrfmiddlewaretoken: token
                    },
                    headers: {
                        'X-CSRFToken': token
                    },
                    data: $scope.prisonerBasicInfo,
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
                    $('.pBasicInfoHolder').toggle()
                    $('.prisonerBasicInfoForm').toggle()
                    updateView();

                }).error(function(error) {
                    console.log(error)
                });
            }

        },
        templateUrl: ipa.staticPrefix + 'ui/templates/prisonerBasicInfo.html'
    };
})
