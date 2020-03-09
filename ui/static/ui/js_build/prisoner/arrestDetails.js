// arrestDetails.js


UFI.directive('arrestDetails', function() {
    return {
        controller: function($scope, $http) {



            // toggle system for the header

            $(document).on("click", ".arrestHeader", function() {
                $('.arrestBody').slideUp()

                if (!$('.arrestBody' + $(this).data('id')).is(':visible')) {
                    $('.arrestBody' + $(this).data('id')).slideToggle()
                }


                $scope.arrestDetailsEdit = {}
                $('.staticViewArrest').show();
                $('.arrestFormHolderEdit').hide();

            })



            // code for arrests

            $scope.showArrestDetailsForm = function(e) {
                e.preventDefault();
                $('.arrestFormHolder').show()
                $('.arrestFormHolderEdit').hide()
                $('.staticViewArrest').show();



            }

            $scope.cancelArrest = function(e) {
                e.preventDefault();
                $('.arrestFormHolder').hide()
                $('.arrestFormHolderEdit').hide()
                $('.staticViewArrest').show();

            }

            $scope.arrest = {}

            $scope.arrest.editMode = false;

            // populates fileds with data to allow editing

            $scope.editArrest = function(_index) {

                $scope.arrestDetailsEdit = {}

                $scope.arrest.editMode = true;

                $('.staticViewArrest').hide();
                $('.arrestFormHolderEdit').show();
                $('.arrestFormHolder').hide()



                var arrest = $scope.current.arrests[_index]


                if (arrest.arrest_year_fa) {
                    $scope.date.doa = {
                        day_j: {
                            text: arrest.arrest_day_fa,
                            value: arrest.arrest_day_fa
                        },
                        month_j: {
                            text: arrest.arrest_month_fa,
                            value: arrest.arrest_month_fa
                        },
                        year_j: {
                            text: arrest.arrest_year_fa,
                            value: arrest.arrest_year_fa
                        }
                    }

                    $scope.onSelectDate_j('doa')
                }

                $scope.arrestDetails.domesticlawviolated_array = arrest.domestic_law_violated_objs
                $scope.arrestDetails.domestic_law_violated_ids = arrest.domestic_law_violated_ids

                $scope.arrestDetails.chargedwith_array = arrest.charged_with_objs
                $scope.arrestDetails.charged_with_ids = arrest.charged_with_ids

                $scope.arrestDetails.internationallawviolated_array = arrest.international_law_violated_objs
                $scope.arrestDetails.international_law_violated_ids = arrest.international_law_violated_ids

                $scope.arrestDetails.city = arrest.city != null ? arrest.city.name_en : null;
                $scope.arrestDetails.city_fa = arrest.city != null ? arrest.city.name_fa : null;
                $scope.arrestDetails.caseid = arrest.case_id != null ? arrest.case_id.name_en : null;
                $scope.arrestDetails.caseid_id = arrest.case_id_id

                $scope.arrestDetails.activity_persecuted_for = arrest.activity_persecuted_for
                $scope.arrestDetails.activity_persecuted_for_objs = arrest.activity_persecuted_for

                $scope.arrestDetails.secondary_activity = arrest.secondary_activity;
                $scope.arrestDetails.tertiary_activity = arrest.tertiary_activity;

                $scope.currentEditIndex = _index;
                $scope.currentEdit = arrest.id;

            }


            // set data using dropdown - Activity Persecuted For

            $scope.onSelectActivity = function() {

                $scope.arrestDetails = this.arrestDetails;
                // Why was the line below placed here? It does not seem to do anything. Commenting out for now.
                //$scope.arrestDetails.activity_persecuted_for_id = this.arrestDetails.activity_persecuted_for_objs.id;

            }


            // save arrest if the case id is not in the Database then it is added for later use on other prisonre with teh same case id.


            $scope.saveArrestDetails = function() {

                if ($scope.date.doa) {
                    $scope.arrestDetails.arrest_day = $scope.date.doa.day ? $scope.date.doa.day.value : null;
                    $scope.arrestDetails.arrest_month = $scope.date.doa.month ? $scope.date.doa.month.value : null;
                    $scope.arrestDetails.arrest_year = $scope.date.doa.year ? $scope.date.doa.year.text : null;

                    $scope.arrestDetails.arrest_day_fa = $scope.date.doa.day_j ? $scope.date.doa.day_j.value : null;
                    $scope.arrestDetails.arrest_month_fa = $scope.date.doa.month_j ? $scope.date.doa.month_j.value : null;
                    $scope.arrestDetails.arrest_year_fa = $scope.date.doa.year_j ? $scope.date.doa.year_j.text : null;
                }
                $scope.arrestDetails.prisoner_id = varID;
                $scope.arrestDetails.case_id_id = $scope.arrestDetails.caseid_id

                $scope.arrestDetails.is_published = true;

                // There is a lot to clean up here... For now we'll just delete the unnecessary.
                // We do not need to send the entire object in the POST req, since we're only concerned with the IDs.
                if ($scope.arrestDetails.activity_persecuted_for_objs) {
                    $scope.arrestDetails.activity_persecuted_for_id = $scope.arrestDetails.activity_persecuted_for_objs.id;
                    delete $scope.arrestDetails.activity_persecuted_for_objs;
                }

                if ($scope.arrestDetails.secondary_activity) {
                    $scope.arrestDetails.secondary_activity_id = $scope.arrestDetails.secondary_activity.id;
                    delete $scope.arrestDetails.secondary_activity;
                }

                if ($scope.arrestDetails.tertiary_activity) {
                    $scope.arrestDetails.tertiary_activity_id = $scope.arrestDetails.tertiary_activity.id;
                    delete $scope.arrestDetails.tertiary_activity;
                }

                if ($scope.arrestDetails.caseid_id == null) {



                    var req = {
                        method: 'POST',
                        url: '/api/prisoners/caseid/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: {
                            'name_en': $scope.arrestDetails.caseid,
                            'name_fa': $scope.arrestDetails.caseid
                        },
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }

                    $http(req).success(function(response) {


                        $scope.arrestDetails.case_id_id = response.id
                        postArrest();
                    }).error(function(error) {
                        console.log(error)
                    });
                } else {
                    $scope.arrestDetails.case_id_id = $scope.arrestDetails.caseid_id
                    postArrest();

                }
            }


            // the arrest post to the server
            // this usesed for both edit and first post

            postArrest = function() {

                if ($scope.arrest.editMode) {

                    var req = {
                        method: method,
                        url: '/api/' + idTag + 's/' + idTag + 'arrest/' + $scope.currentEdit + '/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.arrestDetails,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                } else {
                    var req = {
                        method: 'POST',
                        url: '/api/prisoners/prisonerarrest/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.arrestDetails,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {

                    updateView();
                    $scope.arrestDetailsForm.$setPristine();
                $('.arrestFormHolder').hide()
                $('.arrestFormHolderEdit').hide()
                $('.staticViewArrest').show();
                    $scope.arrestDetails = {};
                    $scope.date = {};

                }).error(function(error) {
                    console.log(error)
                });
            }



            // code for sentances


            // toggle view of each sentence for an arrest

            $scope.showSentenceForm = function(e, id) {
                e.preventDefault();
                $('.sentence').fadeOut()
                if (!$('.sentence' + id).is(':visible')) {
                    $('.sentence' + id).fadeToggle()
                }

                $scope.arrestDetails = {}
                $scope.arrestDetailsForm.$setUntouched();
                $('.staticViewArrest').show();
                $('.arrestFormHolderEdit').hide();

            }


            // pre populates each sentence

            $scope.editSentance = function(_index, arrestIndex) {

                var sentance = $scope.current.arrests[arrestIndex].sentences[_index];

                $('._sentence' + _index).toggle();
                $('.sentancesHolder' + _index + arrestIndex).toggle();

                $scope.currentEdit = sentance.id

                $scope.arrestDetails.judge = sentance.judge ? sentance.judge.surname_en : null;
                $scope.arrestDetails.judge_fa = sentance.judge ? sentance.judge.surname_fa : null;
                $scope.arrestDetails.death_penalty = sentance.death_penalty
                $scope.arrestDetails.exiled = sentance.exiled
                $scope.arrestDetails.life = sentance.life
                $scope.arrestDetails.sentence_years = sentance.sentence_years
                $scope.arrestDetails.sentence_months = sentance.sentence_months
                $scope.arrestDetails.number_of_lashes = sentance.number_of_lashes
                $scope.arrestDetails.fine = sentance.fine
                $scope.arrestDetails.social_depravation_en = sentance.social_depravation_en
                $scope.arrestDetails.social_depravation_fa = sentance.social_depravation_fa
                $scope.arrestDetails.arrest_id = $scope.current.arrests[arrestIndex].id

                $scope.arrestDetails.behaviourtype_array = [];
                $scope.arrestDetails.judgebehaviour = [];
                $scope.arrestDetails.behaviourtype_ids = [];

                angular.forEach(sentance.behaviours, function(value, key) {

                    $scope.arrestDetails.behaviourtype_array.push(value.behaviour_type)
                    $scope.arrestDetails.behaviourtype_ids.push(value.behaviour_type.id)
                    $scope.arrestDetails.judgebehaviour.push({
                        description_en: value.description_en,
                        description_fa: value.description_fa,
                        id: value.id
                    })

                })
            }



            $scope.addSentenceEdit = function() {
                $scope.arrestDetails.is_published = true;


                var req = {
                    method: method,
                    url: '/api/' + idTag + 's/' + idTag + 'sentence/' + $scope.currentEdit + '/',
                    fields: {
                        csrfmiddlewaretoken: token
                    },
                    headers: {
                        'X-CSRFToken': token
                    },
                    data: $scope.arrestDetails,
                    params: {
                        csrfmiddlewaretoken: token
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {
                    postBehaviours(response.id);
                    $('.sentenceStatic').show();
                    $('.sentenceFrom').hide();
                    updateView();


                }).error(function(error) {
                    console.log(error)
                });
            }

            $http({
                url: '/api/prisoners/activitypersecutedfor/',
                method: 'GET'
            }).success(function(data) {
                $scope.activity_persicuted = data.results;

            }).error(function(err) {
                "ERR", console.log(err)
            })

            $scope.arrestDetails = {};





            $scope.addSentence = function(this_id) {

                $scope.arrestDetails.prisoner_id = varID;
                $scope.arrestDetails.arrest_id = this_id;
                $scope.arrestDetails.is_published = true;

                var req = {
                    method: 'POST',
                    url: '/api/prisoners/prisonersentence/',
                    fields: {
                        csrfmiddlewaretoken: token
                    },
                    headers: {
                        'X-CSRFToken': token
                    },
                    data: $scope.arrestDetails,
                    params: {
                        csrfmiddlewaretoken: token
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {
                    postBehaviours(response.id);

                }).error(function(error) {
                    console.log(error)
                });


            }

            $scope.arrestDetails.judgebehaviour = {};


            $scope.deleteBehaviour = function(sid) {

                if (sid) {

                    var req = {
                        method: 'DELETE',
                        url: '/api/' + idTag + 's/sentencebehaviour/' + sid + '/',
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

                    }).error(function(error) {
                        console.log(error)
                    });
                }
            }

            postBehaviours = function(id) {

                var c = 0;

                angular.forEach($scope.arrestDetails.behaviourtype_ids, function(value, key) {

                    var behaviour = $scope.arrestDetails.judgebehaviour ? $scope.arrestDetails.judgebehaviour[key] : null;
                    var description_fa = behaviour ? behaviour.description_fa : "";
                    var description_en = behaviour ? behaviour.description_en : "";
                    var tempBehaviour = {

                        "is_published": true,
                        "sentence_id": id,
                        "description_en": description_en,
                        "description_fa": description_fa,
                        "behaviour_type_id": value
                    };

                    var behaviourID = behaviour ? behaviour.id : null;
                    var methodType = behaviourID ? 'PUT' : 'POST';
                    var idSentence = behaviourID ? behaviourID + '/' : '';



                    var req = {
                        method: methodType,
                        url: '/api/' + idTag + 's/sentencebehaviour/' + idSentence,
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: tempBehaviour,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                    $(".savingBlocker").fadeIn();
                    $http(req).success(function(response) {

                        c++
                        if (c == $scope.arrestDetails.behaviourtype_ids.length) {

                            updateView();
                            $scope.arrestDetails = {};
                            $scope.date = {};

                        }

                    }).error(function(error) {
                        console.log(error)
                    });

                });

                if ($scope.arrestDetails.behaviourtype_ids == undefined) {
                    updateView();
                    $scope.arrestDetails = {};

                }
            }

        },
        templateUrl: ipa.staticPrefix + 'ui/templates/arrestDetails.html'
    };
}).directive('arrestForm', function() {

    return {
        templateUrl: ipa.staticPrefix + 'ui/templates/arrestForm.html'
    };
}).directive('sentanceForm', function() {

    return {
        templateUrl: ipa.staticPrefix + 'ui/templates/sentanceForm.html'
    };
}).directive('sentanceFormEdit', function() {

    return {
        templateUrl: ipa.staticPrefix + 'ui/templates/sentanceFormEdit.html'
    };
})
