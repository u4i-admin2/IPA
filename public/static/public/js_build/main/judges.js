// @ts-check

var tilesJson = tilesJson;
var visNumCols = 3;

(function() {
    "use strict";

    // This is a demo of a responsive implementation of the tiles/circles vis.

    // There are two main components: tilesMenu and tilesVis.

    // tilesMenu handles the main menu (with the 6 categories)
    // tilesVis handles the tiles vis, including the opening up to reveal the judge panel + circle vis

    // In general the usage is:

    // initialise the component
    // set parameters (such as width), then call update()

    // the last step can be repeated over and over


    // So for responsiveness, the pattern is something like:

    // function onResize() {
    //   get new viewport width
    //
    //   set width of menu
    //   call tilesMenu.update()
    //
    //   set width of tilesVis
    //   possibly set number of columns of tilesVis
    //   call tilesVis.update()
    // }

    // this gives you a degree of flexibility as to how you'd like the tiles and circular vis to respond on resize events

    // See the selectLanguage function for an example of how to switch language

    // See js/tiles-vis-language.js for the translation tables

    /**
     * Menu event handler
     *
     * @param {{category: string, label: string}} menuItem
     */
    function handleMenuClick(menuItem) {
        smallmedia.tilesVis.clearSelectedTile();
        smallmedia.tilesVis.setSortCategory(menuItem.category);
        smallmedia.tilesVis.update();
    }

    // Handle responsiveness
    // This is just for demonstration, but feel free to use/refactor
    function setUpResizeTimer() {
        var resizeTimer;

        window.onresize = function(event) {
            clearTimeout(resizeTimer);
            resizeTimer = setTimeout(updateSizes, 200);
        };
    }

    visNumCols = 3;

    // This function updates widths etc. of the tile visualisation and should be called if the page resizes
    // You can put your own logic in here e.g. you can decide on how many columns of tiles should be displayed
    function updateSizes() {
        var newWidth = $('.tiles-container').width();
        // Update tiles
        smallmedia.tilesVis.setWidth(newWidth);

        /** @type {ipa.JudgesCircleVisMode} */
        var circleVisMode = 'phone';
        var circleVisFontSize = 12; // Font size of the info panel next to the circle vis
        var maxBiographyLength = 1000;

        if (newWidth >= 1464) {
            visNumCols = 6;
            circleVisMode = 'desktop-large';
            circleVisFontSize = 18;
        } else if (newWidth >= 1128) {
            visNumCols = 6;
            circleVisMode = 'desktop-small';
            circleVisFontSize = 18;
        } else if (newWidth >= 768) {
            visNumCols = 5;
            circleVisMode = 'tablet-landscape';
            circleVisFontSize = 14;
        } else if (newWidth >= 480) {
            visNumCols = 4;
            circleVisMode = 'tablet-portrait';
            circleVisFontSize = 14;
        }



        // Calculate biography maximum lengths
        if (newWidth >= 1464) {} else if (newWidth >= 1300) {
            maxBiographyLength = 200;
        } else if (newWidth >= 1128) {
            maxBiographyLength = 200;
        } else if (newWidth >= 1000) {
            maxBiographyLength = 200;
        } else if (newWidth >= 900) {
            maxBiographyLength = 200;
        } else if (newWidth >= 840) {
            maxBiographyLength = 200;
        } else if (newWidth >= 768) {
            maxBiographyLength = 200;
        } else if (newWidth >= 480) {
            maxBiographyLength = 200;
        } else {
            maxBiographyLength = 200;
        }
        // else if(newWidth >= 1200) {
        //   maxBiographyLength = 400;
        // };

        // console.log(newWidth, maxBiographyLength);

        smallmedia.tilesVis.setNumberOfCols(visNumCols);
        smallmedia.tilesVis.setCircleVisMode(circleVisMode);
        smallmedia.tilesVis.setCircleVisInfoFontSize(circleVisFontSize);
        smallmedia.tilesVis.setMaxBiographyLength(maxBiographyLength);

        smallmedia.tilesVis.update();

        var CV = 0;

        if ($('.circlevis:visible').length !== 0) {

            CV = $(".circlevis").height();
        }

        // GH 2019-09-27: Commented out since the exact same code is in 3tiles-vis.js’s update() function
        // $(".tiles-container").height($(".inner").height() * ((Math.ceil($(".tile").length / visNumCols) + 1)) + 100 + CV + $("footer").height());
    }

    UFIF.controller('judges', function($scope, $location) {
        $scope.url = $location.absUrl();
        // Set language

        console.log(ipa.lang);
        smallmedia.tilesVisLanguage.setLanguage(ipa.lang);

        // Initialise menu
        smallmedia.tilesMenu.init({
            container: '.tiles-menu',
            click: handleMenuClick
        });

        // Initialise tiles visualisation
        smallmedia.tilesVis.init({
            container: '.tiles-container',
            language: ipa.lang,
            tilesData: tilesJson,

            // URL to judge's profile page
            judgesProfileUrl: '../judge/<%= id %>', // I'm guessing these!

            // URL to all prisoner's of a judge
            judgesAllPrisonersUrl: '/' + ipa.lang + '/search/#/?data=prisoners&all_sentences_judges=', // I'm guessing these!

            // API endpoint for getting the sentences of a particular judge
            enSentencesUrl: '/en/judge/<%= id %>/sentences/',
            faSentencesUrl: '/fa/judge/<%= id %>/sentences/'
        });

        updateSizes();
        setUpResizeTimer();
    });
}());
