// base js

// set app up

ipa.isMobile = false; //initiate as false
// device detection
/* cSpell:disable */
if (/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|ipad|iris|kindle|Android|Silk|lge |maemo|midp|mmp|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(navigator.userAgent) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(navigator.userAgent.substr(0, 4))) {
    ipa.isMobile = true;


    $(".toolTipHolder").remove();
}
/* cSpell:enable */

ipa.colorsRange = [
    'rgb(0, 93, 117)',
    'rgb(0, 135, 62)',
    'rgb(195, 68, 36)',
    'rgb(78, 68, 110)',
    'rgb(243, 128, 0)',

    'rgb(42, 158, 187)',
    'rgb(86, 192, 135)',
    'rgb(234, 111, 79)',
    'rgb(147, 134, 188)',
    'rgb(255, 181, 99)',

    'rgb(152, 221, 238)',
    'rgb(156, 255, 202)',
    'rgb(255, 178, 158)',
    'rgb(206, 195, 242)',
    'rgb(255, 217, 174)',
];

var _searching = true;

var UFIF = angular
  .module(
    'UFIF',
    [
      'rzModule',
      'angularUtils.directives.dirPagination'
    ]
  )
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
  .run(
    function($rootScope) {
        $rootScope.ipa = ipa;
    }
  );

var smallmedia = {};

var onOffSearch = false;

UFIF.controller('quicksearch', function($scope) {
    $scope.quickSearchJudges = [];
    $scope.quickSearchPrisoners = [];
    $scope.quickSearchPrisons = [];
    $scope.quickSearchText = "";

    angular.forEach(quickSearch.judges, function(v, k) {
        $scope.quickSearchJudges.push({
            'name': v,
            'id': k
        });
    });

    angular.forEach(quickSearch.prisons, function(v, k) {
        $scope.quickSearchPrisons.push({
            'name': v,
            'id': k
        });
    });

    if (ipa.site === 'ipa') {
        angular.forEach(quickSearch.prisoners, function(v, k) {
            $scope.quickSearchPrisoners.push({
                'name': v,
                'id': k
            });
        });
    }

    $scope.limit = 4;

    $('.quicksearch').focusin(function() {
        $(".advanceBtn").slideDown();
        $(this).addClass("searching");
        $(".searchGo").addClass("searching");
        onOffSearch = true;
    });

    // GH 2019-09-03: Disabled since advanced search link is now visible at all times
    // $(document).mouseup(function(e) {
    //     var container = $(".js-quickSearchHolder");
    //     console.log($scope.quickSearchText.length);

    //     if (!container.is(e.target) && container.has(e.target).length === 0 && $scope.quickSearchText.length === 0) // ... nor a descendant of the container
    //     {
    //         $(".advanceBtn").slideUp();
    //         $('.quicksearch').removeClass("searching");
    //         $(".searchGo").removeClass("searching");
    //         onOffSearch = false;
    //     }
    // });
});


function capsFirstLetter(str) {

    str = str.toLowerCase().replace(/([^a-z]|^)([a-z])(?=[a-z]{2})/g, function(_, g1, g2) {
        return g1 + g2.toUpperCase();
    });


    return str;

}



$(document).on('tap', '.menu', function() {
    $('.mmm').toggle();
    $('.ccc').toggle();
    $('.dropDown').slideToggle();

});

// ===================
// === NavHeaderCC ===
// ===================

function NavHeaderCC(element) {
    /** @type {HTMLElement} */
    this.element = element;

    this.init();
}

NavHeaderCC.prototype.init = function () {
    this.mobileMenuIsOpen = false;

    /** @type {HTMLAnchorElement} */
    this.menuToggleElement = this.element.querySelector('.jsMenuToggle');

    this.menuToggleElement.addEventListener(
        'click',
        this.onMenuToggleClick.bind(this),
        false
    );
};

NavHeaderCC.prototype.onMenuToggleClick = function () {
    if (this.mobileMenuIsOpen) {
        this.element.classList.remove('mobileMenuIsOpen');
        this.mobileMenuIsOpen = false;
    } else {
        this.element.classList.add('mobileMenuIsOpen');
        this.mobileMenuIsOpen = true;
    }
};


$(document).ready(function() {
    var navHeaderElement = document.querySelector('.NavHeaderC');

    if (navHeaderElement instanceof HTMLElement) {
        new NavHeaderCC(navHeaderElement);
    }

    responsiveHelper();

    if (wH < wW) {
        $(".slideUp1").css("top", wH - ifMobile);
        $(".slideUp2").css("top", -wH + ifMobile);
        setTimeout(function() {
            $(".slideUp1").animate({
                top: 0
            }, 1000, function() {
                // Animation complete.
            });

            $(".slideUp2").animate({
                top: 0
            }, 1000, function() {
                $(".clickHover").css("opacity", 1);
            });
        }, 5000);
    } else {
        $(".slideUp1").css("left", wW);
        $(".slideUp2").css("left", -wW);
        setTimeout(function() {
            $(".slideUp1").animate({
                left: 0
            }, 1000, function() {
                // Animation complete.
            });

            $(".slideUp2").animate({
                left: 0
            }, 1000, function() {
                $(".clickHover").css("opacity", 1);
            });
        }, 7500);

    }



});

