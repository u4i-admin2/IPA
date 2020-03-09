// base js

// xcvxcv


// angular
var UFI = angular
    .module('unitedForIran', ['ngPersian', 'ngSanitize', "checklist-model", 'ui.select', 'angularFileUpload'])
    .config(function($interpolateProvider) {
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    })
    .config(function($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    })
    .config(function($sceDelegateProvider) {
        var resourceUrlWhitelist = [
          'self'
        ];

        if (ipa.staticPrefix.indexOf('http') === 0) {
          resourceUrlWhitelist.push(ipa.staticPrefix + '**');
        }

        $sceDelegateProvider.resourceUrlWhitelist(resourceUrlWhitelist);
      })


UFI.run(function($rootScope, $templateCache) {
    $rootScope.$on('$viewContentLoaded', function() {
        $templateCache.removeAll();
    });
});
// dropdown search vars
var currentTabed = -1;
var _form = null;
var _section = null;
var _field = null;
var _type = null;

UFI.run(function($rootScope) {
    $rootScope.Object = Object;
    $rootScope.ipa = ipa;
});



UFI.controller('maincontroller', function($scope, $upload, $http, $timeout) {

    $scope.disabelPrisoners = false;
    $scope.disabelPrisons = false;
    var dirtyArray = null
    $scope.method = method;

    $scope.idTAG = idTag;


    $scope.judge = [];


    if (method == 'POST') {

    } else {

        $http({
            url: '/api/' + idTag + 's/' + idTag + '/' + id,
            method: 'GET'
        }).success(function(data) {

            console.log(data)

            $scope.current = data;

            if (idTag == 'prisoner' && method == 'PUT') {


                $scope.prisonerBasicInfo = $scope.current;


            }

            if (data.dob_year_fa && method == 'POST') {
                $scope.date.dob = {
                    day_j: {
                        text: $scope.current.dob_day_fa,
                        value: $scope.current.dob_day_fa
                    },
                    month_j: {
                        text: $scope.current.dob_month_fa,
                        value: $scope.current.dob_month_fa
                    },
                    year_j: {
                        text: $scope.current.dob_year_fa,
                        value: $scope.current.dob_year_fa
                    }
                }

                $scope.onSelectDate_j('dob')
            }

        }).error(function(err) {
            "ERR", console.log(err)
        })

    }
    $scope.days = days;
    $scope.months = months;
    $scope.years = years;
    $scope.months_j = months_j;
    $scope.years_j = years_j;
    $scope.date = {};
    $scope.judge = [];
    var _form = null;
    var _section = null;
    var _field = null;
    var _type = null;



    $scope.form = [];
    $scope.picture = null;

    $scope.publishItem = function() {

        var req = {
            method: method,
            url: '/api/' + idTag + 's/' + idTag + '/' + id,
            fields: {
                csrfmiddlewaretoken: token
            },
            headers: {
                'X-CSRFToken': token
            },
            data: {
                is_published: true
            },
            params: {
                csrfmiddlewaretoken: token
            }
        }

        $http(req).success(function(response) {

            $(".publishPopUp").fadeIn();

            setTimeout(function() {
                $(".publishPopUp").fadeOut();
            }, 3000)



        }).error(function(error) {
            console.log(error)
        })
    }

    $scope.unpublishItem = function() {

        var req = {
            method: method,
            url: '/api/' + idTag + 's/' + idTag + '/' + id,
            fields: {
                csrfmiddlewaretoken: token
            },
            headers: {
                'X-CSRFToken': token
            },
            data: {
                is_published: false
            },
            params: {
                csrfmiddlewaretoken: token
            }
        }

        $http(req).success(function(response) {

            $(".unpublishPopUp").fadeIn();

            setTimeout(function() {
                $(".unpublishPopUp").fadeOut();
            }, 3000)



        }).error(function(error) {
            console.log(error)
        })
    }

    $scope.confirmDelete = function() {

        var req = {
            method: 'DELETE',
            url: '/api/' + idTag + 's/' + idTag + '/' + id,
            fields: {
                csrfmiddlewaretoken: token
            },
            headers: {
                'X-CSRFToken': token
            },
            params: {
                csrfmiddlewaretoken: token
            }
        }

        $http(req).success(function(response) {

            window.location.href = '/dashboard/';

        }).error(function(error) {
            console.log(error)
        })


    }

    $scope.deleteItem = function() {
        resizer()
        $(".deletePopUp").fadeIn();


    }
    $scope.cancleDelete = function() {
        resizer()
        $(".deletePopUp").fadeOut();

    }


    $scope.submitForm2 = function() {

        $scope.upload($scope.files2);

    };

    $scope.delete = function(deleteId, apiCall) {
        resizer()
        $('.areyousure').fadeIn();


        $scope.currentDelete = {
            "deleteId": deleteId,
            "apiCall": apiCall
        }

    }

    $scope.cancelDelete = function() {

        $('.areyousure').fadeOut();
    }


    $scope.deleteItemData = function() {

        var req = {
            method: 'DELETE',
            url: '/api/' + idTag + 's/' + idTag + $scope.currentDelete.apiCall + '/' + $scope.currentDelete.deleteId + '/',
            fields: {
                csrfmiddlewaretoken: token
            },
            headers: {
                'X-CSRFToken': token
            },
            params: {
                csrfmiddlewaretoken: token
            }
        }
        $('.areyousure').fadeOut();
        $(".savingBlocker").fadeIn();
        $http(req).success(function(response) {
            $http({
                url: '/api/' + idTag + 's/' + idTag + '/' + id,
                method: 'GET'
            }).success(function(data) {
                $scope.current = data;

                resizer();
                $scope.edit = false;
                updateView()

            }).error(function(err) {
                "ERR", console.log(err)
            })

        }).error(function(error) {
            console.log(error)
        });
    }




    $scope.date = {}



    updateView = function() {

        $http({
            url: '/api/' + idTag + 's/' + idTag + '/' + id,
            method: 'GET'
        }).success(function(data) {

            setTimeout(function() {
                $('.savingBlocker').fadeOut();
            }, 1500)

            $scope.current = data;
            $scope.prisoner = data;
            $scope.date = {};

            resizer();
            setTimeout(function() {
                thumbs()
            }, 100)
            setTimeout(function() {
                thumbs()
            }, 3000)


        }).error(function(err) {
            "ERR", console.log(err)
        })
    }

    function thumbs() {
        $(".thumb").each(function() {
            var thumb = $(this);
            var thumbW = thumb.width();
            var thumbH = thumb.height();
            if (thumbW < thumbH) {

                thumb.width(75)
            } else {
                thumb.height(75)
            }
        });


    }

    setTimeout(function() {
        thumbs()
    }, 100)
    setTimeout(function() {
        thumbs()
    }, 3000)




    $scope.date = {}



    var dict = [];


    if (idTag == "judge") {

        dict = judgeTags
    }
    if (idTag == "prison") {

        dict = prisonTags
    }
    if (idTag == "prisoner") {

        dict = prisonerTags
    }

    var searchResults = []
    $scope.fieldNames = []
    $scope.source = {}



    $scope.search = function(type, value, section, field, route, term) {
        currentTabed = -1
        _section = section;
        _field = field;
        _type = type;
        _term = term;
        _special = false;

        var patt = new RegExp(value, 'i');



        if (value.length > 0) {
            searchResults = []
            $.each(dict, function(index, value) {

                if (patt.test(value)) {

                    searchResults.push({
                        name_en: value,
                        id: value
                    })
                }
            });

            $scope[section][field] = searchResults;
        }
    }








    $scope.addToList = function(id, name, root) {

        if ($scope[root][id + "_id"]) {
            if ($scope[root][name] == undefined) {

                $scope[root][name] = []
            }

            if ($scope[root][name].indexOf($scope[root][id + "_id"]) < 0) {

                $scope[root][name].push($scope[root][id + "_id"])

                if ($scope[root][id + '_array'] == undefined) {

                    $scope[root][id + '_array'] = []
                }

                $scope[root][id + '_array'].push({
                    name_en: $scope[root][id],
                    name_fa: $scope[root][id + '_fa']
                })

                $scope[root][id] = '';
                $scope[root][id + '_fa'] = '';

            }

        } else {
            $scope[root][id] = null;

        }

    }

    $scope.removeFromList = function(index, id, name, root) {

        $scope[root][id + '_array'].splice(index, 1);
        $scope[root][name].splice(index, 1);

    }

    $scope.selectDD = function() {


        $scope[_section][_field].forEach(function(i) {
            i.selected = false;
        })
        var id = _type + '_id'
        if ($scope[_section][_field].length > 0) {
            $scope[_section][_field][this.$index].selected = true;
            $scope[_section][_type] = $scope[_section][_field][this.$index][_term + '_en'];
            $scope[_section][_type + "_fa"] = $scope[_section][_field][this.$index][_term + '_fa'];
            $scope[_section][id] = $scope[_section][_field][this.$index].id;
            if (_special) {

                $scope[_section][_type] = $scope[_section][_field][this.$index]['forename_en'] + " " + $scope[_section][_field][this.$index][_term + '_en'];
                $scope[_section][_type + "_fa"] = $scope[_section][_field][this.$index]['forename_fa'] + " " + $scope[_section][_field][this.$index][_term + '_fa'];

            }
        }
    }

    $(window).keydown(function(event) {
        if (event.keyCode == 13) {
            if ($(document.activeElement)[0].nodeName === 'INPUT')
               event.preventDefault();

            $('.pointer').click();
            $scope.$apply(function() {

                if (_section != null) {
                    $scope[_section][_field] = []
                }

            });
        }
    });

    $(document).keydown(function(e) {
        switch (e.which) {
            case 38: // up

                if (e.keyCode == 38 && currentTabed > 0) {
                    currentTabed -= 1;
                    tab()
                }
                break;
            case 40: // down
                if (e.keyCode == 40 && currentTabed < $scope[_section][_field].length - 1) {
                    currentTabed += 1;
                    tab()
                }
                break;

            default:
                return; // exit this handler for other keys
        }
    });

    $(document).on("keypress", "input", function(e) {
        if (e.keyCode == 13) {}
        if (_section != null) {

            if (e.keyCode == 13) {

                $scope.$apply(function() {

                    $scope[_section][_field] = []

                });
            }
        }
    });
    $(document).on("focusout", "input", function() {
        if (_section != null) {
            $scope.$apply(function() {
                $scope[_section][_field] = []
            })
        }
    });

    $scope.selectFrom = function() {
        if (_section != null) {
            $scope.$apply(function() {
                $scope[_section][_field] = []
            })
        }

    }

    function tab() {
        $scope.$apply(function() {
            $scope[_section][_field].forEach(function(i) {
                i.selected = false;
            })
            var id = _type + '_id'

            $scope[_section][_field][currentTabed].selected = true;
            $scope[_section][_type] = $scope[_section][_field][currentTabed][_term + '_en'];
            $scope[_section][_type + "_fa"] = $scope[_section][_field][currentTabed][_term + '_fa'];
            $scope[_section][id] = $scope[_section][_field][currentTabed].id;

            if (_special) {
                $scope[_section][_type] = $scope[_section][_field][currentTabed]['forename_en'] + " " + $scope[_section][_field][currentTabed][_term + '_en'];
                $scope[_section][_type + "_fa"] = $scope[_section][_field][currentTabed]['forename_fa'] + " " + $scope[_section][_field][currentTabed][_term + '_fa'];

            }
        });

    }

    var _term = null;
    $scope.editTimelineStatus = false;



    $scope.predict = function(type, value, section, field, route, term, special) {

        currentTabed = -1
        _special = special ? special : false;
        _section = section;
        _field = field;
        _type = type;
        _term = term;
        if (value != undefined) {
            $http({
                url: "/api/" + route + "/" + type + "/?q=" + value,

                method: 'GET'
            }).success(function(data) {

                console.log(data)

                $scope[section][field] = data.results;

            }).error(function(err) {
                "ERR", console.log(err)
            })
        }
        if (value == "" || value == undefined) {

            var id = _type + '_id'

            $scope[_section][_type] = null
            $scope[_section][_type + "_fa"] = null
            $scope[_section][id] = null
        }

    }


    $scope.onSelectDate_j = function(id) {

        var noYear = true;
        if ($scope.date[id].year_j) {
            if ($scope.date[id].year_j.text == 'Unknown' || $scope.date[id].year_j.text == null) {
                $scope.date[id].year = null
                $scope.date[id].month = null
                $scope.date[id].day = null

                $scope.date[id].year_j = null
                $scope.date[id].month_j = null
                $scope.date[id].day_j = null
                return
            }
        } else {
            $scope.date[id].year = {
                text: 1393
            }
            noYear = false;
        }
        if ($scope.date[id] == undefined) {
            $scope.date[id] = this[id]
        }
        var noDay = $scope.date[id].day_j ? true : false;
        var noMonth = $scope.date[id].month_j ? true : false;



        if ($scope.date[id].day_j) {
            if ($scope.date[id].day_j.text == null) {
                $scope.date[id].day_j = {
                    'text': 1,
                    'value': 1
                };
                noDay = null

            }

            if ($scope.date[id].day_j.text == 'Unknown') {
                $scope.date[id].day_j = {
                    'text': 1,
                    'value': 1
                };
                noDay = 'Unknown';
            }

        } else {
            $scope.date[id].day_j = {
                'text': 1,
                'value': 1
            };
        }

        if ($scope.date[id].month_j) {

            if ($scope.date[id].month_j.text == null) {
                $scope.date[id].month_j = {
                    'text': 1,
                    'value': 1
                };
                noMonth = null
            }

            if ($scope.date[id].month_j.text == 'Unknown') {
                $scope.date[id].month_j = {
                    'text': 1,
                    'value': 1
                };
                noMonth = 'Unknown';
            }

        } else {
            $scope.date[id].month_j = {
                'text': 1,
                'value': 1
            };
        }



        if ($scope.date[id].day_j && $scope.date[id].month_j && $scope.date[id].year_j) {

            var date = toGregorian(parseInt($scope.date[id].year_j.text), parseInt($scope.date[id].month_j.value), parseInt($scope.date[id].day_j.text))

            if (noYear) {
                $scope.date[id].year = {
                    text: date.gy,
                    value: date.gy,
                };
            } else {
                $scope.date[id].year_j = null
            }


            if (noMonth == true) {
                $scope.date[id].month = {
                    text: $scope.months[date.gm].text,
                    value: date.gm
                };
            } else {
                $scope.date[id].month_j = noMonth == 'Unknown' ? {
                    text: 'Unknown',
                    value: null
                } : null;

                $scope.date[id].month = noMonth == 'Unknown' ? {
                    text: 'Unknown',
                    value: null
                } : null;
            }

            if (noDay == true) {
                $scope.date[id].day = {
                    text: date.gd,
                    value: date.gd
                };
            } else {
                $scope.date[id].day_j = noDay == 'Unknown' ? {
                    text: 'Unknown',
                    value: null
                } : null;

                $scope.date[id].day = noDay == 'Unknown' ? {
                    text: 'Unknown',
                    value: null
                } : null;

            }
        }

    }

    $scope.onSelectDate = function(id) {

        var noYear = true;
        if ($scope.date[id].year) {
            if ($scope.date[id].year.text == 'Unknown') {
                $scope.date[id].year = null
                $scope.date[id].month = null
                $scope.date[id].day = null

                $scope.date[id].year_j = null
                $scope.date[id].month_j = null
                $scope.date[id].day_j = null
                return
            }

            if ($scope.date[id].year.text == null) {
                $scope.date[id].year = {
                    text: new Date().getFullYear()
                }
                noYear = false;
            }
        } else {
            $scope.date[id].year = {
                text: new Date().getFullYear()
            }
            noYear = false;
        }

        if ($scope.date[id] == undefined) {
            $scope.date[id] = this[id]
        }

        var noDay = $scope.date[id].day ? true : false;
        var noMonth = $scope.date[id].month ? true : false;

        if ($scope.date[id].day) {

            if ($scope.date[id].day.text == null) {
                $scope.date[id].day = {
                    'text': 21,
                    'value': 21
                };
                noDay = null;

            }

            if ($scope.date[id].day.text == 'Unknown') {
                $scope.date[id].day = {
                    'text': 21,
                    'value': 21
                };
                noDay = 'Unknown';
            }

        } else {
            $scope.date[id].day = {
                'text': 21,
                'value': 21
            };
        }

        if ($scope.date[id].month) {

            if ($scope.date[id].month.text == null) {
                $scope.date[id].month = {
                    'text': 3,
                    'value': 3
                };
                noMonth = null
            }

            if ($scope.date[id].month.text == 'Unknown') {
                $scope.date[id].month = {
                    'text': 3,
                    'value': 3
                };
                noMonth = 'Unknown';
            }

        } else {
            $scope.date[id].month = {
                'text': 3,
                'value': 3
            };
        }


        if ($scope.date[id].day && $scope.date[id].month && $scope.date[id].year) {

            var date = toJalaali(parseInt($scope.date[id].year.text), parseInt($scope.date[id].month.value), parseInt($scope.date[id].day.text));

            if (noYear) {
                $scope.date[id].year_j = {
                    text: date.jy,
                    value: date.jy
                };
            } else {
                $scope.date[id].year = null;
            }


            if (noMonth == true) {
                $scope.date[id].month_j = {
                    text: $scope.months_j[date.jm].text,
                    value: date.jm
                };
            } else {
                $scope.date[id].month = noMonth == 'Unknown' ? {
                    text: 'Unknown',
                    value: null
                } : null;

                $scope.date[id].month_j = noMonth == 'Unknown' ? {
                    text: 'Unknown',
                    value: null
                } : null;
            }

            if (noDay == true) {
                $scope.date[id].day_j = {
                    text: date.jd,
                    value: date.jd
                };
            } else {
                $scope.date[id].day = noDay == 'Unknown' ? {
                    text: 'Unknown',
                    value: null
                } : null;

                $scope.date[id].day_j = noDay == 'Unknown' ? {
                    text: 'Unknown',
                    value: null
                } : null;
            }
        }
    }

}).directive('date', function() {

    return {
        compile: function(element, attrs) {

            var htmlText = '<div class="row ">' + '<ui-select ' + attrs.required + ' ng-required="' + attrs.validationProp + '" class="col-xs-3 date"  name="' + attrs.localModel + '_day" on-select="onSelectDate(' + attrs.localModel + ')" ng-model="date[' + attrs.localModel + '].day" theme="bootstrap">' + '<ui-select-match placeholder="Day">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in days | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '<ui-select ' + attrs.required + ' ng-required="' + attrs.validationProp + '"class="col-xs-3 date"   name="' + attrs.localModel + '_month" on-select="onSelectDate(' + attrs.localModel + ')" ng-model="date[' + attrs.localModel + '].month" theme="bootstrap">' + '<ui-select-match placeholder="Months">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in months | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '<ui-select ' + attrs.required + ' ng-required="' + attrs.validationProp + '"class="col-xs-3 date"  name="' + attrs.localModel + '_year" on-select="onSelectDate(' + attrs.localModel + ')" ng-model="date[' + attrs.localModel + '].year" theme="bootstrap">' + '<ui-select-match placeholder="Years">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in years | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '</div>';
            element.replaceWith(htmlText);

        }

    };
}).directive('datefa', function() {

    return {
        compile: function(element, attrs) {


            var htmlText = '<div class="row">' + '<ui-select ' + attrs.required + '  ng-required="' + attrs.validationProp + '" name="' + attrs.localModel + '_day_j" class="col-xs-3 date" on-select="onSelectDate_j(' + attrs.localModel + ')" ng-model="date[' + attrs.localModel + '].day_j" theme="bootstrap">' + '<ui-select-match placeholder="روز">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in days | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '<ui-select ' + attrs.required + ' ng-required="' + attrs.validationProp + '"class="col-xs-3 date"  name="' + attrs.localModel + '_month_j" ng-model="date[' + attrs.localModel + '].month_j" on-select="onSelectDate_j(' + attrs.localModel + ')" theme="bootstrap">' + '<ui-select-match placeholder="ماه">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in months_j | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '<ui-select ' + attrs.required + ' ng-required="' + attrs.validationProp + '"class="col-xs-3 date"  name="' + attrs.localModel + '_year_j" on-select="onSelectDate_j(' + attrs.localModel + ')" ng-model="date[' + attrs.localModel + '].year_j" theme="bootstrap">' + '<ui-select-match placeholder="سال">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in years_j | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '</div>'
            element.replaceWith(htmlText);
        }

    };
}).directive('datefayear', function() {

    return {

        compile: function(element, attrs) {



            var htmlText = '<div class="row" >' + '<ui-select ' + attrs.required + '   ng-required="' + attrs.validationProp + '" name="' + attrs.localModel + '_day_j" class="col-xs-3 date hidden" on-select="onSelectDate_j(' + attrs.localModel + ')" ng-model="date[' + attrs.localModel + '].day_j" theme="bootstrap">' + '<ui-select-match placeholder="روز">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in days | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '<ui-select ' + attrs.required + ' ng-required="' + attrs.validationProp + '"class="col-xs-3 date hidden "  name="' + attrs.localModel + '_month_j" ng-model="date[' + attrs.localModel + '].month_j" on-select="onSelectDate_j(' + attrs.localModel + ')" theme="bootstrap">' + '<ui-select-match placeholder="ماه">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in months_j | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '<ui-select ' + attrs.required + ' ng-required="' + attrs.validationProp + '"class="col-xs-6 date"  name="' + attrs.localModel + '_year_j" on-select="onSelectDate_j(' + attrs.localModel + ')" ng-model="date[' + attrs.localModel + '].year_j" theme="bootstrap">' + '<ui-select-match placeholder="سال">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in years_j | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '</div>'
            element.replaceWith(htmlText);

        }

    };
}).directive('dateyear', function() {

    return {

        compile: function(element, attrs, scope) {


            var htmlText = '<div class="row" >' + '<ui-select ' + attrs.required + ' ng-required="' + attrs.validationProp + '" class="col-xs-3 date hidden"  name="' + attrs.localModel + '_day" on-select="onSelectDate(' + attrs.localModel + ')" ng-model="date[' + attrs.localModel + '].day" theme="bootstrap">' + '<ui-select-match placeholder="Day">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in days | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '<ui-select ' + attrs.required + ' ng-required="' + attrs.validationProp + '"class="col-xs-3 date hidden"   name="' + attrs.localModel + '_month" on-select="onSelectDate(' + attrs.localModel + ')" ng-model="date[' + attrs.localModel + '].month" theme="bootstrap">' + '<ui-select-match placeholder="Months">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in months | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '<ui-select ' + attrs.required + ' ng-required="' + attrs.validationProp + '"class="col-xs-6 date"  name="' + attrs.localModel + '_year" on-select="onSelectDate(' + attrs.localModel + ')" ng-model="date[' + attrs.localModel + '].year" theme="bootstrap">' + '<ui-select-match placeholder="Years">{$$select.selected.text$}</ui-select-match>' + '<ui-select-choices repeat="item in years | filter: $select.search">' + '<div ng-bind-html="item.text"></div>' + '</ui-select-choices>' + '</ui-select>' + '</div>';
            element.replaceWith(htmlText);

        }

    };
})





