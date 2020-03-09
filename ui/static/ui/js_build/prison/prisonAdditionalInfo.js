// prisonAdditionalInfo.js

UFI.directive('prisonAdditionalInfo', function() {
    return {
        controller: function($scope, $http) {

            $http({
                url: '/api/prisons/prisonfacility/',
                method: 'GET'
            }).success(function(data) {

                $scope.facility = data.results;

            }).error(function(err) {
                "ERR", console.log(err)
            })


            $scope.date = {}

            $scope.addFacility = function() {
                var data = {
                    name_en: $scope.prisonAdditionalInfo.facility
                }


                var req = {
                    method: 'POST',
                    url: '/api/prisons/prisonfacility/',
                    fields: {
                        csrfmiddlewaretoken: token
                    },
                    headers: {
                        'X-CSRFToken': token
                    },
                    data: data,
                    params: {
                        csrfmiddlewaretoken: token
                    }
                }

                $http(req).success(function(response) {
                    $scope.facility.push(response);

                    $scope.prisonAdditionalInfo.facility = null;

                }).error(function(error) {
                    console.log(error)
                });


            }

            $scope.prisonAdditionalInfo = {}
            $scope.prisonAdditionalInfo.fact = {};

            $scope.editPrisonInfo = function(e) {
                e.preventDefault();

                $('.addInfo').toggle();
                $('.prisonAdditionalInfoForm').toggle();

                $scope.prisonAdditionalInfo = $scope.current;
                $scope.prisonAdditionalInfo.fact = {}
                $.each($scope.current.facilities_objs, function(index, value) {
                    $scope.prisonAdditionalInfo.fact[value.id] = value.id;
                });

                $.each($scope.current.facilitylinks, function(index, value) {
                    $scope.prisonAdditionalInfo[value.facility] = {}
                    $scope.prisonAdditionalInfo[value.facility].description_en = value.description_en;
                    $scope.prisonAdditionalInfo[value.facility].description_fa = value.description_fa;
                });


            }

            $scope.addPrisonAdictionalInfo = function() {


                $scope.prisonAdditionalInfo.facilities_ids = []
                $scope.prisonAdditionalInfo.facilities_objs = []


                $.each($scope.prisonAdditionalInfo.fact, function(key, value) {

                    if (value > 0) {
                        $scope.prisonAdditionalInfo.facilities_ids.push(Number(value))
                        var _method = 'POST'
                        var tempID = ''
                        $.each($scope.current.facilitylinks, function(_key, _value) {
                            if (_value.facility == value) {
                                tempID = _value.id + '/';
                                return _method = 'PUT';
                            }
                        })
                        var rootEl = $scope.prisonAdditionalInfo[key];
                        var description_fa = rootEl ? rootEl.description_fa : '';
                        var description_en = rootEl ? rootEl.description_en : '';
                        var req = {
                            method: _method,
                            url: '/api/prisons/prisonfacilitylink/' + tempID,
                            fields: {
                                csrfmiddlewaretoken: token
                            },
                            headers: {
                                'X-CSRFToken': token
                            },
                            data: {

                                prison_id: varID,
                                facility: value,
                                description_fa: description_fa,
                                description_en: description_en,
                            },
                            params: {
                                csrfmiddlewaretoken: token
                            }
                        }
                        $http(req).success(function(response) {

                        }).error(function(error) {
                            console.log(error)
                        })
                    }
                });

                delete $scope.prisonAdditionalInfo.picture

                var req = {
                    method: method,
                    url: '/api/prisons/prison/' + id,
                    fields: {
                        csrfmiddlewaretoken: token
                    },
                    headers: {
                        'X-CSRFToken': token
                    },
                    data: $scope.prisonAdditionalInfo,
                    params: {
                        csrfmiddlewaretoken: token
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {
                    console.log(response)
                    $('.addInfo').toggle();
                    $('.prisonAdditionalInfoForm').toggle();
                    updateView()

                }).error(function(error) {
                    console.log(error)
                })
            }


        },
        templateUrl: ipa.staticPrefix + 'ui/templates/prisonAdditionalInfo.html'
    };
});
