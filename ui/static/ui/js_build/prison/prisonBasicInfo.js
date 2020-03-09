// prisonBasicInfo.js

UFI.directive('prisonBasicInfo', function() {
    return {
        controller: function($scope, $http) {

            if (method == 'POST') {
                $('.addBasicInfo').toggle();
                $('.prisonbasicInfoform').toggle();
            } else {
                $http({
                    url: '/api/prisons/prison/' + id,
                    method: 'GET'
                }).success(function(data) {

                }).error(function(err) {
                    "ERR", console.log(err)
                })
            }

            $scope.prisonbasicInfo = {}

            $scope.editPrisonBasicInfo = function(e) {
                e.preventDefault();
                $('.addBasicInfo').toggle();
                $('.prisonbasicInfoform').toggle();


                shouldConfirm = true;

                $scope.prisonbasicInfo = $scope.current

                if ($scope.current.opened_year_fa) {
                    $scope.date.od = {
                        day_j: {
                            text: $scope.current.opened_day_fa,
                            value: $scope.current.opened_day
                        },
                        month_j: {
                            text: $scope.current.opened_month_fa,
                            value: $scope.current.opened_month_fa
                        },
                        year_j: {
                            text: $scope.current.opened_year_fa,
                            value: $scope.current.opened_year_fa
                        }
                    }


                    $scope.onSelectDate_j('od')
                }

            }

            $scope.addPrisonbasicInfo = function() {


                if ($scope.date.od) {
                    $scope.prisonbasicInfo.opened_day = $scope.date.od.day ? $scope.date.od.day.value : null;
                    $scope.prisonbasicInfo.opened_month = $scope.date.od.month ? $scope.date.od.month.value : null;
                    $scope.prisonbasicInfo.opened_year = $scope.date.od.year ? $scope.date.od.year.text : null;

                    $scope.prisonbasicInfo.opened_day_fa = $scope.date.od.day_j ? $scope.date.od.day_j.value : null;
                    $scope.prisonbasicInfo.opened_month_fa = $scope.date.od.month_j ? $scope.date.od.month_j.value : null;
                    $scope.prisonbasicInfo.opened_year_fa = $scope.date.od.year_j ? $scope.date.od.year_j.text : null;

                }

                delete $scope.prisonbasicInfo.picture

                var req = {
                    method: method,
                    url: '/api/prisons/prison/' + id,
                    fields: {
                        csrfmiddlewaretoken: token
                    },
                    headers: {
                        'X-CSRFToken': token
                    },
                    data: $scope.prisonbasicInfo,
                    params: {
                        csrfmiddlewaretoken: token
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {

                    $('.addBasicInfo').toggle();
                    $('.prisonbasicInfoform').toggle();
                    id = response.id + '/'
                    varID = response.id
                    method = 'PUT';
                    $scope.method = 'PUT';
                    updateView();


                }).error(function(error) {
                    console.log(error)
                })
            }


        },
        templateUrl: ipa.staticPrefix + 'ui/templates/prisonsBasicInfo.html'
    };
});