$(document).on('keydown', ':input[type="number"]', function(e) {
    // Allow: backspace, delete, tab, escape, enter and .

    if ($.inArray(e.keyCode, [46, 8, 9, 27, 13, 110, 190, 173, 86, 37, 39]) !== -1 ||
        // Allow: Ctrl+A, Command+A
        (e.keyCode == 65 && (e.ctrlKey === true || e.metaKey === true)) ||
        // Allow: home, end, left, right, down, up
        (e.keyCode >= 35 && e.keyCode <= 40)) {
        // let it happen, don't do anything
        return;
    }
    // Ensure that it is a number and stop the keypress
    if ((e.shiftKey || (e.keyCode < 48 || e.keyCode > 57)) && (e.keyCode < 96 || e.keyCode > 105)) {
        e.preventDefault();
    }
});


UFI.directive('alertPopUp', function() {

    return {

        compile: function(element, attrs) {

            var htmlText = '<div class="alertPopUp deletePopUp">' + '<div class="messageArea">Are you sure you want to delete this entry?</div>' + '<div class="buttons">' + '<button ng-click="cancleDelete()" class="btn btn-primary">CANCLE</button>' + '<button ng-click="confirmDelete()" class="btn btn-primary">OK</button>' + '</div>' + '<div class="blankOut" ></div></div>';
            element.replaceWith(htmlText);

        }

    };
})



