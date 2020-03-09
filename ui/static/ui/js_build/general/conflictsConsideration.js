// conflictsConsideration.js

UFI.directive('conflictsConsideration', function() {
    return {
        controller: function($scope, $http) {

            $scope.getText = function(obj) {
                return obj.replace(/\n/g, '<br/><br/>')
            };

            $scope.addComment = function() {

                $scope._comment[idTag + '_id'] = varID;
                $scope._comment.is_published = true;

                var req = {
                    method: 'POST',
                    url: '/api/' + idTag + 's/' + idTag + 'comment/',
                    fields: {
                        csrfmiddlewaretoken: token
                    },
                    headers: {
                        'X-CSRFToken': token
                    },
                    data: $scope._comment,
                    params: {
                        csrfmiddlewaretoken: token
                    }
                }

                $http(req).success(function(response) {
                    $scope._comment = {}
                    $scope.conflictsconsideration.$setPristine();
                    $scope.current.comments.unshift(response)

                }).error(function(error) {
                    console.log(error)
                });
            }

        },
        templateUrl: ipa.staticPrefix + 'ui/templates/conflictsConsideration.html'
    };
})
