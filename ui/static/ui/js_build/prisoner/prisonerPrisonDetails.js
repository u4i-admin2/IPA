// prisonerPrisonDetails.js


UFI.directive('prisonerPrisonDetails', function() {
    return {
        controller: function($scope, $http) {
            $scope.prisonerPrison = {};
            $scope.onSelectArrest = function() {

                $scope.date.doi = {};
                if (this.$select.selected.arrest_year) {
                    $scope.date.doi.year = {
                        text: this.$select.selected.arrest_year,
                        value: this.$select.selected.arrest_year
                    }
                }
                if (this.$select.selected.arrest_month) {
                    $scope.date.doi.month = {
                        text: this.$select.selected.arrest_month,
                        value: this.$select.selected.arrest_month
                    }
                }
                if (this.$select.selected.arrest_day) {
                    $scope.date.doi.day = {
                        text: this.$select.selected.arrest_day,
                        value: this.$select.selected.arrest_day
                    }
                }

                $scope.onSelectDate('doi')
                $scope.onSelectDate_j('doi')
                $scope.prisonerPrison.arrest_id = this.$select.selected.id;

            }

            $scope.editPrisonerDetails = function(detention) {



                if (detention.detention_year_fa) {
                    $scope.date.doi = {
                        year_j: {
                            text: detention.detention_year_fa,
                            value: detention.detention_year_fa
                        },
                        month_j: {
                            text: detention.detention_month_fa,
                            value: detention.detention_month_fa
                        },
                        day_j: {
                            text: detention.detention_day_fa,
                            value: detention.detention_day_fa
                        }
                    }

                    $scope.onSelectDate_j('doi')

                }

                $scope.prisonerPrison.detention_type = detention.detention_type;
                $scope.prisonerPrison.prison = detention.prison.name_en;
                $scope.prisonerPrison.prison_fa = detention.prison.name_fa;
                $scope.prisonerPrison.prisontreatment_array = detention.treatment_objs;
                $scope.prisonerPrison.id = detention.treatment_ids;
                $scope.prisonerPrison.activity_persecuted_for = detention.activity_persecuted_for
                $scope.prisonerPrison.activity_persecuted_for_objs = detention.activity_persecuted_for
                $scope.prisonerPrison.dId = detention.id
                $scope.prisonerPrison.arrest_id = detention.arrest_id
                $scope.prisonerPrison.is_published = true;



                $scope.editPrisonerDetailsMode = true;

            }

            $scope.cancelEditPrisonerDetails = function(e) {
                e.preventDefault();
                $scope.editPrisonerDetailsMode = false;
                $scope.prisonerPrison = {};
                $scope.date.doi = {};
            }


            $scope.savePrisonerPrisonDetails = function() {


                if ($scope.date.doi) {
                    $scope.prisonerPrison.detention_day = $scope.date.doi.day ? $scope.date.doi.day.value : null;
                    $scope.prisonerPrison.detention_month = $scope.date.doi.month ? $scope.date.doi.month.value : null;
                    $scope.prisonerPrison.detention_year = $scope.date.doi.year ? $scope.date.doi.year.text : null;
                    $scope.prisonerPrison.detention_day_fa = $scope.date.doi.day_j ? $scope.date.doi.day_j.value : null;
                    $scope.prisonerPrison.detention_month_fa = $scope.date.doi.month_j ? $scope.date.doi.month_j.value : null;
                    $scope.prisonerPrison.detention_year_fa = $scope.date.doi.year_j ? $scope.date.doi.year_j.text : null;
                }

                $scope.prisonerPrison.treatment_ids = $scope.prisonerPrison.id;
                $scope.prisonerPrison.is_published = true;

                if ($scope.editPrisonerDetailsMode) {
                    var req = {
                        method: 'PUT',
                        url: '/api/' + idTag + 's/' + idTag + 'detention/' + $scope.prisonerPrison.dId + '/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.prisonerPrison,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                } else {
                    var req = {
                        method: 'POST',
                        url: '/api/' + idTag + 's/' + idTag + 'detention/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.prisonerPrison,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {

                    $scope.prisonerPrison = {}
                    $scope.editPrisonerDetailsMode = false;
                    updateView()

                }).error(function(error) {
                    console.log(error)
                });
            }

        },
        templateUrl: ipa.staticPrefix + 'ui/templates/prisonerPrisonDetails.html'
    };
})
