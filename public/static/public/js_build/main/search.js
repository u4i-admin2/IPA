UFIF.controller('search', function($scope, $timeout, $http, $location, $rootScope) {
    var locationSearch = $location.search();

    var hasLoadedFragmentIdentifierState = false;

    $scope.current_prison = locationSearch.current_prison;

    $scope.rzSliderOptions = {
        onEnd: writeFilterStateToFragmentIdentifier,
    };

    $scope.showV2DateFilterFields = false;

    $scope.searchGroup = (
      typeof locationSearch.data === 'string'
        ? locationSearch.data // jshint ignore:line
        : $rootScope.ipa.site === 'ipa'
          ? 'prisoners' // jshint ignore:line
          : 'prisons'
    );

    $scope.mainsearch = {};

    $scope.filterObj = dimensions;

    $(document).on('mouseover', '.filterBTN', function() {
        $(this).addClass('over');
    });
    $(document).on('mouseout', '.filterBTN', function() {
        $(this).removeClass('over');
    });

    // $(document).on('tap', '.filterBTN', function() {
    //     $(this).toggleClass('on')
    // })
    $(document).on('tap', '.filterSubSection', function() {
        $(this).parent().find('.searchFilters').slideToggle();

        var $iconSpan = $(this).find('span');

        $iconSpan.toggleClass('icon-plus');
        $iconSpan.toggleClass('icon-minus');

        if ($iconSpan.hasClass('icon-minus')) {
            $scope.$broadcast('rzSliderForceRender');
        }
    });

    $(document).on('tap', ".filterSection", function() {
        $(this).parent().find('.filtersHolder').slideToggle();

        var $iconSpan = $(this).find('span');

        $iconSpan.toggleClass('icon-plus');
        $iconSpan.toggleClass('icon-minus');
    });

    $(document).on('tap', ".refine", function() {
        $('.allFilters').slideToggle();
        $('.icon-down-dir').toggle();
        $('.icon-up-dir').toggle();
    });

    setSliders();
    $scope.resetFilters = function() {
        $scope.mainsearch = {};

        if ($scope.current_prison) {
            $scope.mainsearch.current_prison = $scope.current_prison;
        }

        $scope.most_recent_prison = null;

        setSliders();

        $scope.searchtext = '';

        if (hasLoadedFragmentIdentifierState) {
            $location
                .search('state', null)
                .search('query', null)
                .replace();
        }

        $('.datePickerJalaali').val('');
    };

    var defaultFilterStates = {
        activities: [],
        administered_by: [],
        all_arrests_activities: [],
        all_arrests_charges: [],
        all_arrests_prison_treatments: [],
        all_arrests_prisons: [],
        all_sentences_death_penalty: [],
        all_sentences_exiled: [],
        all_sentences_fine: [],
        all_sentences_judges: [],
        all_sentences_lashes: [],
        all_sentences_life: [],
        all_sentences_sentence_years: {min: 0, max: 110},
        affiliations: [],
        age: {min: 0, max: 110},
        capacity: {min: 0, max: 20000},
        detention_status: [],
        ethnicity: [],
        facilities: [],
        files: [],
        gender: [],
        is_cleric: [],
        judge_type: [],
        judge_type_secondary: [],
        quotes: [],
        religion: [],
        treatments: [],
    };

    $scope.setFilter = function(catagory, item) {
        if (typeof $scope.mainsearch[catagory] == 'string') {
            $scope.mainsearch[catagory] = [$scope.mainsearch[catagory]];
        }

        $scope.mainsearch[catagory] = $scope.mainsearch[catagory] ? $scope.mainsearch[catagory] : [];
        var index = $scope.mainsearch[catagory].indexOf(item);
        if (index == -1) {
            $scope.mainsearch[catagory].push(item);
        } else {
            $scope.mainsearch[catagory].splice(index, 1);

        }

        writeFilterStateToFragmentIdentifier();

        setTimeout(function() {
            responsiveHelper();
        }, 100);
    };

    $scope.length = function(obj) {
        var len = 0;
        for (var o in obj) {
            len++;
        }

        return len;
    };

    var interval;
    $scope.setData = function(dataSet) {
        clearInterval(interval);

        $scope.searchGroup = dataSet;
        $location
            .search('data', $scope.searchGroup)
            .replace();

        $scope.resetFilters();
        $scope._data = null;
        $('.savingBlocker').fadeIn();

        var queryString = $location.search();

        // GH 2019-07-16: This seems to be necessary to fix initializing
        // search view with all_sentences_judges search parameter. e.g.
        // with URLs like this:
        //
        // /en/search/#/?data=prisoners&all_sentences_judges=Abolghasem Salavati
        //
        // It works on V1 but I can’t figure out how — all filtering is
        // done on the frontend, but I don’t see it anywhere in the JS.
        // It’s extremely possible that I’m missing something obvious
        // here.
        if (
            typeof queryString.all_sentences_judges === 'string' &&
            dataSet === 'prisoners'
        ) {
            $scope.setFilter(
                'all_sentences_judges',
                queryString.all_sentences_judges
            );
        }

        if (!hasLoadedFragmentIdentifierState) {
            readFilterStateFromFragmentIdentifier();

            readSearchQueryFromFragmentIdentifier();
        }

        $scope.$watch(
            'searchtext',
            writeSearchQueryToFragmentIdentifier
        );

        oboe({
                url: '/' + ipa.lang + '/search-' + dataSet + '/',
                headers: {
                    Accept: "application/json, text/plain, */*"
                }
            })
            .start(function() {
                $('.savingBlocker').fadeOut();
                interval = window.setInterval(function() {
                    var data = this.root();
                    $scope.$apply(function() {
                        $scope._data = data;

                    });

                }.bind(this), 10);
            })
            .done(function(data) {
                clearInterval(interval);

                $scope._data = data;

                $scope.$apply(function() {
                    $('.savingBlocker').fadeOut();

                    $scope.genrefilters = {};
                    responsiveHelper();
                });
            })
            .fail(function() {

                // we don't got it
            });
    };
    $scope.setData($scope.searchGroup);

    hasLoadedFragmentIdentifierState = true;

    function onDatePickerSelect(_unixDate) {
        // -----------------------------------
        // --- Get selected Gregorian date ---
        // -----------------------------------
        var selectedDateGregorianInfo = null;

        try {
            selectedDateGregorianInfo = this.model.state.selected.dateObject.State.gregorian;
        } catch (e) {
            console.log('Exception while getting Persian Date Picker Gregorian date:', e);
            return;
        }

        // Note: Date.getMonth() is zero-based
        var dateInfo = {
            year: selectedDateGregorianInfo.year,
            month: selectedDateGregorianInfo.month + 1,
            day: selectedDateGregorianInfo.day,
        };

        // ----------------------------
        // --- Apply state to scope ---
        // ----------------------------
        var inputElement = this.model.input.elem;
        var datePickerScopeKey = inputElement.getAttribute('data-filter-state-key');

        if (typeof datePickerScopeKey === 'string') {
            $scope.$applyAsync(function () {
                $scope.mainsearch[datePickerScopeKey] = dateInfo;

                writeFilterStateToFragmentIdentifier();
            });
        }
    }

    $timeout(function () {
        revealActiveFilters();

        $('.datePickerJalaali').pDatepicker({
            calendarType: (ipa.lang === 'en' ? 'gregorian' : 'persian'),
            format: 'YYYY/M/D',
            initialValue: false,
            onSelect: onDatePickerSelect,
        });
    });

    $scope.infilter = function(cat, v) {
        $scope.mainsearch[cat] = $scope.mainsearch[cat] ? $scope.mainsearch[cat] : [];
        if ($scope.mainsearch[cat].indexOf(v) !== -1) {
            return true;
        } else {
            return false;
        }
    };

    function setSliders() {
        $scope.sliderOptions = {};

        if ($scope.searchGroup === 'judges' | $scope.searchGroup == 'prisoners') {
            var ageMin = 0;
            var ageMax = 110;

            $scope.sliderOptions.age = {
                floor: ageMin,
                ceil: ageMax,
                onEnd: writeFilterStateToFragmentIdentifier,
            };

            $scope.mainsearch.age = {
                min: ageMin,
                max: ageMax,
            };
        }
        if ($scope.searchGroup == 'prisoners') {
            var sentenceYearsMin = 0;
            var sentenceYearsMax = 110;

            $scope.sliderOptions.sentenceYears = {
                floor: sentenceYearsMin,
                ceil: sentenceYearsMax,
                onEnd: writeFilterStateToFragmentIdentifier,
            };

            $scope.mainsearch.all_sentences_sentence_years = {
                min: sentenceYearsMin,
                max: sentenceYearsMax,
            };
        }

        if ($scope.searchGroup == 'prisons') {
            var capacityMin = 0;
            var capacityMax = 20000;

            $scope.sliderOptions.capacity = {
                floor: capacityMin,
                ceil: capacityMax,
                onEnd: writeFilterStateToFragmentIdentifier,
            };

            $scope.mainsearch.capacity = {
                min: capacityMin,
                max: capacityMax,
            };
        }
    }

    function revealActiveFilters() {
        var filterWasRevealed = false;

        angular.forEach(
            Object.keys($scope.mainsearch),
            function (fieldSlug) {
                // ===========================
                // === Bail-out conditions ===
                // ===========================

                // Stop if there’s no associated defaultFilterStates entry
                if (defaultFilterStates[fieldSlug] === undefined) {
                    console.log('revealActiveFilters: Couldn’t find ' + fieldSlug + ' in defaultFilterStates');

                    return;
                }

                // Stop if state is default
                if (_.isEqual(
                    $scope.mainsearch[fieldSlug],
                    defaultFilterStates[fieldSlug]
                )) {
                    return;
                }

                // Get .filterHolder and stop if it isn’t present
                var $filterHolder = $('.filterHolder.filter-' + fieldSlug);

                if ($filterHolder.length === 0) {
                    console.log('revealActiveFilters: Couldn’t find ' + $filterHolder.selector);

                    return;
                }

                // ==========================================================
                // === Open parent .filtersHolder if not already revealed ===
                // ==========================================================

                var $filtersHolder = $filterHolder.parent();

                if ($filtersHolder.css('display') !== 'block') {
                    var $filterSectionSpan = $filtersHolder.siblings('.filterSection').find('span.icon-plus');

                    $filtersHolder.slideToggle();
                    $filterSectionSpan.attr('class', 'icon-minus');
                }

                // ==========================================
                // === Bail if filter is already revealed ===
                // ==========================================

                var $searchFilters = $filterHolder.find('.searchFilters');

                if ($searchFilters.css('display') === 'block') {
                    console.log('revealActiveFilters: ' + fieldSlug + ' was already revealed');

                    return;
                }

                // =====================
                // === Reveal filter ===
                // =====================

                var $iconSpan = $filterHolder.find('span.icon-plus');

                $searchFilters.slideToggle();
                $iconSpan.attr('class', 'icon-minus');

                filterWasRevealed = true;
            }
        );

        if (filterWasRevealed) {
            $scope.$broadcast('rzSliderForceRender');
        }
    }

    function writeFilterStateToFragmentIdentifier() {
        var encodedSerializedMainsearch = JSON.stringify($scope.mainsearch);

        $location
            .search('state', encodedSerializedMainsearch)
            .replace();
    }

    function readFilterStateFromFragmentIdentifier() {
        var locationStateValue = $location.search().state;

        if (!locationStateValue) {
            return;
        }

        var decodedDeserializedMainsearch = JSON.parse(locationStateValue);

        $scope.mainsearch = decodedDeserializedMainsearch;
    }

    function readSearchQueryFromFragmentIdentifier() {
        var locationQueryValue = $location.search().query;

        if (!locationQueryValue) {
            return;
        }

        $scope.searchtext = locationQueryValue;
    }

    function writeSearchQueryToFragmentIdentifier() {
        if (
            typeof $scope.searchtext === 'string' &&
            $scope.searchtext.length > 0
        ) {
            $location
                .search('query', $scope.searchtext)
                .replace();
        }
    }
});


