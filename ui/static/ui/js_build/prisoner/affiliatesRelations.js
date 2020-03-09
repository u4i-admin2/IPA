// affiliatesRelations.js

UFI.directive('affiliatesRelations', function() {

    return {
        controller: function($scope, $http) {

            $scope.editRelationshipMode = false;
            $scope.saveRelationship = function() {

                $scope.relationship.related_prisoner_id = $scope.relationship.prisoner_id;
                $scope.relationship.prisoner_id = varID;
                $scope.relationship.forename_en = $scope.relationship.prisoner
                $scope.relationship.forename_fa = $scope.relationship.prisoner_fa
                $scope.relationship.is_published = true;

                if ($scope.editRelationshipMode) {
                    var req = {
                        method: 'PUT',
                        url: '/api/' + idTag + 's/' + idTag + 'relationship/' + $scope.relationshipId + '/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.relationship,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                } else {
                    var req = {
                        method: 'POST',
                        url: '/api/' + idTag + 's/' + idTag + 'relationship/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.relationship,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {
                    $scope.relationship = {};
                    $scope.relationshipForm.$setPristine();
                    updateView();
                    $scope.editRelationshipMode = false;

                }).error(function(error) {
                    console.log(error)
                });

            }

            $scope.editAffiliationMode = false;
            $scope.editAffiliation = function(affiliation) {

                $scope.affiliation = {}
                $scope.affiliationId = affiliation.id;

                $scope.affiliation.organisation = affiliation.organisation.name_en;
                $scope.affiliation.organisation_fa = affiliation.organisation.name_fa;
                $scope.affiliation.confirmed = affiliation.confirmed;

                $scope.editAffiliationMode = true;

            }

            $scope.cancelEditAffiliation = function(e) {
                e.preventDefault()
                $scope.affiliation = {}
                $scope.editAffiliationMode = false;


            }

            $scope.saveAffiliation = function() {


                $scope.affiliation.prisoner_id = varID;
                $scope.affiliation.is_published = true;

                $scope.affiliation.relationship_type_id = 1;
                if ($scope.editAffiliationMode) {
                    var req = {
                        method: 'PUT',
                        url: '/api/' + idTag + 's/' + idTag + 'affiliation/' + $scope.affiliationId + '/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.affiliation,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                } else {

                    var req = {
                        method: 'POST',
                        url: '/api/' + idTag + 's/' + idTag + 'affiliation/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.affiliation,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {
                    $scope.affiliation = {};
                    $scope.affiliationForm.$setPristine();
                    updateView();
                    $scope.editAffiliationMode = false;

                }).error(function(error) {
                    console.log(error)
                });
            }

            $scope.cancelEditRelationship = function(e) {
                e.preventDefault()
                $scope.relationship = {}
                $scope.editRelationshipMode = false;

            }

            $scope.editRelationshipMode = false;

            $scope.editRelationship = function(r) {

                $scope.editRelationshipMode = true;

                $scope.relationship = {}
                $scope.relationshipId = r.id;
                $scope.relationship.prisoner = r.related_prisoner.surname_en;
                $scope.relationship.prisoner_fa = r.related_prisoner.surname_fa;
                $scope.relationship.relationship_type_id = r.relationship_type.id;
                $scope.relationship.is_confirmed = r.is_confirmed;
            }
        },
        templateUrl: ipa.staticPrefix + 'ui/templates/affiliatesRelations.html'
    };
})
