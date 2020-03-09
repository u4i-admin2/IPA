// prisonsIndex.js


UFI.controller('prisons', function($scope, $http) {
    var toggle = "";
    var order = "";
    $scope.data = [];
    $scope.next = [];
    $scope.prev = [];
    $http({
        url: '/api/prisons/prison/',
        params: {
            limit: 20
        },
        method: 'GET'
    }).success(function(data) {
        $scope.data = data.results;
        $scope.next = data.next;
        $scope.prev = data.previous;

    }).error(function(err) {
        "ERR", console.log(err)
    })

    $scope.paginate = function(url) {
        $http({
            url: url,
            method: 'GET'
        }).success(function(data) {
            $scope.data = data.results;
            $scope.next = data.next;
            $scope.prev = data.previous;

        }).error(function(err) {
            "ERR", console.log(err)
        })

    }

    $scope.order = function(_order) {
        order = _order;
        if (toggle == "") {
            toggle = "-"
        } else {
            toggle = ""
        }
        $scope.updateTable();
    }

    $scope.updateTable = function() {


        $http({
            url: '/api/prisons/prison/',
            params: {
                limit: 10,
                ordering: toggle + order,
            },
            method: 'GET'
        }).success(function(data) {
            $scope.data = data.results;
            $scope.next = data.next;
            $scope.prev = data.previous;

        }).error(function(err) {
            "ERR", console.log(err)
        })
    }


})
