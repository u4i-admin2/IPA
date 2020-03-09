// searchResults.js

UFI.controller('searchResults', function($scope, $upload, $http, $timeout) {

    $scope._prisoners = [];
    $scope._prison = [];
    $scope._judge = [];
    $http({
        url: "/api/search/?q=" + searchQ
    }).success(function(result) {

        angular.forEach(result, function(value, key) {
            console.log(value)

            if (value.type == 'prisoner') {
                $scope._prisoners.push(value)
            }

            if (value.type == 'prison') {
                $scope._prison.push(value)
            }

            if (value.type == 'judge') {
                $scope._judge.push(value)
            }
        });


    });

})