UFI.directive('unpublishPopUp', function() {
    return {
        controller: function($scope, $http) {

        },
        compile: function(element, attrs) {

            var htmlText = '<div class="alertPopUp unpublishPopUp">' + '<div class="messageArea">Succefully Unpublished</div>' + '</div>';
            element.replaceWith(htmlText);

        }
    }

})


UFI.directive('publishPopUp', function() {
    return {
        controller: function($scope, $http) {

        },
        compile: function(element, attrs) {

            var htmlText = '<div class="alertPopUp publishPopUp">' + '<div class="messageArea">Succefully Published</div>' + '</div>';
            element.replaceWith(htmlText);

        }
    }

})


UFI.directive("limitTo", [function() {
    return {
        restrict: "A",
        link: function(scope, elem, attrs) {
            var limit = parseInt(attrs.limitTo);
            angular.element(elem).on("keypress", function(e) {

                if (this.value.length == limit && e.keyCode != 8) return false;
            });
        }
    }
}]);


$(document).on("click", ".checkBox", function(e) {
    var radioBTN = $(this).parent().children('input')
    radioBTN.click();
})

UFI.controller('downloadcsv', function($scope, $upload, $http, $timeout) {

    $scope._downloadcsv = function() {

        window.location.assign("/api/prisoners/csv/")

        // var req = {
        //     method: 'GET',
        //     url: '/api/prisoners/csv/'

        // }

        // $http(req).success(function(response) {


        //     window.location.assign("/api/prisoners/csv/")

        // }).error(function(error) {
        //     console.log(error)
        // })



    }


})



