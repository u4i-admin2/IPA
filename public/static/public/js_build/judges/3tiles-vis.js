// @ts-check

smallmedia.tilesVis = (function() {
    var my = {};

    var config = {
        numCols: 6,
        tilePadding: 8,
        circleVisMode: 'full'
    };

    var state = {
        selectedTile: null,
        sortCategory: (
            {
                'aea': 'total_victims',
                'ipa': 'total_verdicts',
            }[ipa.site] || null
        )
    };

    var elements = {};

    var data = {
        tiles: [],
    };

    /*-------
    CONSTRUCT
    -------*/
    /**
     * @param {Array<ipa.JudgeDataAea> | Array<ipa.JudgeDataIpa>} judgeDatas
     */
    function processTileData(judgeDatas) {
        // Convert json into array

        /** @type {Array<ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa>} */
        var judgeTileDatas = [];

        _.each(
            judgeDatas,
            /**
             * @param {ipa.JudgeDataAea | ipa.JudgeDataIpa} judgeData
             * @param {number} k
             */
            function(judgeData, k) {
                /** @type {ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa} */
                var judgeTileData = Object.assign(
                    {},
                    judgeData,
                    {
                        id: +k,
                        geometry: {},
                    }
                );

                judgeTileDatas.push(judgeTileData);
            }
        );

        return judgeTileDatas;
    }

    function construct() {
        elements.container = d3.select(config.container)
            .append('div');

        elements.circleVis = elements.container
            .append('div')
            .classed('circlevis', true)
            .style('position', 'absolute');
    }


    /*----
    UPDATE
    ----*/
    function updateGeometry() {
        config.tileWidth = config.width / config.numCols;
        config.chosenRow = null;
        if (state.selectedTile !== null) {
            config.chosenRow = Math.floor(state.selectedTile.geometry.i / config.numCols);
        }
    }

    function sortTiles() {
        data.tiles = _.sortBy(
            data.tiles,

            /** @param {ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa} judgeTileData */
            function(judgeTileData) {
                var val = 0;

                if (_.has(judgeTileData, 'stats')) {
                    val = judgeTileData.stats[state.sortCategory];
                    if (isNaN(val))
                        val = 0;
                    else
                        val = +val;
                }

                return -val;
            }
        );
    }

    function layoutTiles() {
        _.each(
            data.tiles,
            /**
             * @param {ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa} judgeTileData
             * @param {number} k
             */
            function(judgeTileData, i) {
                judgeTileData.geometry.i = i;
                judgeTileData.geometry.x = (i % config.numCols) * config.tileWidth;

                var row = Math.floor(i / config.numCols);
                judgeTileData.geometry.y = row * config.tileWidth;
                if (config.chosenRow !== null && row > config.chosenRow) {
                    judgeTileData.geometry.y += config.circleVisHeight;
                }
            }
        );
    }

    function updateTiles() {
        var u = elements.container
            .selectAll('div.tile')
            .data(
                data.tiles,
                /** @param {ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa} judgeTileData */
                function(judgeTileData) {
                    return judgeTileData.id;
                }
            );

        var enteringTiles = u.enter()
            .append('div')
            .classed('tile', true)
            .style('width', config.tileWidth + 'px')
            .style('height', config.tileWidth + 'px')
            .style('position', 'absolute');

        if (ipa.site === 'aea') {
            enteringTiles = enteringTiles
                .append('a')
                .attr(
                    'href',
                    /** @param {ipa.JudgeTileDataAea} judgeTileData */
                    function(judgeTileData) {
                        return ('/' + ipa.lang + '/judge/' + judgeTileData.id);
                    }
                );
        } else if (ipa.site === 'ipa') {
            enteringTiles = enteringTiles
                .append('div');
        }

        enteringTiles
            .classed('inner', true)
            .style({
                'position': 'absolute',
                // 'font-size': '20px',
                'background-size': '100%',
                // 'background-color': '#eee',
                'cursor': 'pointer'
            })
            .style(
                'background-image',
                /** @param {ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa} judgeTileData */
                function(judgeTileData) {
                    var picture = (
                        judgeTileData.picture_url
                            ? judgeTileData.picture_url // jshint ignore:line
                            : ipa.staticPrefix + "public/img/judge_bw.png?v=2019-08-28"
                    );
                    return 'url("' + picture + '")';
                }
            );

        if (ipa.site === 'ipa') {
            enteringTiles = enteringTiles.on('click', tileClick);
        }

        u.exit().remove();

        u
            .classed(
                'selected',
                /** @param {ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa} judgeTileData */
                function(judgeTileData) {
                    if (d3.select(this).attr("class").indexOf("selected") >= 0)
                        return true;

                    if (state.selectedTile === null)
                        return false;
                    return judgeTileData.id === state.selectedTile.id;
                }
            )
            .transition()
            .style(
                'top',
                /** @param {ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa} judgeTileData */
                function(judgeTileData) {
                    return judgeTileData.geometry.y + 'px';
                }
            )
            .style(
                'left',
                /** @param {ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa} judgeTileData */
                function(judgeTileData) {
                    return judgeTileData.geometry.x + 'px';
                }
            );

        u
            .select('.inner')
            .html(
                /** @param {ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa} judgeTileData */
                function(judgeTileData) {
                    var ret = '';
                    ret += '<div class="tilesvis-tint"></div>';
                    ret += '<div class="tilesvis-info">';
                    ret += '<div class="tilesvis-info-tint"></div>';

                    if (_.has(judgeTileData, 'stats')) {
                        ret += '<div class="tilesvis-value">' + judgeTileData.stats[state.sortCategory] + '</div>';
                    }

                    ret += '<div class="tilesvis-surname">' + judgeTileData.surname + '</div>';
                    ret += '</div>';

                    return ret;
                }
            )
            .style({
                'width': (config.tileWidth - 2 * config.tilePadding) + 'px',
                'height': (config.tileWidth - 2 * config.tilePadding) + 'px',
                'position': 'absolute',
                'top': config.tilePadding + 'px',
                'left': config.tilePadding + 'px'
            });

        // Font sizes
        u.select('.inner .tilesvis-value')
            .style('font-size', config.tileWidth * 0.15 + 'px');
        u.select('.inner .tilesvis-surname')
            .style('font-size', config.tileWidth * 0.08 + 'px');
    }

    function update() {
        updateGeometry();
        sortTiles();
        layoutTiles();
        updateTiles();

        var CV = 0;

        if ($('.circlevis:visible').length !== 0) {
            CV = $(".circlevis").height();
        }

        $(".tiles-container").height(
            (
                $(".tile").height() * Math.ceil($(".tile").length / visNumCols)
            ) +
            CV
        );


        elements.circleVis
            .style('top', (config.chosenRow + 1) * config.tileWidth + 'px');
    }


    /*----
    EVENTS
    ----*/
    /**
     *
     * @param {ipa.JudgeTileDataAea | ipa.JudgeTileDataIpa} judgeTileData
     */
    function tileClick(judgeTileData) {
        $(".tile").removeClass("selected");

        if (state.selectedTile !== null && judgeTileData.id === state.selectedTile.id) {
            state.selectedTile = null;
            smallmedia.circleVis.setSelectedJudge(null);
            smallmedia.circleVis.update();
            update();
            return;
        }

        smallmedia.circleVis.setSelectedJudge(judgeTileData);
        smallmedia.circleVis.update();

        // Not an ideal way of doing this. Alternative is to use a mediator.
        var newWidth = $('.tiles-container').width();

        state.selectedTile = judgeTileData;
        smallmedia.tilesVis.setWidth(newWidth);
        update();
    }


    /*-
    API
    -*/
    /**
     * @param {object} conf
     */
    my.init = function(conf) {
        config = _.extend(config, conf);

        data.tiles = processTileData(config.tilesData);
        construct();

        smallmedia.circleVis.init({
            container: elements.circleVis,
            judgesProfileUrl: config.judgesProfileUrl,
            judgesAllPrisonersUrl: config.judgesAllPrisonersUrl,
            enSentencesUrl: config.enSentencesUrl,
            faSentencesUrl: config.faSentencesUrl,
            maxBiographyLength: config.maxBiographyLength
        });
    };

    /**
     * @param {number} width
     */
    my.setWidth = function(width) {
        config.width = width;
        smallmedia.circleVis.setWidth(width);
    };

    /**
     * @param {number} cols
     */
    my.setNumberOfCols = function(cols) {
        config.numCols = cols;
    };

    /**
     * @param {string} cat
     */
    my.setSortCategory = function(cat) {
        state.sortCategory = cat;
    };

    my.clearSelectedTile = function() {
        state.selectedTile = null;
        smallmedia.circleVis.setSelectedJudge(null);
    };

    /** @param {ipa.JudgesCircleVisMode} mode */
    my.setCircleVisMode = function(mode) {
        config.circleVisMode = mode;
        config.circleVisHeight = smallmedia.circleVis.getHeightFromMode(mode);

        smallmedia.circleVis.setMode(mode);
    };

    /** @param {number} px */
    my.setCircleVisInfoFontSize = function(px) {
        smallmedia.circleVis.setInfoFontSize(px);
    };

    /** @param {number} chars */
    my.setMaxBiographyLength = function(chars) {
        smallmedia.circleVis.setMaxBiographyLength(chars);
    };

    my.update = function() {
        update();
        smallmedia.circleVis.update();
    };

    return my;
}());
