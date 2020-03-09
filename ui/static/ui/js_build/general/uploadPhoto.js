// uploadPhoto.js


UFI.controller('uploadPhoto', function($scope, $upload, $http, $timeout) {

    $scope.form = [];
    $scope.picture = null;


    $scope.judge = [];

    $scope.deletePhoto = function() {
        var req = {
            method: 'PUT',
            url: '/api/' + idTag + 's/' + idTag + '/' + id,
            fields: {
                csrfmiddlewaretoken: token
            },
            headers: {
                'X-CSRFToken': token
            },
            params: {
                csrfmiddlewaretoken: token
            },
            data: {
                picture: null
            }
        }

        $http(req).success(function(response) {

            $http({
                url: '/api/' + idTag + 's/' + idTag + '/' + id,
                method: 'GET'
            }).success(function(data) {

                $scope.current = data;


                profilePic()
                setTimeout(function() {
                    profilePic()
                }, 1200);
                setTimeout(function() {
                    profilePic()
                }, 5200);



            })


        }).error(function(error) {
            console.log(error)
        })

    }

    $http({
        url: '/api/' + idTag + 's/' + idTag + '/' + id,
        method: 'GET'
    }).success(function(data) {
        $scope.current = data;

        profilePic()
        setTimeout(function() {
            profilePic()
        }, 1200);
        setTimeout(function() {
            profilePic()
        }, 5200);

    })

    function profilePic() {
        var thumb = $('.profilePic');
        var thumbW = thumb.width();
        var thumbH = thumb.height();
        if (thumbW < thumbH) {

            thumb.width(115)
        } else {
            thumb.height(115)
        }
    }


    $scope.submitForm = function() {

        $scope.upload($scope.files);
    };

    $scope.upload = function(files) {
        var errDiv = $('#uploadError');
        errDiv.hide();

        if (files && files.length) {
            for (var i = 0; i < files.length; i++) {
                var file = files[i];

                if (!/^[0-9A-Za-z\-\_\.]+$/.test(file.name)) {
                    var errMsg = 'The file name "' + file.name + '" is ' +
                                  'invalid.<br/>Please ensure that the ' +
                                  'image name consists of letters, numbers, ' +
                                  'periods, dashes, and underscores only.' +
                                  '<br/><br/>' + 'نام انتخابی "' + file.name +
                                  '" معتبر نیست.<br/>لطفا مطمئن شوید که نام ' +
                                  'تصویر فقط ترکیبی از حروف، اعداد، نقطه و ' +
                                  'یا خط تیره باشد.';
                    errDiv.html(errMsg);
                    errDiv.show();
                    continue;
                }

                $upload.upload({
                    url: '/api/' + idTag + 's/pictures/' + id,
                    fields: {
                        csrfmiddlewaretoken: token
                    },
                    file: file
                }).progress(function(evt) {
                    var progressPercentage = parseInt(100.0 * evt.loaded / evt.total);

                }).success(function(data, status, headers, config) {

                    $scope.current.picture_resized = data.url
                    setTimeout(function() {
                        profilePic()
                    }, 1200);
                });
            }
        }
    };


})
