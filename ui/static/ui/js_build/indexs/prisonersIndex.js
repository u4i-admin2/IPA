// prisonersIndex.js



UFI.controller('prisoners', function($scope, $http) {
    $scope.filters = {
        gender: {
            text: 'Gender',
            value: null
        },
        religion: {
            text: 'Religion',
            value: null
        },
        is_detained: {
            text: 'Detention Status',
            value: null
        },
        ethnicity: {
            text: 'Ethnicity',
            value: null
        },
        has_comments: {
            text: 'Conflicts & Consideration',
            value: null
        },
        arrest_year_min: {
            text: 'Arrest Year Start',
            value: null
        },
        arrest_year_max: {
            text: 'Arrest Year End',
            value: null
        }

    };

    $scope.resetFilters = function() {

        $scope.filters = {
            gender: {
                text: 'Gender',
                value: null
            },
            religion: {
                text: 'Religion',
                value: null
            },
            is_detained: {
                text: 'Detention Status',
                value: null
            },
            ethnicity: {
                text: 'Ethnicity',
                value: null
            },
            has_comments: {
                text: 'Conflicts & Consideration',
                value: null
            },
            arrest_year_min: {
                text: 'Arrest Year Start',
                value: null
            },
            arrest_year_max: {
                text: 'Arrest Year End',
                value: null
            }

        };

        $scope.updateTable();
    }
    $scope.has_comments = has_comments;
    $scope.gender = gender;
    $scope.arrest_year_min = years;
    $scope.arrest_year_max = years;
    $scope.ethnicity = ethnicity
    $scope.is_detained = is_detained;
    $scope.religion = religion;
    $scope.data = [];
    $scope.next = [];
    $scope.prev = [];
    var toggle = "";
    var order = "";
    $http({
        url: '/api/prisoners/prisoner/',
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
            url: '/api/prisoners/prisoner/',
            params: {
                limit: 20,
                ordering: toggle + order,
                gender: $scope.filters.gender.value,
                is_detained: $scope.filters.is_detained.value,
                religion: $scope.filters.religion.value,
                ethnicity: $scope.filters.ethnicity.value,
                has_comments: $scope.filters.has_comments.value,
                arrest_year_min: $scope.filters.arrest_year_min.text,
                arrest_year_max: $scope.filters.arrest_year_max.text
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
