// detentionDetails.js

UFI.directive('detentionDetails', function() {
    return {
        controller: function($scope, $http) {

            $scope.detentionstatusYes = []
            $scope.detentionstatusNo = []
            $http({
                url: '/api/prisoners/detentionstatus/',
                method: 'GET'
            }).success(function(data) {

                for (var key in data.results) {

                   console.log(data.results[key]);

                    if (data.results[key].detained) {
                        $scope.detentionstatusYes.push(data.results[key])
                    } else {
                        $scope.detentionstatusNo.push(data.results[key])
                    }
                }


            }).error(function(err) {
                "ERR", console.log(err)
            })

            $scope.isDetained = function(status) {
                if (status) {

                    var detained = status.detained  ? "yes" : "no";

                    return detained;
                } else {
                    return '';
                }


            }

            $scope.onSelectDetentionDate = function() {

                $scope.date.dod = {};
                if (this.$select.selected.arrest_year_fa) {
                    $scope.date.dod.year_j = {
                        text: this.$select.selected.arrest_year_fa,
                        value: this.$select.selected.arrest_year_fa
                    }
                }
                if (this.$select.selected.arrest_month) {
                    $scope.date.dod.month_j = {
                        text: this.$select.selected.arrest_month_fa,
                        value: this.$select.selected.arrest_month_fa
                    }
                }
                if (this.$select.selected.arrest_day) {
                    $scope.date.dod.day_j = {
                        text: this.$select.selected.arrest_day_fa,
                        value: this.$select.selected.arrest_day_fa
                    }
                }

                $scope.onSelectDate_j('dod')

            }

            $scope.editDetention = function(e) {
                e.preventDefault();
                $('.dentionHolder').toggle();
                $('.detentionForm').toggle();

                $scope.detention_status = {};


                if ($scope.current.detention_year_fa) {
                    $scope.date.dod = {
                        day_j: {
                            text: $scope.current.detention_day_fa,
                            value: $scope.current.detention_day_fa
                        },
                        month_j: {
                            text: $scope.current.detention_month_fa,
                            value: $scope.current.detention_month_fa
                        },
                        year_j: {
                            text: $scope.current.detention_year_fa,
                            value: $scope.current.detention_year_fa
                        }
                    }

                    $scope.onSelectDate_j('dod')

                }

                $scope.detention_status.detention_is_approx = $scope.current.detention_is_approx;
                $scope.detention_status.activity_persecuted_for_objs = $scope.current.detention_status;

                $scope.detention_status.detained = $scope.current.detention_status.name_en.substring(0, 1) == "Y" ? false : true;

            }

            $scope.onSelectDetention = function() {

                $scope.detention_status.detention_status = this.$select.selected.id;

            }

            $scope.saveDetention = function() {

                if ($scope.date.dod) {
                    $scope.detention_status.detention_day = $scope.date.dod.day ? $scope.date.dod.day.value : null;
                    $scope.detention_status.detention_month = $scope.date.dod.month ? $scope.date.dod.month.value : null;
                    $scope.detention_status.detention_year = $scope.date.dod.year ? $scope.date.dod.year.text : null;
                    $scope.detention_status.detention_day_fa = $scope.date.dod.day_j ? $scope.date.dod.day_j.value : null;
                    $scope.detention_status.detention_month_fa = $scope.date.dod.month_j ? $scope.date.dod.month_j.value : null;
                    $scope.detention_status.detention_year_fa = $scope.date.dod.year_j ? $scope.date.dod.year_j.text : null;
                }

                $scope.detention_status.detention_status_id = $scope.detention_status.detention_status;
                $scope.detention_status.is_published = true;

                var req = {
                    method: 'PUT',
                    url: '/api/' + idTag + 's/' + idTag + '/' + id,
                    fields: {
                        csrfmiddlewaretoken: token
                    },
                    headers: {
                        'X-CSRFToken': token
                    },
                    data: $scope.detention_status,
                    params: {
                        csrfmiddlewaretoken: token
                    }
                }

                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {


                    updateView()
                    $('.dentionHolder').toggle();
                    $('.detentionForm').toggle();

                }).error(function(error) {
                    console.log(error)
                });
            }

        },
        templateUrl: ipa.staticPrefix + 'ui/templates/detentionDetails.html'
    };
})
