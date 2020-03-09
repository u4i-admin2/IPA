// timeline.js

UFI.directive('timeline', function() {
    return {
        controller: function($scope, $http) {

            var currentTimeline = null;
            $scope.editTimelineStatus = false;


            $scope.editTimeline = function(id, ct) {

                currentTimeline = ct;



                $scope.editTimelineStatus = true;
                var timelineEdit = $scope.current.timeline[id];

                $scope.date.tld = {
                    day_j: {
                        text: timelineEdit.day_fa
                    },
                    month_j: {
                        text: timelineEdit.month_fa,
                        value: timelineEdit.month_fa
                    },
                    year_j: {
                        text: timelineEdit.year_fa
                    }
                }

                $scope.timeline = {}

                $scope.timeline.timeline_is_estimate = timelineEdit.timeline_is_estimate
                $scope.timeline.source_link = timelineEdit.source_link
                $scope.timeline.description_fa = timelineEdit.description_fa
                $scope.timeline.description_en = timelineEdit.description_en
                $scope.onSelectDate_j('tld');


            }
            $scope.cancelEditTimeline = function(e) {
                e.preventDefault()


                $scope.editTimelineStatus = false;
                currentTimeline = null;
                $scope.timelineForm.$setPristine();
                $scope.timeline = {};
                $scope.date = {};
                $scope.timelineForm.$setPristine();

            }

            $scope.addTimeline = function() {


                if ($scope.date.tld) {

                    $scope.timeline.day = $scope.date.tld.day ? $scope.date.tld.day.value : null;
                    $scope.timeline.month = $scope.date.tld.month ? $scope.date.tld.month.value : null;
                    $scope.timeline.year = $scope.date.tld.year ? $scope.date.tld.year.text : null;

                    $scope.timeline.day_fa = $scope.date.tld.day_j ? $scope.date.tld.day_j.value : null;
                    $scope.timeline.month_fa = $scope.date.tld.month_j ? $scope.date.tld.month_j.value : null;
                    $scope.timeline.year_fa = $scope.date.tld.year_j ? $scope.date.tld.year_j.text : null;
                }



                $scope.timeline[idTag + '_id'] = varID;
                $scope.timeline.is_published = true;


                if ($scope.editTimelineStatus == false) {
                    var req = {
                        method: 'POST',
                        url: '/api/' + idTag + 's/' + idTag + 'timeline/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.timeline,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                } else {
                    var req = {
                        method: 'PUT',
                        url: '/api/' + idTag + 's/' + idTag + 'timeline/' + currentTimeline + '/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.timeline,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }

                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {


                    $scope.editTimelineStatus = false;
                    currentTimeline = null;
                    $scope.timelineForm.$setPristine();
                    $scope.timeline = {};
                    $scope.timelineForm.$setPristine();
                    $scope.date = {};
                    updateView();


                }).error(function(error) {
                    console.log(error)
                });


            }
        },
        templateUrl: ipa.staticPrefix + 'ui/templates/timeline.html'
    };
})
