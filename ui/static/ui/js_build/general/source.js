// source.js

UFI.directive('source', function() {
    return {
        controller: function($scope, $http) {

            $scope.judge = {}
            $scope.judge.source = {}
            $scope.editId = null;
            $scope.edit = false;



            $scope.setEdit = function(editId, index) {

                $scope.editId = editId;
                $scope.edit = true;

                var temp = $scope.current.sources[index].related_fields

                $scope.source = $scope.current.sources[index];
                $scope.source.related_fields = $scope.current.sources[index].related_fields.length > 0 ? temp.split(",") : []
                $scope.source._related_fields_array = []
                angular.forEach($scope.source.related_fields, function(value, key) {
                    $scope.source._related_fields_array[key] = {
                        'name_en': value
                    };



                })

            }

            $scope.cancelEdit = function(e) {
                e.preventDefault();
                $scope.edit = false;
                $scope.source = {}

            }

            $scope.addSource = function(edit) {

                $scope.source[idTag + "_id"] = varID;
                $scope.source.is_published = true;

                if (edit == true) {

                    var req = {
                        method: method,
                        url: '/api/' + idTag + 's/' + idTag + 'source/' + $scope.editId + '/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.source,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }

                } else {

                    var req = {
                        method: 'POST',
                        url: '/api/' + idTag + 's/' + idTag + 'source/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.source,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }

                }

                $scope.source.related_fields = $scope.source.related_fields ? $scope.source.related_fields.join(",") : '';
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {


                    $scope.source = {};
                    $scope.edit = false;
                    $scope.sourceForm.$setPristine();
                    updateView()

                }).error(function(error) {
                    console.log(error)
                });
            }

        },
        templateUrl: ipa.staticPrefix + 'ui/templates/source.html'
    };
})