UFIF.filter('mainFilter', function() {
    return function(items, filterSets) {

        filterSets = filterSets ? filterSets : {};
        items = items ? items : [];

        var testCount = 0;
        if (filterSets.detention_status) {
            var ds = filterSets.detention_status[0] === 'true' || filterSets.detention_status[0] === true ? true : null;
            if (ds)
                filterSets.detention_status[0] = ds;
        }

        var i;
        var item;

        var filtered = [];
        angular.forEach(filterSets, function(v, k) {
            filterSets[k] = typeof filterSets[k] == "string" ? [filterSets[k]] : filterSets[k];
            var tempItems = [];
            if (filterSets[k].length !== 0 && k !== 'age' && k !== 'detention_status' && k !== 'current_prison' && k !== 'all_sentences_sentence_years' && k !== 'capacity') {



                // for ( i = 0; i < items.length; i++) {
                angular.forEach(items, function(_v, i) {

                    item = items[i];
                    if (typeof item[k] == 'string' || typeof item[k] == 'boolean') {

                        if (filterSets[k].indexOf(item[k]) !== -1) {
                            tempItems.push(item);


                        }
                    } else {
                        var blocker = true;

                        angular.forEach(item[k], function(_v, _k) {

                            if (filterSets[k].indexOf(_v) !== -1 && blocker) {

                                blocker = false;
                                if (_k === 0) tempItems.unshift(item);
                                else tempItems.push(item);
                            }

                        });
                    }


                });

                items = tempItems;
            }

            if (k == 'detention_status') {

                if (filterSets[k].length) {

                    for (i = 0; i < items.length; i++) {

                        item = items[i];


                        if (item.current_prison) {
                            tempItems.push(item);
                        }
                    }
                    items = tempItems;
                }
            }

            if (k == 'current_prison') {


                if (filterSets[k]) {

                    for (i = 0; i < items.length; i++) {
                        item = items[i];

                        if (item.current_prison == filterSets[k]) {


                            tempItems.push(item);
                        }

                    }
                    items = tempItems;

                }

            }


            if (k == 'all_sentences_sentence_years') {
                for (i = 0; i < items.length; i++) {
                    item = items[i];

                    if (item[k]) {




                        item[k].sort(function(a, b) {
                            return b - a;
                        });

                        if (item[k][0] >= filterSets[k].min && item[k][0] <= filterSets[k].max) {

                            tempItems.push(item);
                        }

                    }


                }

                items = tempItems;
            }
            if (k == 'age' || k == 'capacity') {
                for (i = 0; i < items.length; i++) {
                    item = items[i];

                    if (k == 'age') {
                        item[k] = item[k] < 0 ? 0 : item[k];
                    }



                    if (item[k] >= filterSets[k].min && item[k] <= filterSets[k].max) {

                        tempItems.push(item);

                    } else {

                    }
                }
                items = tempItems;
            }
            filtered = items;

        });
        setTimeout(function() {
            responsiveHelper();
        }, 10);



        return filtered;
    };
});
