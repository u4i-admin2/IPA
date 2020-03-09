// supportingEvidence.js

UFI.directive('supportingEvidence', function() {
    return {
        controller: function($scope, $http , $timeout , $upload) {


            $scope.upload = function(files) {

                if (files && files.length && $scope.readyforuploiad) {

                    for (var i = 0; i < files.length; i++) {
                        $(".savingBlocker").fadeIn();
                        var file = files[i];
                        $(".savingBlocker").fadeIn();
                        $upload.upload({
                            method: "PATCH",
                            headers: {
                                'X-CSRFToken': token
                            },
                            url: '/api/' + idTag + 's/' + idTag + 'file/' + $(".mmm").html() + "/",
                            fields: {
                                csrfmiddlewaretoken: token,
                                "description_en": $scope.supportingEvidence.description_en,
                                "description_fa": $scope.supportingEvidence.description_fa
                            },
                            file: file,
                            fileFormDataName: "file_thumb"

                        }).progress(function(evt) {
                            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);

                            $(".fillUp").width((progressPercentage / 2) + 50 + "%");
                        }).success(function(data, status, headers, config) {
                            updateView();
                            $scope.supportingEvidence = {}
                            $scope.files = null
                            $scope.files2 = null
                            $scope.fileUpload.$setPristine();
                            $scope.selectedFileIcon = false;
                            $scope.uploading = false;
                            $('#saveFile').removeClass('disabled')
                            $('#saveFile').html('Save File');
                            $scope.readyforuploiad = false

                        });
                    }
                } else {
                    if ($(".mmm").html() != '') {
                        $(".savingBlocker").fadeIn();
                        var req = {
                            method: 'PATCH',
                            url: '/api/' + idTag + 's/' + idTag + 'file/' + $(".mmm").html() + "/",
                            fields: {
                                csrfmiddlewaretoken: token
                            },
                            headers: {
                                'X-CSRFToken': token
                            },
                            data: {
                                "description_en": $scope.supportingEvidence.description_en,
                                "description_fa": $scope.supportingEvidence.description_fa
                            },
                            params: {
                                csrfmiddlewaretoken: token
                            }
                        }
                        $(".savingBlocker").fadeIn();
                        $http(req).success(function(response) {

                            $(".fillUp").width((100 / 2) + 50 + "%");
                            updateView();
                            $scope.supportingEvidence = {}
                            $scope.files = null
                            $scope.files2 = null
                            $scope.fileUpload.$setPristine();
                            $scope.selectedFileIcon = false;
                            $scope.uploading = false;
                            $('#saveFile').removeClass('disabled')
                            $('#saveFile').html('Save File');
                            $scope.readyforuploiad = false;

                        }).error(function(error) {
                            console.log(error)
                        });


                    }
                }
            };
            $scope.fileArray = []

            $scope.uploading = false;

            $scope.addFile = function(e) {

                if (!$scope.uploading) {
                    $scope.uploading = true;
                    $('#saveFile').addClass('disabled')
                    $('#saveFile').html('Uploading');
                    $scope.submitFile($scope.files);
                }

            };

            $scope.clickUpload = function(e) {
                e.preventDefault()
                $timeout(function() {
                    angular.element('#selectFile').trigger('click');
                }, 100);


            }

            $scope.submitFileUploads = function(e) {
                e.preventDefault()
                $timeout(function() {
                    angular.element('#addEvidence').trigger('click');
                }, 100);
            }

            $scope.showIcon = function(e) {


                var preview = document.querySelector('img');
                var file = e.target.files[0];
                var reader = new FileReader();

                reader.onloadend = function() {

                    var thumb = $('.previewThumb');

                    thumb.attr('src', reader.result);
                    var thumbW = thumb.width();
                    var thumbH = thumb.height();
                    if (thumbW < thumbH) {

                        thumb.width(75)
                    } else {
                        thumb.height(75)
                    }

                }
                if (file) {
                    reader.readAsDataURL(file)
                }


            }

            $scope.removeClass = function(e) {

                e.preventDefault()

                $scope.supportingEvidence.name_en = e.target.value.replace("C:\\fakepath\\", " ");
                $scope.supportingEvidence.name_fa = e.target.value.replace("C:\\fakepath\\", " ");
                $scope.selectedFileIcon = true;

            }

            $scope.selectedFileIcon = false;
            $scope.readyforuploiad = false;


            $scope.submitFile = function(files) {


                if (files && files.length) {

                    for (var i = 0; i < files.length; i++) {
                        var file = files[i];
                        $(".savingBlocker").fadeIn();
                        $upload.upload({
                            method: 'POST',
                            url: '/api/' + idTag + 's/' + idTag + 'file/',
                            headers: {
                                'X-CSRFToken': token
                            },
                            fields: {
                                csrfmiddlewaretoken: token,
                                "name_en": $scope.supportingEvidence.name_en,
                                "name_fa": $scope.supportingEvidence.name_fa,
                                "judge_id": varID,
                                "prison_id": varID,
                                "prisoner_id": varID,
                                "file_type": $scope.supportingEvidence.typeOfFile,
                                "is_published": true,
                            },
                            file: file
                        }).progress(function(evt) {
                            var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);
                            $(".fillUp").width((progressPercentage / 2) + "%");

                        }).success(function(data, status, headers, config) {


                            $(".mmm").html(data.id)
                            $scope.readyforuploiad = true;
                            $scope.$$postDigest(function() {

                                $('#addEvidencePhoto').click()

                            });



                        });
                    }
                }
            };




            $scope.editQuoteStatus = false;
            $scope.quoteId = null;
            $scope.supportingEvidence = {}

            $scope.editQuote = function(i, q) {

                $scope.editQuoteStatus = true;
                $scope.quoteId = q;
                $scope.supportingEvidence.quote_en = $scope.current.quotes[i].quote_en
                $scope.supportingEvidence.quote_fa = $scope.current.quotes[i].quote_fa
                $scope.supportingEvidence.source_name_en = $scope.current.quotes[i].name_en
                $scope.supportingEvidence.source_name_fa = $scope.current.quotes[i].name_fa
                $scope.supportingEvidence.source = $scope.current.quotes[i].source

            }
            $scope.cancelEditQuote = function(e) {
                e.preventDefault();
                $scope.editQuoteStatus = false;
            }

            $scope.addQuote = function() {

                $scope.quoteVars = {
                    "quote_en": $scope.supportingEvidence.quote_en,
                    "quote_fa": $scope.supportingEvidence.quote_fa,
                    "name_en": $scope.supportingEvidence.source_name_en,
                    "name_fa": $scope.supportingEvidence.source_name_fa,
                    "source": $scope.supportingEvidence.source,
                    "judge_id": varID,
                    "prison_id": varID,
                    "prisoner_id": varID,
                    "is_published": true,
                }

                if ($scope.editQuoteStatus) {
                    var req = {
                        method: 'PUT',
                        url: '/api/' + idTag + 's/' + idTag + 'quote/' + $scope.quoteId + '/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.quoteVars,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                } else {

                    var req = {
                        method: 'POST',
                        url: '/api/' + idTag + 's/' + idTag + 'quote/',
                        fields: {
                            csrfmiddlewaretoken: token
                        },
                        headers: {
                            'X-CSRFToken': token
                        },
                        data: $scope.quoteVars,
                        params: {
                            csrfmiddlewaretoken: token
                        }
                    }
                }
                $(".savingBlocker").fadeIn();
                $http(req).success(function(response) {

                    $scope.editQuoteStatus = false;
                    $scope.supportingEvidence = {}
                    $scope.quote.$setPristine();
                    updateView()

                }).error(function(error) {
                    console.log(error)
                });

            }

        },
        templateUrl: ipa.staticPrefix + 'ui/templates/supportingEvidence.html'
    };
})