// helpers

$('.btn-danger').click(function() {

    $('.form-group').toggleClass('has-error')
})

$(document).ready(function() {
    resizer()
    $('.search').click(function() {

        $('#searchBox').focus()
    })


    $(document).on("click", ".section-title", function() {
        $(this).parent().children('.sectionHide').slideToggle();
        $(this).parent().toggleClass('visible');
        $(this).find(".toggleSection").toggleClass('icon-minus');
        $(this).find(".toggleSection").toggleClass('icon-plus');
    });


    $(document).on("click", ".icon-search", function() {
        if ($('#searchBox').val().length > 1) {
            window.location.href = '/dashboard/search/?q=' + $('#searchBox').val();
        } else {
            $('#searchBox').focus()
        }

    })


    $("#searchBox").keydown(function(event) {

        if (event.which == 13) {
            event.preventDefault();
            window.location.href = '/dashboard/search/?q=' + $('#searchBox').val();
        }

    });


})


$(window).resize(function() {
    resizer()
});

function resizer() {

    var _width = $(window).width();
    var _top = $(window).height();

    $('.alertPopUp').css({
        'left': _width / 2 - 150,
        'top': (_top * 0.3) - ($('.alertPopUp').height() / 2)
    })

    $('.areyousure').css({
        'left': _width / 2 - 150,
        'top': (_top * 0.3) - ($('.alertPopUp').height() / 2)
    })


}