setTimeout(function() {
    thumb = $('.profileImage');
    thumbW = thumb.width();
    thumbH = thumb.height();
    profilePic();
    thumb.show();

}, 300);



$(window).resize(function() {
    responsiveHelper();
});

var thumb = $('.profileImage');
var thumbW;
var thumbH;

function profilePic() {
    var width = $(".imageHolder").width();
    $(".imageHolder").height(width);

    if (thumb.width() < thumb.height()) {
        thumb.addClass('taller');
    } else {
        thumb.addClass('wider');
    }


}
setTimeout(function() {
    $(".clickHover").css("opacity", 1);

    if (!ipa.isMobile) {

        $(document).on("mouseover", ".slideUp", function() {

            var h = $(this).children(".clickHover").height() + 60;

            $(this).stop();
            if (wH < wW) {
                $(this).animate({
                    top: -h
                }, 300, function() {
                    // Animation complete.
                });
            } else {
                $(this).animate({
                    left: -300
                }, 300, function() {
                    // Animation complete.
                });

            }

        });

        $(document).on("mouseout", ".slideUp", function() {



            $(this).stop();
            if (wH < wW) {
                $(this).animate({
                    top: 0

                }, 300, function() {
                    // Animation complete.
                });
            } else {
                $(this).animate({

                    left: 0
                }, 300, function() {
                    // Animation complete.
                });
            }

        });

    }

}, 8500);

$(".searchGo").click(function() {
    _searching = false;
    if (onOffSearch) {
        $(".advanceBtn").slideUp();
        $('.quicksearch').removeClass("searching");
        $(".searchGo").removeClass("searching");
        onOffSearch = false;
        _searching = true;
    }
    $(".menuHider").toggleClass("hideMe");
    $(".quicksearch").toggleClass("open");
    $(".js-quickSearchHolder").toggleClass("open");
    $(this).toggleClass("open");
    $(this).removeClass("searching");
    $(".quicksearch").removeClass("searching");
    $(".quicksearch").val("");

    var scope = angular.element($(".quicksearch")).scope();
    scope.$apply(function() {
        scope.quickSearchText = "";
    });

    if (!onOffSearch) {
        $(".quicksearch").focus();
    }
});


var wH,
    wW,
    ifMobile;


function responsiveHelper() {

    _file = $('.file');
    fileHover = $('.fileHover');
    _fileW = _file.width();
    _file.height(_fileW);
    fileHover.width(_fileW - 20);
    fileHover.height(_fileW - 20);
    profilePic();

    wH = $(window).height();
    wW = $(window).width();



    var l = (wW - $(".homeNave").width()) / 2;

    var introRow = $(".introRow");

    ifMobile = wW < 1025 ? 60 : 0;
    splashScreen = $(".splashScreen");
    splashScreen.height(wH);







    if (wH < wW) {

        $(".introMenu").height(wH - ifMobile);
        $(".introRow").height(wH - ifMobile);
        $(".menubackdrop").height(wH - ifMobile);
        $(".menubackdrop").width("");
        $(".slideUp").css("left", "");
        $(".slideUp").css("top", 0);

        splashScreen.addClass("landscape");
        splashScreen.removeClass("portrait");

        introRow.addClass("landscape");
        introRow.removeClass("portrait");

    } else {

        $(".introRow").height(wH - ifMobile);
        $(".menubackdrop").width(wW);
        $(".menubackdrop").height("");
        $(".introMenu").height("");
        $(".slideUp").css("left", 0);
        $(".slideUp").css("top", "");

        splashScreen.removeClass("landscape");
        splashScreen.addClass("portrait");

        introRow.removeClass("landscape");
        introRow.addClass("portrait");
    }

    matcher(".matcher");
    matcher("._matcher");
}





$('.pageTop').on('tap', function() {
    $("html, body").animate({ scrollTop: "0px" });

});



function matcher(_class) {
    setTimeout(function() {
        $(_class).removeAttr('style');
        var allH = [];
        $(_class).each(function() {
            allH.push($(this).height());
        });
        allH.sort(function(a, b) {
            return b - a;
        });
        $(_class).each(function() {
            $(this).css("height", allH[0]);
        });
    }, 1);
}


function traverse(el) {
    var persian = {
        0: '۰',
        1: '۱',
        2: '۲',
        3: '۳',
        4: '۴',
        5: '۵',
        6: '۶',
        7: '۷',
        8: '۸',
        9: '۹'
    };

    var list = el.match(/[0-9]/g);
    console.log(persian);
    if (list !== null && list.length !== 0) {
        for (var i = 0; i < list.length; i++)
            el = el.replace(list[i], persian[list[i]]);
    }

    return el;


}
