smallmedia.circleVis = (function() {
    var my = {};

    var TWO_PI = 2 * Math.PI;

    var config = {
        width: null,
        aboutPadding: 15,
        vis: {
            numCols: 24,
            rowHeight: 40
        },
        maxBiographyLength: 450
    };

    var state = {
        selectedJudge: null,
        hoveredCategory: null
    };

    var elements = {};

    var geometry = {}; // derived values

    var heightFromMode = {
        'closed': 0,
        'phone': 350,
        'tablet-portrait': 300,
        'tablet-landscape': 450,
        'desktop-small': 500,
        'desktop-large': 660
    };

    var templateFromMode = {
        'closed': closedTemplate,
        'phone': phoneTemplate,
        'tablet-portrait': tabletTemplate,
        'tablet-landscape': fullTemplate,
        'desktop-small': fullTemplate,
        'desktop-large': fullTemplate
    };

    var classFromMode = function(d) {
        return d;
    };

    var iconSvg = {
        cross: 'M10.4,0.8l-2.9,3l-3-2.9c-1.1-1-2.7-1-3.8,0.1C0.3,1.5,0,2.2,0,2.9c0,0.7,0.3,1.4,0.8,1.9l3,2.9l-2.9,3c-0.5,0.5-0.8,1.2-0.7,1.9c0,0.7,0.3,1.4,0.8,1.9c0.5,0.5,1.2,0.8,1.9,0.8c0.7,0,1.4-0.3,1.9-0.8l2.9-3l3,2.9c1.1,1,2.7,1,3.8-0.1c0.5-0.5,0.8-1.2,0.7-1.9c0-0.7-0.3-1.4-0.8-1.9l-3-2.9l2.9-3C14.7,4,15,3.3,15,2.6c0-0.7-0.3-1.4-0.8-1.9C13.6,0.3,13,0,12.3,0C11.6,0,10.9,0.3,10.4,0.8z',
        diagonal: 'M11.4,7.7l3-3.1c0.5-0.5,0.8-1.2,0.8-1.9s-0.3-1.4-0.8-1.9C13.8,0.3,13.1,0,12.4,0c-0.7,0-1.4,0.3-1.9,0.8l-3,3.1L3.7,7.8l-3,3.1C0.3,11.4,0,12.1,0,12.8c0,0.7,0.3,1.4,0.8,1.9c0.5,0.5,1.2,0.8,1.9,0.8c0.7,0,1.4-0.3,1.9-0.8l3-3.1L11.4,7.7z',
        dash: 'M12.6,5.5l4.3,0c0.7,0,1.4-0.3,1.9-0.8s0.8-1.2,0.8-2c0-0.7-0.3-1.4-0.8-1.9c-0.5-0.5-1.2-0.8-2-0.8l-4.3,0l-5.5,0l-4.3,0C2,0.1,1.3,0.4,0.8,0.9S0,2.1,0,2.9c0,0.7,0.3,1.4,0.8,1.9c0.5,0.5,1.2,0.8,2,0.8l4.3,0L12.6,5.5z'
    };

    var sentenceColors = {
        execution: '#3266A7',
        exile: '#96D5F2',
        life: '#91CDBC',
        fine: '#5975B9',
        lashes: '#59B297',
        unknown: '#D2EBF1',
        years: '#30A7C2',
        suspended: '#A8CCEA'
    };

    // var spokeAngles = [0, TWO_PI / 6, TWO_PI / 3, TWO_PI / 2, 2 * TWO_PI / 3, 5 * TWO_PI / 6];
    var spokeAngles = [0, 60, 120, 180, 240, 300];

    // Sorted as appears in legend... so not quite the order in which they appear in the circle visualisation!
    var categories = {
        unknown: {
            name: 'UNKNOWN / NOT GUILTY',
            symbol: 'circle',
            visGeometry: {
                startAngle: 0,
                endAngle: TWO_PI,
                innerRadius: null,
                outerRadius: null
            }
        },
        years: {
            name: 'YEARS SENTENCED',
            symbol: 'circle',
            visGeometry: {
                startAngle: 0,
                endAngle: TWO_PI,
                innerRadius: null,
                outerRadius: null
            }
        },
        execution: {
            name: 'EXECUTION',
            symbol: 'cross',
            visGeometry: {
                startAngle: 4 * TWO_PI / 6,
                endAngle: 5 * TWO_PI / 6,
                innerRadius: null,
                outerRadius: null
            }
        },
        fine: {
            name: 'FINE',
            symbol: 'circle',
            visGeometry: {
                startAngle: 0,
                endAngle: TWO_PI / 6,
                innerRadius: null,
                outerRadius: null
            }
        },
        exile: {
            name: 'EXILE',
            symbol: 'diagonal',
            visGeometry: {
                startAngle: 2 * TWO_PI / 6,
                endAngle: 3 * TWO_PI / 6,
                innerRadius: null,
                outerRadius: null
            }
        },
        lashes: {
            name: 'LASHES',
            symbol: 'circle',
            visGeometry: {
                startAngle: TWO_PI / 6,
                endAngle: 2 * TWO_PI / 6,
                innerRadius: null,
                outerRadius: null
            }
        },
        life: {
            name: 'LIFE IMPRISONMENT',
            symbol: 'dash',
            visGeometry: {
                startAngle: TWO_PI / 2,
                endAngle: 4 * TWO_PI / 6,
                innerRadius: null,
                outerRadius: null
            }
        },
        suspended: {
            name: 'YEARS SUSPENDED',
            symbol: 'circle',
            visGeometry: {
                startAngle: 5 * TWO_PI / 6,
                endAngle: TWO_PI,
                innerRadius: null,
                outerRadius: null
            }
        }
    };

    var layer1RadiusScale = d3.scale.sqrt().domain([0, 100]);
    var segment0RadiusScale = d3.scale.sqrt().domain([0, 6000000]); // fine
    var segment1RadiusScale = d3.scale.sqrt().domain([0, 200]); // lashes
    var segment5RadiusScale = d3.scale.sqrt().domain([0, 100]);

    var sentencesUrl = {
        en: null,
        fa: null
    };

    var judgesProfileUrl, judgesAllPrisonersUrl;

    var arcGenerator = d3.svg.arc();

    var language = null;
    var enFa = smallmedia.tilesVisLanguage.enFa;

    /*-----
    HELPERS
    -----*/
    function showVis() {
        return (
            ipa.site === 'ipa' &&
            (
                state.mode === 'tablet-landscape' ||
                state.mode === 'desktop-small' ||
                state.mode === 'desktop-large'
            )
        );
    }

    function getPosFromAngle(r, a) {
        var pos = {};
        pos.x = r * Math.sin(a);
        pos.y = -r * Math.cos(a);
        return pos;
    }

    function radToDeg(a) {
        return 180 * a / Math.PI;
    }


    /*-------------
    DATA PROCESSING
    -------------*/
    function processData(json) {
        // build lookup of sentences
        var sentences = {};

        _.each(json.sentences, function(d, i) {
            sentences[i] = d;
        });

        // merge sentence data into prisoner data


        var prisoners = [];
        _.each(sentences, function(d, i) {


            _.each(json.prisoners, function(_d, _i) {

                if (sentences[i].arrest__prisoner_id == _d.id) {


                    sentences[i] = _.merge(d, _d);

                }


            });


        });

        prisoners = sentences;

        // merge sentence_years and sentence_months
        prisoners = _.map(prisoners, function(d) {
            d.sentence = null;
            if (d.sentence_years === null && d.sentence_months === null)
                return d;

            d.sentence = d.sentence_years + (d.sentence_months / 12);
            return d;
        });

        // add extra info such as the sentence type
        prisoners = _.map(prisoners, function(d) {
            d.extraInfo = {};

            if (d.death_penalty === true)
                d.extraInfo.sentenceType = 'execution';
            else if (d.life !== null && d.life === true)
                d.extraInfo.sentenceType = 'life';
            else if (d.sentence !== null)
                d.extraInfo.sentenceType = 'years';
            else if (d.number_of_lashes !== null)
                d.extraInfo.sentenceType = 'lashes';
            else if (d.exiled !== null && d.exiled === true)
                d.extraInfo.sentenceType = 'exile';
            else if (d.fine !== null)
                d.extraInfo.sentenceType = 'fine';
            // else if(d. !== null) //TODO
            // d.extraInfo.sentenceType = 'suspended';
            else
                d.extraInfo.sentenceType = 'unknown';

            return d;
        });

        state.groupedData = groupDataIntoLayersAndSegments(prisoners);

        // console.log(state.groupedData);
    }

    function groupDataIntoLayersAndSegments(prisoners) {

        var ret = {
            layer0: [],
            layer1: [],
            segments: []
        };

        // Execution
        ret.segments[4] = _.remove(prisoners, function(d) {
            return d.extraInfo.sentenceType === 'execution';
        });

        // Life sentence
        ret.segments[3] = _.remove(prisoners, function(d) {
            return d.extraInfo.sentenceType === 'life';
        });

        // Sentence
        ret.layer1 = _.remove(prisoners, function(d) {
            return d.extraInfo.sentenceType === 'years';
        });

       // Lashes
        ret.segments[1] = _.remove(prisoners, function(d) {
            return d.extraInfo.sentenceType === 'lashes';
        });

        // Exile TODO
        ret.segments[2] = _.remove(prisoners, function(d) {
            return d.extraInfo.sentenceType === 'exile';
        });

        // Fine
        ret.segments[0] = _.remove(prisoners, function(d) {
            return d.extraInfo.sentenceType === 'fine';
        });

        // Years suspended
        ret.segments[5] = _.remove(prisoners, function(d) {
            return d.extraInfo.sentenceType === 'suspended';
        });

        // Unknown
        ret.layer0 = _.map(prisoners, function(d) {
            return d;
        });

        // _.forEach(prisoners, function(d) {
        //     // if (d.fine !== null) { ret.segments[0].push(d); };
        //     if (d.death_penalty === true) { ret.segments[1].push(d); };
        //     if (d.exiled !== null && d.exiled === true) { ret.segments[2].push(d); };
        //     if (d.life !== null && d.life === true) { ret.segments[3].push(d); };
        //     if (d.number_of_lashes !== null) { ret.segments[4].push(d); };
        //     // if (d.number_of_lashes !== null) { ret.segments[4].push(d); };
        //     if (d.sentence !== null) { ret.layer0.push(d); };
        //     if ( d.extraInfo.sentenceType == 'unknown') { ret.layer1.push(d); };


        // })

        return ret;
    }

    /*-------
    TEMPLATES
    -------*/
    function closedTemplate() {
        return '';
    }

    function closeButtonTemplate() {
        return '<div class="circlevis-close-panel"><svg width="20px" height="20px"><g transform="scale(0.08)translate(-10,-10)"><g><path class="st0" d="M205.6,221c-4,0-7.9-1.5-10.9-4.5L4.5,26.4c-6-6-6-15.8,0-21.8c6-6,15.8-6,21.8,0l190.1,190.1c6,6,6,15.8,0,21.8C213.5,219.5,209.5,221,205.6,221z"/></g><g><path class="st0" d="M15.4,221c-4,0-7.9-1.5-10.9-4.5c-6-6-6-15.8,0-21.8L194.7,4.5c6-6,15.8-6,21.8,0c6,6,6,15.8,0,21.8L26.4,216.5C23.3,219.5,19.4,221,15.4,221z"/></g></g></svg></div>';
    }

    function explanationTemplate() {
        return '<div class="circlevis-explanation">' + enFa('Each icon on the left represents a prisoner. Hover over the key below or the diagram on the left to explore the prisoners sentenced by this judge. Click on the judge image or the ‘x’ to close this box.') + '</div>';
    }

    function judgeTemplate(d) {
        var ret = '';
        ret += '<div class="circlevis-aboutjudge">';
        // ret += '<div class="circlevis-header">JUDGE SELECTED</div>';
        ret += '<div class="circlevis-header">' + enFa('JUDGE SELECTED') + '</div>';
        ret += '<div class="circlevis-value">' + (language === 'en' ? d.surname : d.surname) + '</div>';
        ret += '<div class="" ><a href="' + judgesProfileUrl(d) + '/">' + enFa('View Profile') + '>></a></div>';
        ret += '</div>';
        return ret;
    }

    function sentencedTemplate(d) {
        // console.log(d);
        var ret = '';

        console.log(d.forename);

        var forename = d.forename ? d.forename : "";
        var surname = d.surname ? d.surname : "";
        var space = d.forename && d.surname ? " " : "";

        ret += '<div class="circlevis-sentenced">';
        ret += '<div class="circlevis-header">' + enFa('PRISONERS SENTENCED') + '</div>';
        ret += '<div class="circlevis-value">' + d.stats.prisoners_sentenced + '</div>';
        ret += '<div><a href="' + judgesAllPrisonersUrl(d) + forename + space + surname + '">' + enFa('View All Prisoners') + '>></a></div>';
        ret += '</div>';
        return ret;
    }

    function biographyTemplate(d) {
        if (d.biography === null)
            return '';

        var bio = language === 'en' ? d.biography : d.biography;

        if (bio.length > config.maxBiographyLength)
            bio = bio.substr(0, config.maxBiographyLength) + '&hellip;';


        var ret = '';
        ret += '<div class="circlevis-biography">';
        ret += '<div>' + bio + '</div>';
        ret += '</div>';
        return ret;
    }


    function phoneTemplate(d) {
        var ret = '';
        if (state.selectedJudge === null)
            return ret;

        ret += '<div class="circlevis-about circlevis-about-phone">';
        ret += closeButtonTemplate();
        ret += '<div class="circlevis-about-inner">';
        ret += judgeTemplate(d);
        ret += sentencedTemplate(d);
        ret += biographyTemplate(d);
        ret += '</div>';
        ret += '</div>';

        return ret;
    }

    function tabletTemplate(d) {
        var ret = '';
        if (state.selectedJudge === null)
            return ret;

        ret += '<div class="circlevis-about circlevis-about-tablet">';
        ret += closeButtonTemplate();
        ret += '<div class="circlevis-about-inner">';
        ret += judgeTemplate(d);
        ret += sentencedTemplate(d);
        ret += biographyTemplate(d);
        ret += '</div>';
        ret += '</div>';
        return ret;
    }

    function fullTemplate(d) {
        var ret = '';
        if (state.selectedJudge === null)
            return ret;

        // Define triangle for the tooltip
        var svgTriangle = '<svg width="40px" height="20px"><path d="M0,0 l20,0 l-10,10 z"></path></svg>';

        var circleVisClass = 'circlevis-vis-' + classFromMode(state.mode);
        ret += '<div class="circlevis-vis ' + circleVisClass + '"><svg><g class="circlevis-vis"></g></svg></div>';
        ret += '<div class="circlevis-about circlevis-about-full ' + circleVisClass + '">';
        ret += closeButtonTemplate();
        ret += '<div class="circlevis-about-inner">';
        ret += judgeTemplate(d);
        ret += sentencedTemplate(d);
        ret += biographyTemplate(d);
        ret += '<div class="circlevis-legend">';
        ret += explanationTemplate();
        ret += '</div>';
        ret += '</div>';
        ret += '</div>';
        ret += '<div class="circlevis-vis-tooltip"><div class="circlevis-vis-tooltip-inner"></div>' + svgTriangle + '</div>';
        return ret;
    }

    var tooltipSentenceTemplates = {
        execution: function(d) {
            return enFa('Execution');
        },
        exile: function(d) {
            return enFa('Exiled');
        },
        life: function(d) {
            return enFa('Life');
        },
        fine: function(d) {
            return d.fine + ' ' + enFa('fine');
        },
        lashes: function(d) {
            return d.number_of_lashes + ' ' + enFa('lashes');
        },
        unknown: function(d) {
            return enFa('Unknown / not guilty');
        },
        years: function(d) {
            var month = (
              d.sentence_months
                ? ' ' + d.sentence_months + ' ' + enFa('months') // jshint ignore:line
                : ''
            );
            return d.sentence_years + ' ' + enFa('years') + month;
        },
        suspended: function(d) {
                return enFa('Suspended');
            } //TODO
    };

    function getDateOfBirthString(d) {
        var day, month, year;
        if (language === 'en') {
            day = d.dob_day;
            month = d.dob_month;
            year = d.dob_year;
        } else {
            day = d.dob_day_fa;
            month = d.dob_month_fa;
            year = d.dob_year_fa;
        }

        var dob = '';
        if (day !== null) {
            dob = day + '.' + month + '.' + year;
        } else if (month !== null) {
            dob = month + '.' + year;
        } else if (year !== null) {
            dob = year;
        } else {
            dob = enFa('Unknown date of birth');
        }

        return dob;
    }

    function tooltipTemplate(d) {
        // console.log(d);
        var ret = '';

        // Photo
        var picture = (
          d.picture_url
            ? d.picture_url // jshint ignore:line
            : ipa.staticPrefix + "public/img/profile_temp.png?v=2019-08-28"
        );

        ret += '<div class="circlevis-photo"><img src="' + picture + '" alt="' + d.forename + ' ' + d.surname + '" ></div>';

        // Name
        ret += '<div class="circlevis-name">' + d.forename + ' ' + d.surname + '</div>';

        // Date of birth
        var dob = getDateOfBirthString(d);
        ret += '<div class="circlevis-dob">' + '</div>';

        // Persecuted for
        var persecutedFor = language === 'en' ? d.latest_activity_persecuted_for_name_en : d.latest_activity_persecuted_for_name_fa;
        if (persecutedFor === null)
            persecutedFor = ' ';
        ret += '<div class="circlevis-latest-activity">' + persecutedFor + '</div>';

        // Sentence type
        ret += '<div class="sentence-type">' + enFa('Sentence') + ': ' + tooltipSentenceTemplates[d.extraInfo.sentenceType](d) + '</div>';

        return ret;
    }

    function setUpCloseButton() {
        config.container
            .select('.circlevis-close-panel svg')
            .on('click', function() {
                // Not ideal, be nicer to use a mediator pattern
                smallmedia.tilesVis.clearSelectedTile();
                smallmedia.tilesVis.update();
            });
    }

    /*-------
    CONSTRUCT
    -------*/
    function construct() {
        config.container
            .style('display', 'none')
            .style('width', '100%')
            .style('background-color', '#F9FCFC');
    }


    /*----
    UPDATE
    ----*/
    function updateLegend() {

        var categoriesArray = _.map(categories, function(v, k) {
            v.id = k;
            return v;
        });

        config.container
            .select('.circlevis-legend')
            .selectAll('div.circlevis-item')
            .data(categoriesArray)
            .enter()
            .append('div')
            .classed('circlevis-item', true)
            .html(function(d) {
                var ret = '';
                var symbolStyle = 'style="fill: ' + sentenceColors[d.id] + '"';
                var symbol = '<circle cx="5" cy="5" r="5" ' + symbolStyle + '></circle>';
                if (d.symbol !== 'circle') {
                    symbol = '<path transform="scale(0.5)" d="' + iconSvg[d.symbol] + '"' + symbolStyle + '></path>';
                }
                ret += '<svg width="16" height="10">';
                ret += symbol;
                ret += '</svg>';
                ret += enFa(d.name);
                return ret;
            })
            .on('mouseover', handleCategoryMouseover)
            .on('mouseout', handleCategoryMouseout);
    }

    function updateCategoryHighlight() {
        // console.log('highlight')
        // console.log('hover', state.hoveredCategory);
        config.container
            .select('.circlevis-legend')
            .selectAll('div.circlevis-item')
            .style('background-color', function(d) {
                return d.id === state.hoveredCategory ? '#E8F1F1' : 'transparent';
            });

        d3.select('.circlevis-vis')
            .selectAll('g.hover-layer path')
            .style('fill', function(d) {
                return d.id === state.hoveredCategory ? '#EFF6F6' : 'none';
            });
    }

    function updatePanelStyle() {

        config.container
            .select('.circlevis-about')
            .style('padding', config.aboutPadding + 'px')
            .style('font-size', config.infoFontSize + 'px');

        /* HACK - to handle scrollbar appearing and altering page width! */
        var pageWidth = $('.tiles-container').width();

        if (showVis()) {
            var size = heightFromMode[state.mode];

            config.container
                .select('svg')
                .attr('width', size + 'px')
                .attr('height', size + 'px');

            geometry.aboutWidth = pageWidth - size - 2 * config.aboutPadding;
        } else {
            geometry.aboutWidth = pageWidth - 2 * config.aboutPadding;
        }

        config.container
                .select('.circlevis-about')
                .style('width', geometry.aboutWidth + 'px');
    }

    function visLayout() {
        // Compute the positions of the prisoner icons

        // layer 0
        _.each(state.groupedData.layer0, function(d, i) {
            var row = Math.floor(i / config.vis.numCols);

            d.geometry = {};
            d.geometry.r = geometry.innerRadius + (row + 0.5) * geometry.rowHeight;
            d.geometry.angle = (i % config.vis.numCols + 0.5) * geometry.angleStep;

            d.geometry.pos = getPosFromAngle(d.geometry.r, d.geometry.angle);
        });

        // layer 1
        _.each(state.groupedData.layer1, function(d, i) {
            var row = Math.floor(i / config.vis.numCols);

            d.geometry = {};
            d.geometry.r = geometry.layer1Radius + (row + 0.5) * geometry.rowHeight;
            d.geometry.angle = (i % config.vis.numCols + 0.5) * geometry.angleStep;

            d.geometry.pos = getPosFromAngle(d.geometry.r, d.geometry.angle);
        });

        // segments
        _.each(state.groupedData.segments, function(segment, i) {
            _.each(segment, function(d, ii) {
                var row = Math.floor(ii / geometry.segmentNumCols);

                d.geometry = {};
                d.geometry.r = geometry.segmentRadius + (row + 0.5) * geometry.rowHeight;
                d.geometry.angle = (ii % geometry.segmentNumCols + 0.5) * geometry.segmentAngleStep + i * geometry.segmentAngle;

                d.geometry.pos = getPosFromAngle(d.geometry.r, d.geometry.angle);
            });
        });
    }

    function updateVisGeometry() {
        var size = heightFromMode[state.mode];

        // Offset of the containing g element
        geometry.offset = 0.5 * size;

        geometry.innerRadius = 0.1 * size;
        geometry.outerRadius = 0.5 * 0.9 * size;

        // geometry.segmentNumCols = config.vis.numCols / 6;
        geometry.segmentNumCols = 4;

        var numRows = {};
        numRows.layer0 = Math.ceil(state.groupedData.layer0.length / config.vis.numCols);
        numRows.layer1 = Math.ceil(state.groupedData.layer1.length / config.vis.numCols);

        // Force minimum or 1 row in layer 1
        if (numRows.layer1 === 0)
            numRows.layer1 = 1;

        numRows.segments = _.map(state.groupedData.segments, function(segment) {
            return Math.ceil(segment.length / geometry.segmentNumCols);
        });

        // console.log(numRows);

        var maxRowsOfSegments = _.max(numRows.segments);
        if (maxRowsOfSegments === 0)
            maxRowsOfSegments = 1;

        var totalNumRows = numRows.layer0 + numRows.layer1 + maxRowsOfSegments;
        // console.log(totalNumRows);

        geometry.rowHeight = config.vis.rowHeight;
        var computedRowHeight = (geometry.outerRadius - geometry.innerRadius) / totalNumRows;
        if (computedRowHeight < geometry.rowHeight)
            geometry.rowHeight = computedRowHeight;

        geometry.layer1Radius = geometry.innerRadius + numRows.layer0 * geometry.rowHeight;
        geometry.segmentRadius = geometry.layer1Radius + numRows.layer1 * geometry.rowHeight;

        geometry.angleStep = 2 * Math.PI / config.vis.numCols;
        geometry.segmentAngle = 2 * Math.PI / 6;
        geometry.segmentAngleStep = geometry.segmentAngle / geometry.segmentNumCols;

        geometry.innerCircleRadius = geometry.rowHeight * 0.2 * 0.5;
        geometry.outerCircleRadius = geometry.rowHeight * 0.8 * 0.5;

        // Update the inner and outer radii for each category's segment
        categories.unknown.visGeometry.innerRadius = 0;
        categories.unknown.visGeometry.outerRadius = geometry.layer1Radius;
        categories.years.visGeometry.innerRadius = geometry.layer1Radius;
        categories.years.visGeometry.outerRadius = geometry.segmentRadius;

        categories.fine.visGeometry.innerRadius = geometry.segmentRadius;
        categories.exile.visGeometry.innerRadius = geometry.segmentRadius;
        categories.life.visGeometry.innerRadius = geometry.segmentRadius;
        categories.suspended.visGeometry.innerRadius = geometry.segmentRadius;
        categories.execution.visGeometry.innerRadius = geometry.segmentRadius;
        categories.lashes.visGeometry.innerRadius = geometry.segmentRadius;

        categories.fine.visGeometry.outerRadius = geometry.outerRadius;
        categories.exile.visGeometry.outerRadius = geometry.outerRadius;
        categories.life.visGeometry.outerRadius = geometry.outerRadius;
        categories.suspended.visGeometry.outerRadius = geometry.outerRadius;
        categories.execution.visGeometry.outerRadius = geometry.outerRadius;
        categories.lashes.visGeometry.outerRadius = geometry.outerRadius;

        // console.log(geometry);
    }

    function updateScaleFunctions() {
        layer1RadiusScale.range([geometry.innerCircleRadius, geometry.outerCircleRadius]);
        segment0RadiusScale.range([geometry.innerCircleRadius, geometry.outerCircleRadius]);
        segment1RadiusScale.range([geometry.innerCircleRadius, geometry.outerCircleRadius]);
        segment5RadiusScale.range([geometry.innerCircleRadius, geometry.outerCircleRadius]);
    }

    function layer1Circles(d) {
        d3.select(this)
            .append('circle')
            .attr('r', function(d) {
                return layer1RadiusScale(d.sentence);
            })
            .style('fill', '#91CEDC'); //sentenceColors.years);

        d3.select(this)
            .append('circle')
            .attr('r', geometry.innerCircleRadius)
            .style('fill', sentenceColors.years);

    }

    function segment0Circles(d) {
        d3.select(this)
            .append('circle')
            .attr('r', function(d) {
                return segment0RadiusScale(d.fine);
            })
            .style('fill', '#849BC7');

        d3.select(this)
            .append('circle')
            .attr('r', geometry.innerCircleRadius)
            .style('fill', sentenceColors.fine);

    }

    function segment1Circles(d) {
        d3.select(this)
            .append('circle')
            .attr('r', function(d) {
                return segment1RadiusScale(d.number_of_lashes);
            })
            .style('fill', '#8AC7B5');

        d3.select(this)
            .append('circle')
            .attr('r', geometry.innerCircleRadius)
            .style('fill', sentenceColors.lashes);

    }

    function segment5Circles(d) {
        d3.select(this)
            .append('circle')
            .attr('r', function(d) {
                return segment5RadiusScale(d.sentence);
            })
            .style('fill', '#C1DAEE');

        d3.select(this)
            .append('circle')
            .attr('r', geometry.innerCircleRadius)
            .style('fill', sentenceColors.suspended);

    }

    function updateVis() {
        if (!showVis())
            return;

        var svg = config.container.select('svg g');
        svg.attr('transform', 'translate(' + geometry.offset + ',' + geometry.offset + ')');

        // Hover layer
        // elements.hoverLayer = svg.append('g')
        //   .classed('circlevis-hover-layer', true);

        // var categoriesArray = _.map(categories, function(v, k) {
        //   v.id = k;
        //   return v;
        // });

        // elements.hoverLayer
        //   .selectAll('path')
        //   .data(categoriesArray)
        //   .enter()
        //   .append('path')
        //   .attr('d', function(d) {
        //     // console.log(d);
        //     return arcGenerator(d.visGeometry);
        //   })
        //   .on('mouseover', handleCategoryMouseover)
        //   .on('mouseout', handleCategoryMouseout);


        // Grid lines
        var grid = svg.append('g')
            .classed('circlevis-vis-grid', true);

        grid.append('circle')
            .attr('r', geometry.segmentRadius);

        grid.append('circle')
            .attr('r', geometry.layer1Radius);

        grid.selectAll('line')
            .data(spokeAngles)
            .enter()
            .append('line')
            .attr('y1', -geometry.segmentRadius)
            .attr('y2', -geometry.outerRadius)
            .attr('transform', function(d) {
                return 'rotate(' + d + ')';
            });


        // And now for the prisoners...
        // Layer 0 (unknown)
        var layer0 = svg.append('g')
            .classed('circlevis-vis-layer0 circlevis-prisoner-group', true)
            .datum(categories.unknown);

        layer0
            .selectAll('circle')
            .data(state.groupedData.layer0)
            .enter()
            .append('circle')
            .classed('circlevis-vis-prisoner', true)
            .attr('r', 5)
            .attr('cx', function(d) {
                return d.geometry.pos.x;
            })
            .attr('cy', function(d) {
                return d.geometry.pos.y;
            })
            .style('fill', sentenceColors.unknown)
            .attr("data-id", function(d) {

                return d.id;
            });

        // Layer 1 (years sentence)
        var layer1 = svg.append('g')
            .classed('circlevis-vis-layer1 circlevis-prisoner-group', true)
            .datum(categories.years);

        layer1
            .selectAll('g')
            .data(state.groupedData.layer1)
            .enter()
            .append('g')
            .classed('circlevis-vis-prisoner', true)
            .attr('transform', function(d) {
                return 'translate(' + d.geometry.pos.x + ',' + d.geometry.pos.y + ')';
            })
            .each(layer1Circles)
            .attr("data-id", function(d) {
                return d.id;
            });


        // Segment 0 (fine)
        var segment0 = svg.append('g')
            .classed('circlevis-vis-segment circlevis-vis-segment0 circlevis-prisoner-group', true)
            .datum(categories.fine);

        segment0
            .selectAll('g')
            .data(state.groupedData.segments[0])
            .enter()
            .append('g')
            .classed('circlevis-vis-prisoner', true)
            .attr('transform', function(d) {
                return 'translate(' + d.geometry.pos.x + ',' + d.geometry.pos.y + ')';
            })
            .each(segment0Circles)
            .attr("data-id", function(d) {
                return d.id;
            });

        // Segment 1 (lashes)
        var segment1 = svg.append('g')
            .classed('circlevis-vis-segment circlevis-vis-segment1 circlevis-prisoner-group', true)
            .datum(categories.lashes);

        segment1
            .selectAll('g')
            .data(state.groupedData.segments[1])
            .enter()
            .append('g')
            .classed('circlevis-vis-prisoner', true)
            .attr('transform', function(d) {
                return 'translate(' + d.geometry.pos.x + ',' + d.geometry.pos.y + ')';
            })
            .each(segment1Circles)
            .attr("data-id", function(d) {
                return d.id;
            });

        // Segment 2 (exile)
        var segment2 = svg.append('g')
            .classed('circlevis-vis-segment circlevis-vis-segment2 circlevis-prisoner-group', true)
            .datum(categories.exile);

        segment2
            .selectAll('path')
            .data(state.groupedData.segments[2])
            .enter()
            .append('path')
            .classed('circlevis-vis-prisoner', true)
            .attr('d', iconSvg.diagonal)
            .style('fill', sentenceColors.exile)
            .attr('transform', function(d) {
                return 'rotate(' + radToDeg(d.geometry.angle) + ')translate(0, -' + d.geometry.r + ')translate(-7,-7)scale(0.5)';
            })
            .attr("data-id", function(d) {
                return d.id;
            });

        // Segment 3 (life)
        var segment3 = svg.append('g')
            .classed('circlevis-vis-segment circlevis-vis-segment3 circlevis-prisoner-group', true)
            .datum(categories.life);

        segment3
            .selectAll('path')
            .data(state.groupedData.segments[3])
            .enter()
            .append('path')
            .classed('circlevis-vis-prisoner', true)
            .attr('d', iconSvg.dash)
            .style('fill', sentenceColors.life)
            .attr('transform', function(d) {
                return 'rotate(' + radToDeg(d.geometry.angle) + ')translate(0, -' + d.geometry.r + ')translate(-7,-7)scale(0.5)';
            })
            .attr("data-id", function(d) {
                return d.id;
            });

        // Segment 4 (execution)
        var segment4 = svg.append('g')
            .classed('circlevis-vis-segment circlevis-vis-segment4 circlevis-prisoner-group', true)
            .datum(categories.execution);

        segment4
            .selectAll('path')
            .data(state.groupedData.segments[4])
            .enter()
            .append('path')
            .classed('circlevis-vis-prisoner', true)
            .attr('d', iconSvg.cross)
            .style('fill', sentenceColors.execution)
            .attr('transform', function(d) {
                return 'rotate(' + radToDeg(d.geometry.angle) + ')translate(0, -' + d.geometry.r + ')translate(-7,-7)scale(0.5)';
            })
            .attr("data-id", function(d) {
                return d.id;
            });

        // Segment 5 (suspended)
        var segment5 = svg.append('g')
            .classed('circlevis-vis-segment circlevis-vis-segment5 circlevis-prisoner-group', true)
            .datum(categories.suspended);

        segment5
            .selectAll('g')
            .data(state.groupedData.segments[5])
            .enter()
            .append('g')
            .classed('circlevis-vis-prisoner', true)
            .attr('transform', function(d) {
                return 'translate(' + d.geometry.pos.x + ',' + d.geometry.pos.y + ')';
            })
            .each(segment5Circles)
            .attr("data-id", function(d) {
                return d.id;
            });

        // Attach tooltip event
        svg.selectAll('.circlevis-vis-prisoner')
            .on('mouseover', handlePrisonerMouseover)
            .on('mouseout', handlePrisonerMouseout);

        svg.selectAll('.circlevis-prisoner-group')
            .on('mouseover', handleCategoryMouseover)
            .on('mouseout', handleCategoryMouseout)
            .insert('g', ':first-child')
            .classed('hover-layer', true)
            .append('path')
            .attr('d', function(d) {
                return arcGenerator(d.visGeometry);
            });

    }

    function updateTooltip(d) {
        var x = d.geometry.pos.x + geometry.offset - 30;
        var y = d.geometry.pos.y + geometry.offset - 100;
        // console.log(x, y);

        config.container
            .select('.circlevis-vis-tooltip')
            .style('display', 'block')
            .style('left', x + 'px')
            .style('top', y + 'px')
            .select('.circlevis-vis-tooltip-inner')
            .html(tooltipTemplate(d));
    }

    function hideTooltip() {
        config.container
            .select('.circlevis-vis-tooltip')
            .style('display', 'none');
    }

    function update() {
        // console.log(state);
        language = smallmedia.tilesVisLanguage.getLanguage();

        config.container
            .style('display', state.selectedJudge === null ? 'none' : 'block')
            .style('height', heightFromMode[state.mode] + 'px')
            .html(templateFromMode[state.mode](state.selectedJudge));


        updatePanelStyle();

        setUpCloseButton();

        updateLegend();



        if (state.selectedJudge === null)
            return;

        if (!showVis())
            return;

        // Get prisoner's of selected judge
        var url = sentencesUrl.en(state.selectedJudge);
        if (language === 'fa')
            url = sentencesUrl.fa(state.selectedJudge);

        d3.json(url, function(err, json) {

            processData(json);
            // useTestData();
            updateVisGeometry();
            updateScaleFunctions();
            visLayout();
            updateVis();

        });
    }

    /*----
    EVENTS
    ----*/
    function handleCategoryMouseover(d) {
        // console.log(d);
        state.hoveredCategory = d.id;
        updateCategoryHighlight();
    }

    function handleCategoryMouseout(d) {
        // console.log('out', d);
        state.hoveredCategory = null;
        updateCategoryHighlight();
    }

    function handlePrisonerMouseover(d) {
        console.log(d);
        updateTooltip(d);
    }

    function handlePrisonerMouseout(d) {
        hideTooltip();
    }

    $(document).on("click", '.circlevis-vis-prisoner', function() {

        var id = $(this).data("id");
        window.open("/" + language + "/prisoner/" + id + "/", "_self");

    });

    /*-
    API
    -*/
    my.init = function(conf) {
        config = _.extend(config, conf);

        // data = cleanData(config.data);


        judgesProfileUrl = _.template(config.judgesProfileUrl);
        judgesAllPrisonersUrl = _.template(config.judgesAllPrisonersUrl);

        sentencesUrl.en = _.template(config.enSentencesUrl);
        sentencesUrl.fa = _.template(config.faSentencesUrl);

        construct();
    };

    my.setSelectedJudge = function(j) {
        state.selectedJudge = j;
    };

    my.setMode = function(mode) {
        state.mode = mode;
    };

    my.setWidth = function(width) {
        config.width = width;
    };

    my.setInfoFontSize = function(px) {
        config.infoFontSize = px;
    };

    my.setMaxBiographyLength = function(chars) {
        config.maxBiographyLength = chars;
    };

    // my.setLanguage = function(lang) {
    //   config.language = lang;
    // }

    my.update = function() {
        update();
    };

    my.getHeightFromMode = function(mode) {
        return heightFromMode[mode];
    };

    return my;
}());
