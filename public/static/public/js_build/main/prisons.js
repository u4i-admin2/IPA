// @ts-check

/**
 * @type {ipa.AeaPrisonsMainDataCumulatives | ipa.IpaPrisonsMainDataCumulatives}
 */
var cumulatives = cumulatives;

/**
 * @type {ipa.AeaPrisonsMainData | ipa.IpaPrisonsMainData}
 */
var mainData = mainData;

(function() {
    "use strict";

    var colours = {
        mapMarkerNeutral: {
            aea: 'rgba(86, 192, 135 , 1)',
            ipa: 'rgba(47, 166, 193 , 1)',
        },
        mapMarkerSelected: {
            aea: 'rgba(223, 134, 81 , 1)',
            ipa: 'rgba(234, 172, 95 , 1)',
        },
        popCircleNeutral: {
            aea: 'rgba(86, 192, 135 , 0.2)',
            ipa: 'rgba(47, 166, 193 , 0.2)',
        },
        popCircleSelected: {
            aea: 'rgba(223, 134, 81 , 0.2)',
            ipa: 'rgba(234, 172, 95 , 0.2)',
        },
    };

    UFIF.controller('prisons', function($scope, $location) {
        $scope.allAreas = [];
        var all = ipa.lang == 'en' ? 'all' : '​همه';
        $scope.url = $location.absUrl();
        $(".map").panzoom();
        var _top = 39.703449;
        var _bottom = 25.063190;
        var _left = 44.080966;
        var _right = 63.416901;
        var state = null;

        /** @type {ipa.AeaPrisonsMainData | null} */
        var aeaMainData = null;

        /** @type {ipa.IpaPrisonsMainData | null} */
        var ipaMainData = null;

        /** @type {number | null} */
        var cumulativePopulation = null;

        /** @type {string | null} */
        var defaultDataSetName = null;

        if (ipa.site === 'aea') {
            defaultDataSetName = 'procedural_violations';
        } else if (ipa.site === 'ipa') {
            defaultDataSetName = 'ethnicities';
        }


        var $panzoom = $(".map").panzoom("option", {
            increment: 0.1,
            minScale: 0.1,
            maxScale: 2,
            duration: 500,
            $zoomIn: $(".icon-plus"),
            $zoomOut: $(".icon-minus"),

        });
        $panzoom.parent().on('mousewheel.focal', function(e) {
            e.preventDefault();

            var delta = e.delta || e.originalEvent.wheelDelta;
            var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;

            $panzoom.panzoom('zoom', zoomOut, {
                increment: 0.007,
                animate: false,
                focal: e
            });
        });

        $('.zoomCenter').on('tap', function(e) {
            var resetVal = ipa.lang == 'en' ? 'matrix(0.292, 0, 0, 0.292, -119.012, -117.774)' : 'matrix(0.292, 0, 0, 0.292, 125.988, -120.774)';

            $('.map').css('transform', resetVal);
        });

        $panzoom.parent().get([0]).addEventListener('DOMMouseScroll', mouseWheelEvent);

        function mouseWheelEvent(e) {
            e.preventDefault();
            var delta = e.wheelDelta ? e.wheelDelta : -e.detail;

            var zoomOut = delta ? delta < 0 : e.originalEvent.deltaY > 0;

            $panzoom.panzoom('zoom', zoomOut, {
                increment: 0.007,
                animate: false,
                focal: e
            });
        }

        $(document).on('tap', '.filterHeaderPrison', function() {
            $(this).parent().find('.blueArea').slideToggle();
            $(this).find('.icon-up-dir').toggle();
            $(this).find('.icon-down-dir').toggle();
        });

        $scope.administered_by_stats = administered_by_stats;

        $scope.switchArray = [];

        $scope.statusArray = ['pdotj', 'moi', 'police', 'irgc'];

        var colorsRange = ipa.colorsRange;

        var mapWidthRatio = (_right - _left) / 2000;
        var mapHeightRatio = (_top - _bottom) / 1800;

        /** @type {Array<ipa.AeaPrisonData | ipa.IpaPrisonData>} */
        var data = [];
        var dataNo = 0;

        var prisonersTotals = [];
        var tt = $('.toolTipHolder');

        $(document).mousemove(function(event) {
            tt.css('top', event.pageY - tt.height() - 15);
            tt.css('left', event.pageX - 15);
        });

        if (ipa.site === 'aea') {
            aeaMainData = /** @type {ipa.AeaPrisonsMainData} */ (mainData);

            aeaMainData[0] = /** @type {ipa.AeaPrisonsMainDataCumulatives} */ (cumulatives);

            cumulativePopulation = aeaMainData[0].total_victims;

            angular.forEach(aeaMainData, function(item, i) {
                item.id = i;

                if (item.latitude && item.total_victims) {
                    /** @type {ipa.AeaPrisonData} */
                    var prisonData = item;

                    data.push(prisonData);

                    prisonersTotals.push(prisonData.total_victims || 0);
                }
            });
        } else if (ipa.site === 'ipa') {
            ipaMainData = /** @type {ipa.IpaPrisonsMainData} */ (mainData);

            ipaMainData[0] = /** @type {ipa.IpaPrisonsMainDataCumulatives} */ (cumulatives);

            cumulativePopulation = ipaMainData[0].total_prisoners;

            angular.forEach(ipaMainData, function(item, i) {
                item.id = i;

                if (item.latitude && item.total_prisoners) {
                    /** @type {ipa.IpaPrisonData} */
                    var prisonData = item;

                    data.push(prisonData);

                    prisonersTotals.push(prisonData.total_prisoners || 0);
                }
            });
        }

        function getMaxOfArray(numArray) {
            return Math.max.apply(null, numArray);
        }

        var populationRatio = getMaxOfArray(prisonersTotals) / 200;

        /**
         * @param {number} longitude
         */
        var getPosLong = function(longitude) {
            var pos = (longitude - _left) / mapWidthRatio;
            var nearestPos = (Math.ceil(pos / 20) * 20) + 10;

            return nearestPos - 2;

        };

        /**
         * @param {number} latitude
         */
        var getPosLat = function(latitude) {
            var pos = (latitude - _bottom) / mapHeightRatio;
            var nearestPos = (Math.round(pos / 20) * 20) + 10;
            return 1820 - nearestPos - 2;

        };

        var svg = d3.select(".mapData").append("svg")
            .attr("width", 2020)
            .attr("height", 1820);

        var population = svg.selectAll("population")
            .data(data);

        population.enter().append("circle")
            .attr("cy", function(d, i) {
                var pos = (d.latitude - _bottom) / mapHeightRatio;
                var nearestPos = (Math.round(pos / 20) * 20) + 10;

                return 1820 - nearestPos - 2;
            })
            .attr("cx", function(d, i) {
                var pos = (d.longitude - _left) / mapWidthRatio;
                var nearestPos = (Math.ceil(pos / 20) * 20) + 10;

                return nearestPos - 2;
            })
            .attr("r", 0)
            .attr("class", function(d, i) {

                return 'popCircle pop' + i;

            })
            .style("fill", colours.popCircleNeutral[ipa.site])
            .transition()
            .duration(1000)
            .attr("r", function(d) {
                return (d.total_victims || d.total_prisoners || 0) / populationRatio;
            });


        var circle = svg.selectAll("data")
            .data(data);

        circle.enter().append("circle")
            .attr("cy", function(d, i) {
                var pos = (d.latitude - _bottom) / mapHeightRatio;
                var nearestPos = (Math.round(pos / 20) * 20) + 10;
                return 1820 - nearestPos - 2;
            })
            .attr("cx", function(d, i) {
                var pos = (d.longitude - _left) / mapWidthRatio;
                var nearestPos = (Math.ceil(pos / 20) * 20) + 10;

                return nearestPos - 2;
            })
            .attr("r", function(d) {
                return 10;
            })
            .attr("data-admin", function(d) {
                return d.administered_by;
            })
            .attr("data-no", function(d , i) {
                return i;
            })
            .attr("data-name", function(d) {
                return d.name;
            })
            .on(
                'mouseover',
                /**
                 * @param {ipa.AeaPrisonData | ipa.IpaPrisonData} d
                 * @param {number} i
                 */
                function(d, i) {
                    $scope.allAreasOver = [];

                    angular.forEach(
                        data,
                        /**
                         * @param {ipa.AeaPrisonData | ipa.IpaPrisonData} _v
                         * @param {number} _i
                         */
                        function(_v, _i) {
                            if (getPosLat(d.latitude) === getPosLat(_v.latitude) && getPosLong(d.longitude) === getPosLong(_v.longitude)) {
                                _v.i = _i;

                                $scope.$apply(function() {
                                    $scope.allAreasOver.push(_v);
                                });
                            }
                        }
                    );

                    if ($scope.allAreasOver.length > 1) {
                        var _p = 0;

                        angular.forEach($scope.allAreasOver, function(_v, _i) {
                            _p += (_v.total_victims || _v.total_prisoners);
                        });

                        var mp = ipa.lang == 'en' ? "Multiple Prisons" : 'چندین زندان'; /* cSpell: disable-line */

                        $(".name").html(mp);
                        $(".population").html(_p);

                    } else {
                        $(".population").html(
                            /** @type {ipa.AeaPrisonData} */ (d).total_victims ||
                            /** @type {ipa.IpaPrisonData} */ (d).total_prisoners ||
                            0
                        );
                        $(".name").html(d.name);
                    }

                    d3.select(this)
                        .style('fill', colours.mapMarkerSelected[ipa.site]);

                    d3.select(".pop" + i)
                        .style('fill', colours.popCircleSelected[ipa.site]);

                    tt.stop();
                    tt.height();
                    tt.css('top', d3.event.pageY - tt.height() - 15);
                    tt.css('left', d3.event.pageX - 15);
                    tt.fadeIn(200);
                }
            )
            .on(
                'mouseout',
                /**
                 * @param {ipa.AeaPrisonData | ipa.IpaPrisonData} d
                 * @param {number} i
                 */
                function(d, i) {
                    if (d3.select(this).attr("class").indexOf("selectedPrison") > -1) {

                        d3.select(this)
                            .style('fill', colours.mapMarkerSelected[ipa.site]);

                        d3.select(".pop" + i)
                            .style('fill', colours.popCircleSelected[ipa.site]);

                    } else {

                        d3.select(this)
                            .style('fill', colours.mapMarkerNeutral[ipa.site]);

                        d3.select(".pop" + i)
                            .style('fill', colours.popCircleNeutral[ipa.site]);
                    }

                    tt.stop();
                    tt.fadeOut(200);
                }
            )
            .on(
                'touchend',
                /**
                 * @param {ipa.AeaPrisonData | ipa.IpaPrisonData} d
                 * @param {number} i
                 */
                function(d, i) {
                    $scope.allAreas = [];

                    angular.forEach(
                        data,
                        /**
                        * @param {ipa.AeaPrisonData | ipa.IpaPrisonData} _v
                        * @param {number} _i
                        */
                        function(_v, _i) {
                            if (
                                getPosLat(d.latitude) === getPosLat(_v.latitude) &&
                                getPosLong(d.longitude) === getPosLong(_v.longitude)
                            ) {
                                _v.i = _i;
                                $scope.$apply(function() {
                                    $scope.allAreas.push(_v);
                                });
                            }
                        }
                    );

                    if ($scope.allAreas.length <= 1) {
                        d3.selectAll(".mapMarker")
                            .attr("class", "mapMarker")
                            .style('fill', colours.mapMarkerNeutral[ipa.site]);

                        d3.selectAll(".popCircle")
                            .attr("class", function(d, i) {
                                return "popCircle pop" + i;
                            })
                            .style('fill', colours.popCircleNeutral[ipa.site]);

                        d3.select(this)
                            .attr("class", "mapMarker selectedPrison")
                            .style('fill', colours.mapMarkerSelected[ipa.site]);

                        d3.select(".pop" + i)
                            .style('fill', colours.popCircleSelected[ipa.site])
                            .attr("class", function() {
                                return "popCircle pop" + i + " selectedPrison";
                            });

                        selectPrison(d, i);
                    }
                }
            )
            .on(
                'click',
                /**
                 * @param {ipa.AeaPrisonData | ipa.IpaPrisonData} d
                 * @param {number} i
                 */
                function(d, i) {
                    $scope.allAreas = [];

                    angular.forEach(
                        data,
                        /**
                         * @param {ipa.AeaPrisonData | ipa.IpaPrisonData} _v
                         * @param {number} _i
                         */
                        function(_v, _i) {
                            if (
                                getPosLat(d.latitude) === getPosLat(_v.latitude) &&
                                getPosLong(d.longitude) === getPosLong(_v.longitude)
                            ) {
                                _v.i = _i;
                                $scope.$apply(function() {
                                    $scope.allAreas.push(_v);
                                });
                            }
                        }
                    );

                    if ($scope.allAreas.length <= 1) {
                        d3.selectAll(".mapMarker")
                            .attr("class", "mapMarker")
                            .style('fill', colours.mapMarkerNeutral[ipa.site]);

                        d3.selectAll(".popCircle")
                            .attr("class", function(d, i) {
                                return "popCircle pop" + i;
                            })
                            .style('fill', colours.popCircleNeutral[ipa.site]);

                        d3.select(this)
                            .attr("class", "mapMarker selectedPrison")
                            .style('fill', colours.mapMarkerSelected[ipa.site]);



                        d3.select(".pop" + i)
                            .style('fill', colours.popCircleSelected[ipa.site])
                            .attr("class", function() {
                                return "popCircle pop" + i + " selectedPrison";
                            });

                        selectPrison(d, i);
                    }
                }
            )
            .attr("class", "mapMarker")
            .style("fill", colours.mapMarkerNeutral[ipa.site])
            .style("opacity", 0)
            .transition()
            .duration(1000)
            .style("opacity", 1);

        circle.exit().remove();

        $(document).on('tap', '.multiPrison', function() {
            var i = $(this).data("id");

            d3.selectAll(".mapMarker")
                .attr("class", "mapMarker")
                .style('fill', colours.mapMarkerNeutral[ipa.site]);

            d3.selectAll(".popCircle")
                .attr("class", function(d, i) {
                    return "popCircle pop" + i;
                })
                .style('fill', colours.popCircleNeutral[ipa.site]);

            d3.select('.mapMarker[data-no="' + i + '"]')
                .attr("class", "mapMarker selectedPrison")
                .style('fill', colours.mapMarkerSelected[ipa.site]);



            d3.select(".pop" + i)
                .style('fill', colours.popCircleSelected[ipa.site])
                .attr("class", function() {
                    return "popCircle pop" + i + " selectedPrison";
                });


            // selectPrison(d, i);
            selectPrison($(this).data("prison"), $(this).data("id"));
        });

        /**
         * @param {ipa.AeaPrisonData | ipa.IpaPrisonData} d
         * @param {number} i
         */
        function selectPrison(d, i) {
            dataNo = i;

            $scope.$apply(function() {
                $scope.allAreas = [];
                $scope.name = d.name;
                $scope.id = d.id;
                $scope.bio = d.bio;
                $scope.population = (
                    /** @type {ipa.AeaPrisonData} */ (d).total_victims ||
                    /** @type {ipa.IpaPrisonData} */ (d).total_prisoners
                );
            });

            var svg = d3.select("#viz");
            svg.selectAll("div")
                .transition()
                .duration(1000)
                .style('opacity', 0)
                .remove();
            setTimeout(function() {
                $scope.chart(d[$scope.currentDataSetName], $scope.currentDataSetName);
            }, 1001);
        }

        /**
         * @param {string} status
         */
        $scope.setStatusFilter = function(status) {
            if (status != "ALL") {
                $("." + status).toggleClass("on");
                $(".ALL").removeClass("on");

                var index = $scope.switchArray.indexOf(status);

                if (index == -1) {
                    $scope.switchArray.push(status);
                } else {
                    $scope.switchArray.splice(index, 1);
                }

                $scope.statusArray = $scope.switchArray;

                svg.selectAll(".mapMarker")
                    .transition()
                    .duration(1000)
                    .style("opacity", function(d) {
                        if ($scope.statusArray.indexOf(d.administered_by) != -1) {
                            return 1;
                        } else {
                            return 0;
                        }
                    });

                svg.selectAll(".popCircle")
                    .transition()
                    .duration(1000)
                    .attr('r',
                        /**
                         * @param {ipa.AeaPrisonData | ipa.IpaPrisonData} d
                         * @param {number} i
                         */
                        function(d) {
                            if ($scope.statusArray.indexOf(d.administered_by) != -1) {
                                return (
                                    (
                                        /** @type {ipa.AeaPrisonData} */ (d).total_victims ||
                                        /** @type {ipa.IpaPrisonData} */ (d).total_prisoners ||
                                        0
                                    ) / populationRatio
                                );
                            } else {
                                return 0;
                            }
                        }
                    );
            } else {
                $(".switchHolder").removeClass("on");
                $("." + status).addClass("on");
                $scope.switchArray = [];

                $scope.statusArray = ['pdotj', 'moi', 'police', 'irgc'];

                svg.selectAll(".mapMarker")
                    .transition()
                    .duration(1000)
                    .style("opacity", 1);

                svg.selectAll(".popCircle")
                    .transition()
                    .duration(1000)
                    .attr('r', function(d) {
                        return (d.total_victims || d.total_prisoners || 0) / populationRatio;
                    });
            }
        };


        var map = d3.select(".map")
            .attr("width", "100%")
            .attr("height", "100%");

        $scope.currentDataSetName = defaultDataSetName;
        $scope.population = cumulativePopulation;
        $scope.name = all;

        $scope.reset = function() {
            $scope.allAreas = [];
            $scope.currentDataSetName = defaultDataSetName;
            $scope.id = 0;
            $scope.name = all;
            $scope.population = cumulativePopulation;
            $scope.setSelection($scope.currentDataSetName);

            dataNo = 0;

            d3.selectAll(".mapMarker").attr("class", "mapMarker").style('fill', colours.mapMarkerNeutral[ipa.site]);

            d3.selectAll(".popCircle").attr("class", function(d, i) {
                return "popCircle pop" + i;
            }).style('fill', colours.popCircleNeutral[ipa.site]);
        };

        $scope.setSelection = function(dataSet) {
            $scope.currentDataSetName = dataSet;

            var svg = d3.select("#viz");
            svg.selectAll("div")
                .transition()
                .duration(1000)
                .style('opacity', 0)
                .remove();
            setTimeout(function() {
                if (dataNo === 0) {
                    $scope.chart(
                        (aeaMainData || ipaMainData)[0][dataSet],
                        dataSet
                    );
                } else {
                    $scope.chart(data[dataNo][dataSet], dataSet);
                }
            }, 1001);
        };

        var width = 360;

        // var svg = d3.select(".map-grid")
        $scope.chart = function(_data, dataSet) {
            var searchGroupsByDataSet = {
                'genders': 'gender',
                'treatments': 'all_arrests_prison_treatments',
                'activities': 'all_arrests_activities',
                'charges': 'all_arrests_charges',
                'religions': 'religion',
                'ethnicities': 'ethnicity',
            };

            var searchGroup = searchGroupsByDataSet[dataSet] || '';

            $scope.$apply(function() {
                $scope.unknown = 0;
            });

            var data = [];

            angular.forEach(_data, function(v, k) {
                if (k !== "Unknown") {
                    var obj = {};
                    obj.count = v;
                    obj.name = k;
                    data.push(obj);
                } else {
                    $scope.$apply(function() {
                        $scope.unknown = v;
                    });
                }
            });
            data.sort(function(a, b) {
                return b.count - a.count;
            });

            var svg = d3.select("#viz").append("div");
            state = svg.selectAll(".state")
                .data(data)
                .enter().append("div")
                .attr("class", "col-md-12 col-sm-6 ")
                .append('div')
                .attr('class', 'barHolder barHolderPrison')
                .style('opacity', 0);



            width = $(".barHolder").width();

            var x = d3.scale.ordinal()
                .rangeRoundBands([0, width], 0.1);

            var y = d3.scale.linear()
                .range([width, 0]);

            var xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom");

            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left")
                .ticks(10, "%");

            var titles = state.append("a")
                .attr("x", 0)
                .attr("y", 0)
                .attr('class', 'title')
                .attr('href', function(d) {

                    var searchQ = searchGroup ? searchGroup + '=' + d.name : '';
                    var prison = $scope.name == all ? '&detention_status=true' : '&current_prison=' + $scope.name;
                    return '/' + ipa.lang + '/search/#/?data=prisoners&' + searchQ + prison;
                })
                .attr('target', '_blank')
                .html(function(d, k) {

                    return d.name + "<span class='totalNo' >" + d.count + "</span>";
                });

            y.domain([0, d3.max(data, function(d) {
                return d.count;
            })]);

            svg.selectAll(".barHolder")
                .append("div")
                .attr("class", "barPrisonMarker")
                .style("width", width);


            svg.selectAll(".barHolder")
                .append("div")
                .attr("class", "barPrisonPadder");


            $(".barPrisonMarker").width(width);

            svg.selectAll(".barHolder")
                .append("svg")
                .attr("width", 1000)
                .attr("height", '15px')
                .attr("class", "barPrison")
                .append("rect")
                .attr('x', width)
                .attr("class", "barPrisonRect")
                .attr("height", 15)
                .attr("width", 0)
                .attr('ry', 7)
                .attr('rx', 7)
                .style("fill", function(d, i) {
                    return colorsRange[i];
                })
                .transition()
                .delay(1000)
                .duration(1000)
                .attr("width", function(d) {

                    return width - y(d.count);
                })
                .attr('x', function(d) {

                    return width - (width - y(d.count));
                });

            state.transition()
                .delay(100)
                .duration(1000)
                .style('opacity', 1);

            $(window).resize(function() {
                $('.mapPort').width(($('.container').width() * 0.66) + 30);
                $(".mapPort").height($(window).height() * 0.7);
                var svg = d3.select("#viz");
                width = $(".barHolder").width();
                $(".barPrisonMarker").width(width);

                var y = d3.scale.linear()
                    .range([width, 0]);

                var yAxis = d3.svg.axis()
                    .scale(y)
                    .orient("left")
                    .ticks(10, "%");
                y.domain([0, d3.max(data, function(d) {
                    return d.count;
                })]);


                svg.selectAll(".barPrisonRect")
                    .attr("width", function(d) {
                        return width - y(d.count);
                    })
                    .attr('x', function(d) {
                        return width - (width - y(d.count));
                    });

                $panzoom.panzoom("resetDimensions");
            });
        };

        $(document).ready(function() {
            width = $(".barHolder").width();
            $('.mapPort').width(($('.container').width() * 0.66) + 30);
            $(".barPrisonMarker").width(width);
            $scope.chart(
                (aeaMainData || ipaMainData)[dataNo][defaultDataSetName],
                defaultDataSetName
            );
            $(".mapPort").height($(window).height() * 0.7);
            $panzoom.panzoom("resetDimensions");

            window.scrollBy(0, 1);
        });
    });
}());
