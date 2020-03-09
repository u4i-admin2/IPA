(function() {
    "use strict";
    var sortedData = [];
    var prisonersSquare = [];


    // default data selection

    var yAxisNameSet = 'activity';
    var xAxisNameSet = 'ethnicity';
    var xAxisNameRoot = 'ethnicity';


    var totalUnknown = 0;

    var colorsRange = ipa.colorsRange;



    var load = true;


    var selected = null;



    var filters = [];


    $('.filterTab').on("tap", function() {
        console.log("sfhksdhf");
        $(".filterTab").toggleClass('on');
        $(".statusArea").toggleClass('on');
    });

    $('.filterHearder').on("tap", function() {
        $(".filterTab").toggleClass('on');
        $(".statusArea").toggleClass('on');
    });

    $(document).mouseup(function(e) {
        var container = $(".dropDownBtn");

        if (!container.is(e.target) && container.has(e.target).length === 0) {
            container.parent().find('.dropMenu').slideUp();
            container.children().removeClass('down');
        }
    });



    $(document).on("click", '.dropDownBtn', function() {

        $(this).parent().find('.dropMenu').slideToggle();
        $(this).children().toggleClass('down');

    });

    var menuIcon = '<span class="menuIcon"><span class="icon-up-dir"></span><span class="icon-down-dir"></span></span>';

    $('.dropMenu li ').on('click', function() {
        $(this).parent().slideUp();

        $(this).parent().parent().find('.dropDownBtn').html($(this).html() + menuIcon);


    });


    UFIF.controller('prisoners', function($scope, $timeout, $http, $location) {
        $scope.url = $location.absUrl();
        $scope.xAxisNameSet = 'ethnicity';
        $scope.yAxisNameSet = 'activity';

        $scope.detention_stats = detention_stats;

        $scope.colorsRange = colorsRange;

        $scope.getColor = function(c) {
            return $scope.colorsRange[c];

        };



        $scope.regexAz = function(str) {

            return str.replace(/[^\w]/g, ' ').replace(/\s/g, '');
        };


        $scope.filterReset = true;


        $scope.newValue = function(value, i) {
            if ($scope.filterReset) {
                filters = [];
                $scope.filterReset = false;
            }

            $("#dot" + i).toggleClass('checked');

            var index = filters.indexOf(value);
            if (index !== -1) {
                filters.splice(index, 1);
            } else {
                filters.push(value);
            }


            if (!filters.length) {


                angular.forEach(mainData[xAxisNameRoot], function(_value, _key) {

                    if (_key != 'null' && _key != 'State') {
                        filters.push(_key);

                    }

                });
                $scope.filterReset = true;


            }

            $scope.setData();


            filterViz();

        };

        // on select events
        $scope.setAxisY = function(axis) {
            $('.blocker').show();

            $('.filterColors').removeClass('checked');


            yAxisNameSet = axis;
            setFilters();
            $scope.setData();
            setTimeout(renderViz(), 100);
            $(".switchHolder").removeClass("on");
            $(".DETAINED").addClass("on");
            $scope.filterReset = true;
            $scope.switchArray = ['DETAINED'];
            $scope.statusArray = ['DETAINED'];
        };
        $scope.setAxisX = function(axis) {
            $('.filterColors').removeClass('checked');
            $('.blocker').show();

            xAxisNameSet = axis;
            xAxisNameRoot = axis;
            setFilters();
            $scope.setData();
            setTimeout(renderViz(), 100);
            $(".switchHolder").removeClass("on");
            $(".DETAINED").addClass("on");
            $scope.filterReset = true;
            $scope.switchArray = ['DETAINED'];
            $scope.statusArray = ['DETAINED'];
        };



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

            } else {
                $(".switchHolder").removeClass("on");
                $("." + status).addClass("on");
                $scope.switchArray = [];

                $scope.statusArray = ['DETAINED', 'UNKNOWN', 'RELEASED', 'PASSED_AWAY', 'EXECUTED'];
            }



            $scope.setData();

            setTimeout(renderViz(), 100);
        };

        setFilters();
        // sort data to correct format for each data set
        function setFilters() {
            $scope.lookUpArray = [];
            filters = [];

            angular.forEach(mainData[xAxisNameRoot], function(_value, _key) {

                if (_key != 'null' && _key != 'State') {
                    $scope.lookUpArray.push(_key);
                    filters.push(_key);

                }

            });


        }

        $scope.setData = function() {
            console.log(filters);
            $scope.unknown = 0;

            $scope.xAxisNameSet = xAxisNameSet;
            $scope.yAxisNameSet = yAxisNameSet;
            totalUnknown = 0;

            prisonersSquare = [];
            sortedData = [];
            var yAxis = mainData[yAxisNameSet];
            var xAxis = mainData[xAxisNameRoot];

            var num = 0;

            xAxisNameSet = xAxisNameSet == 'activity' ? 'latest_activity' : xAxisNameSet;
            xAxisNameSet = xAxisNameSet == 'mistreatments' ? 'treatments' : xAxisNameSet;
            xAxisNameSet = xAxisNameSet == 'sentences' ? 'sentence' : xAxisNameSet;


            console.log(xAxisNameSet);


            angular.forEach(yAxis, function(value, key) {




                var tempOBJ = {
                    'State': key
                };

                var colors = [];

                angular.forEach(xAxis, function(_value, _key) {


                    tempOBJ[_key] = [];


                });



                angular.forEach(value, function(_value, i) {



                    if (xAxisNameSet == 'charges' || xAxisNameSet == 'treatments') {
                        // console.log(prisoner_lookup[_value][xAxisNameSet])
                        angular.forEach(prisoner_lookup[_value][xAxisNameSet], function(_v, _i) {




                            if (prisoner_lookup[_value][xAxisNameSet].length > 1 && filters.indexOf(_v) !== -1) {

                                if ($scope.statusArray.indexOf(prisoner_lookup[_value].detention_status) != -1) {
                                    tempOBJ[_v].push(_value);
                                }
                            }
                        });
                    } else if (xAxisNameSet == 'sentence') {
                        if (prisoner_lookup[_value][xAxisNameSet]) {
                            angular.forEach(tempOBJ, function(_v, _k) {


                                if (prisoner_lookup[_value][xAxisNameSet][_k] && filters.indexOf(_k) !== -1) {

                                    if ($scope.statusArray.indexOf(prisoner_lookup[_value].detention_status) != -1) {
                                        tempOBJ[_k].push(_value);
                                    }
                                }
                            });
                        }

                    } else {
                        if (prisoner_lookup[_value][xAxisNameSet] && filters.indexOf(prisoner_lookup[_value][xAxisNameSet]) !== -1) {

                            if ($scope.statusArray.indexOf(prisoner_lookup[_value].detention_status) != -1) {
                                tempOBJ[prisoner_lookup[_value][xAxisNameSet]].push(_value);
                            }
                        }
                    }
                });


                tempOBJ['null'] = [];


                var secondTemp = [];


                angular.forEach(tempOBJ, function(_value, i) {

                    angular.forEach(_value, function(_v, _k) {

                        if (_v > 0) {

                            if (i != 'null' && i != 'State') {
                                colors.push(i);
                            }
                        }
                        if (_v > 0) {
                            if (i != 'null' && i != 'State') {
                                secondTemp.push(_v);
                            }
                        }


                    });

                });


                tempOBJ.prisonersSquare = secondTemp;
                tempOBJ.colors = colors;

                if (key !== 'Unknown') {
                    sortedData[num] = tempOBJ;
                    num++;
                } else {
                    $scope.unknown = tempOBJ.prisonersSquare.length;
                }

            });



            // wait for data sort completion just incase



        };





        // render default data set








        var graphOrder = [];

        var margin,
            x,
            y,
            color,
            xAxis,
            yAxis,
            svg,
            width,
            height;







        // graphe basic vars set

        $(document).ready(function() {

            graphOrder = [];
            margin = {
                top: 0,
                right: 17,
                bottom: 0,
                left: 17
            };
            width = $('.container').width() - margin.left - margin.right;
            height = 3000 - margin.top - margin.bottom;

            x = d3.scale.ordinal()
                .rangeRoundBands([0, height], 0.1);

            y = d3.scale.linear()
                .rangeRound([width, 0]);

            color = d3.scale.ordinal()
                .range(colorsRange);

            xAxis = d3.svg.axis()
                .scale(x)
                .orient("bottom");

            yAxis = d3.svg.axis()
                .scale(y)
                .orient("left")
                .tickFormat(d3.format(".2s"));

            svg = d3.select("#viz").append("div");
            // .attr("width", width + margin.left + margin.right)
            // .attr("height", height + margin.top + margin.bottom)
            // .append("g")
            // .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

            $scope.switchArray = [];
            $scope.statusArray = ['DETAINED', 'UNKNOWN', 'RELEASED', 'PASSED_AWAY', 'EXECUTED'];

            $scope.setData();

            $scope.switchArray = ['DETAINED'];
            $scope.statusArray = ['DETAINED'];

            $scope.setData();

            setTimeout(renderViz(), 100);
        });


        var tt = $('.toolTipHolder');

        $(document).mousemove(function(event) {


            tt.height();
            // tt.css('top', event.pageY - tt.height() - 15)
            // tt.css('left', event.pageX - 15)

        });





        var totts = 0;
        var state;
        var data;
        var activeRenderTimeoutId;

        function filterViz() {
            data = sortedData;
            var currentData = data[0].State;
            var currentColor = 0;


            color.domain(d3.keys(data[0]).filter(function(key) {
                return key !== "State" && key !== "prisonersSquare" && key !== "colors";
            }));

            data.forEach(function(d) {

                var y0 = 0;
                d.ages = color.domain().map(function(name) {
                    return {
                        name: name,
                        y0: y0,
                        y1: y0 += +d[name].length
                    };
                });

                d.total = d.ages[d.ages.length - 1].y1;

            });

            var dataTemp = [];
            data.sort(function(a, b) {

                return b.total - a.total;
            });
            height = ((Math.ceil(data[0].prisonersSquare.length * 17) / width) * 17);

            angular.forEach(graphOrder, function(_value, _key) {
                angular.forEach(data, function(_v, _k) {
                    if (_v.State == _value) {
                        dataTemp.push(_v);
                    }
                });
            });

            data = dataTemp;





            x.domain(data.map(function(d) {
                return d.State;
            }));
            width = $('.container').width() - margin.left - margin.right;

            var y = d3.scale.linear()
                .rangeRound([width, 0]);
            var yAxis = d3.svg.axis()
                .scale(y)
                .orient("left")
                .tickFormat(d3.format(".2s"));

            y.domain([0, d3.max(data, function(d) {
                return d.total;
            })]);

            svg.selectAll('.squares').selectAll(".square")
                .transition()
                .duration(1)
                .delay(function(d, i) {
                    return i;
                })
                .style("opacity", 0)
                .style("display", "none");




            $(".totalNo").each(function(i) {
                $(this).html(data[i].total);
            });


            state.selectAll('.squares').transition()
                .duration(500)
                // .delay(_delay)
                .attr("height", function() {
                    if ($(this).height() > 0) {
                        return height + 14;
                    } else {
                        return 0;
                    }
                });


            state.selectAll(".bar")
                .data(data)
                .selectAll('.vizSection')
                .data(function(d, i) {
                    return data[i].ages;
                })
                .transition()
                .duration(700)
                .attr("height", 35)
                .attr("x", function(d, i) {
                    return width - y(d.y0);
                })
                .attr("width", function(d) {

                    return y(d.y0) - y(d.y1);
                });

            svg.selectAll('.squares')
                .data(data)
                // .transition()
                // .duration(500)
                // // .delay(_delay)
                // .attr("height", function() {
                //     if ($(this).height() > 0) {
                //         return height + 14
                //     } else {
                //         return 0
                //     }
                // })
                .selectAll(".square")
                .data(function(d, i) {

                    return data[i].prisonersSquare;
                })
                .attr("data-id", function(d) {

                    return d;
                })
                .transition()
                .style("display", "block")
                .duration(1)
                .delay(function(d, i) {

                    return i * 3;
                })
                .attr('y', function(d, i) {
                    var nextRow = Math.floor(i / (Math.ceil(height / 17)));
                    var _height = Math.ceil(height / 17) * 17;
                    return (i * 17) - (_height * nextRow);
                })
                .attr('x', function(d, i) {
                    var _height = Math.ceil(height / 17) * 17;
                    return (Math.ceil((i + 1) / (_height / 17)) * 17) - 17;
                }).style("fill", function(d, i) {

                    var parentData = d3.select(this.parentNode).datum();

                    console.log(selected == d);

                    if (selected == d) {
                        return "#EFA954";

                    } else {
                        return color(parentData.colors[i]);
                    }



                }).style("opacity", 1);

        }





        function renderViz() {



            // set up the data set
            data = sortedData;


            var currentData = data[0].State;
            var currentColor = 0;

            color.domain(d3.keys(data[0]).filter(function(key) {
                return key !== "State" && key !== "prisonersSquare" && key !== "colors";
            }));

            data.forEach(function(d) {

                var y0 = 0;
                d.ages = color.domain().map(function(name) {
                    return {
                        name: name,
                        y0: y0,
                        y1: y0 += +d[name].length
                    };
                });

                d.total = d.ages[d.ages.length - 1].y1;

            });

            data.sort(function(a, b) {
                return b.total - a.total;
            });

            graphOrder = [];
            angular.forEach(data, function(_value, _key) {

                graphOrder.push(_value.State);
            });

            x.domain(data.map(function(d) {
                return d.State;
            }));
            y.domain([0, d3.max(data, function(d) {
                return d.total;
            })]);


            $(window).resize(function() {
                width = $('.container').width() - margin.left - margin.right;

                height = ((Math.ceil(data[0].prisonersSquare.length * 17) / width) * 17);
                var y = d3.scale.linear()
                    .rangeRound([width, 0]);
                var yAxis = d3.svg.axis()
                    .scale(y)
                    .orient("left")
                    .tickFormat(d3.format(".2s"));

                y.domain([0, d3.max(data, function(d) {
                    return d.total;
                })]);


                svg.selectAll(".vizSection")
                    .transition()
                    .duration(700)
                    .attr("height", 35)
                    .attr("x", function(d) {
                        return width - y(d.y0);
                    })
                    .attr("width", function(d) {
                        return y(d.y0) - y(d.y1);
                    });



                svg.selectAll('.squares').transition()
                    .duration(500)
                    // .delay(_delay)
                    .attr("height", function() {
                        if ($(this).height() > 0) {
                            return height + 14;
                        } else {
                            return 0;
                        }
                    }).selectAll(".square")
                    .transition()
                    .duration(1)
                    .delay(function(d, i) {
                        return i * 3;
                    })
                    .attr('y', function(d, i) {
                        var nextRow = Math.floor(i / (Math.ceil(height / 17)));
                        var _height = Math.ceil(height / 17) * 17;
                        return (i * 17) - (_height * nextRow);
                    })
                    .attr('x', function(d, i) {
                        var _height = Math.ceil(height / 17) * 17;
                        return (Math.ceil((i + 1) / (_height / 17)) * 17) - 17;
                    });


            });



            // reset page for each new result
            svg.selectAll(".vizSection")
                .transition()
                .duration(2000)
                .attr("height", 35)
                .attr("x", 0)
                .attr("width", 0)
                .remove();

            svg.selectAll(".title")
                .transition()
                .duration(2000)
                .style('opacity', 0)
                .remove();


            svg.selectAll('.squares').selectAll(".square")
                .transition()
                .duration(1)
                .delay(function(d, i) {
                    return i;
                })
                .style("opacity", 0)
                .remove();

            svg.selectAll('.barHolder')
                .style("opacity", 1)
                .transition()
                .duration(500)
                .delay(1500)
                .style("opacity", 0)
                .remove();

            clearTimeout(activeRenderTimeoutId);

            // render new graph set and wait for reset
            activeRenderTimeoutId = setTimeout(function() {
                var _classNum = 0;

                height = ((Math.ceil(data[0].prisonersSquare.length * 17) / width) * 17);

                state = svg.selectAll(".state")
                    .data(data)
                    .enter().append("div")
                    .attr("class", "barHolder")
                    .attr("transform", function(d, i) {
                        return "translate( 0 ," + ((height + 100) * i) + ")";
                    })
                    .style("opacity", 0);


                svg.selectAll(".barHolder")
                    .transition()
                    .duration(500)
                    .style("opacity", 1);


                var titles = state.append("div")
                    .attr("x", 0)
                    .attr("y", 0)
                    .attr('class', 'title')
                    .attr('data-id', function(d, i) {
                        return i;
                    })
                    .on("click", function() {
                        expand(this);
                    })
                    .style('opacity', 0)
                    .html(function(d) {
                        return "<span class='icon-right-dir hideOnMobile ' ></span><span class='icon-down-dir hideOnMobile' style='display:none' ></span>" + d.State + "<span class='totalNo' >" + d.prisonersSquare.length + "</span>";
                    })
                    .transition()
                    .duration(2000)
                    .style('opacity', 1);

                state.append("svg")
                    .attr('width', 1400)
                    .attr('height', 0)
                    .attr('x', 0)
                    .attr('class', function(d, i) {
                        // var parentData = d3.select(this.parentNode).datum();
                        // parentData['State'];

                        return 'squares ' + 'squares' + i;
                    })
                    .attr('data-id', function(d, i) {

                        return i;
                    })
                    .selectAll(".squareholder")
                    .data(function(d, i) {

                        return d.prisonersSquare;
                    })
                    .enter()
                    .append("rect")
                    .attr('width', 15)
                    .attr('height', 15)
                    .attr('y', function(d, i) {
                        var nextRow = Math.floor(i / (Math.ceil(height / 17)));
                        var _height = Math.ceil(height / 17) * 17;
                        return (i * 17) - (_height * nextRow);
                    })
                    .attr('x', function(d, i) {
                        var _height = Math.ceil(height / 17) * 17;
                        return (Math.ceil((i + 1) / (_height / 17)) * 17) - 17;
                    })
                    .attr('rx', 3)
                    .attr('ry', 3)
                    .attr('data-id', function(d) {
                        return d;
                    })
                    .attr('class', function(d, i) {
                        var parentData = d3.select(this.parentNode).attr('data-id');

                        return 'square square' + parentData;
                    })
                    .style("fill", function(d, i) {

                        var parentData = d3.select(this.parentNode).datum();

                        return color(parentData.colors[i]);

                    })
                    .on("mouseover", function() {


                        var dataSet = prisoner_lookup[$(this).data('id')];
                        var picture = (
                          dataSet.picture !== ''
                            ? dataSet.picture // jshint ignore:line
                            : ipa.staticPrefix + 'public/img/profile_temp.png?v=2019-08-28'
                        );
                        $('.profileImage').attr('src', picture);
                        $('.name').html(dataSet.forename + " " + dataSet.surname);

                        $('.activePersecutedFor').html(dataSet.latest_activity);
                        if (dataSet.sentence) {
                            if (dataSet.sentence.executed) {
                                $(".excecuted").show();
                            } else {
                                $(".excecuted").hide();
                            }
                        }
                        $('.sentance').html(dataSet.sentence);

                        tt.stop();
                        tt.height();
                        tt.css('top', event.pageY - tt.height() - 15);
                        tt.css('left', event.pageX - 15);
                        tt.fadeIn(200);

                    })
                    .on("mouseout", function() {
                        tt.stop();
                        tt.fadeOut(200);

                    })
                    .on("click", function(d) {

                        selected = d;
                        svg.selectAll('.squares')
                            .data(data)
                            .selectAll(".square")
                            .data(function(d, i) {

                                return data[i].prisonersSquare;
                            })
                            .attr("data-id", function(d) {

                                return d;
                            })
                            .transition()
                            .style("display", "block")
                            .duration(1)
                            .delay(function(d, i) {

                                return i * 3;
                            })
                            .attr('y', function(d, i) {
                                var nextRow = Math.floor(i / (Math.ceil(height / 17)));
                                var _height = Math.ceil(height / 17) * 17;
                                return (i * 17) - (_height * nextRow);
                            })
                            .attr('x', function(d, i) {
                                var _height = Math.ceil(height / 17) * 17;
                                return (Math.ceil((i + 1) / (_height / 17)) * 17) - 17;
                            }).style("fill", function(d, i) {

                                var parentData = d3.select(this.parentNode).datum();

                                console.log(selected == d);

                                if (selected == d) {
                                    return "#EFA954";

                                } else {
                                    return color(parentData.colors[i]);
                                }



                            }).style("opacity", 1);

                        window.open('../prisoner/' + $(this).data('id') + '/', '_blank');

                    })
                    .style("opacity", 0)
                    .transition()
                    .duration(1)
                    .delay(function(d, i) {
                        return i * 3;
                    })
                    .style("opacity", 0);


                state.append("svg")
                    .attr('width', 1400)
                    .attr('height', 35)
                    .attr('data-on', true)
                    .attr('opacity', 1)
                    .attr('class', function(d, i) {

                        return 'bar bar' + i;
                    })
                    .selectAll("rect")
                    .data(function(d) {
                        return d.ages;
                    })
                    .enter().append("rect")
                    .attr("class", "vizSection")
                    .attr("height", 35)
                    .attr("x", 0)
                    .attr("width", 0)
                    .style("fill", function(d) {
                        return color(d.name);
                    })
                    .transition()
                    .duration(2000)
                    .attr("height", 35)
                    .attr("x", function(d) {
                        return width - y(d.y0);
                    })
                    .attr("width", function(d) {

                        return y(d.y0) - y(d.y1);
                    });


                $('.blocker').hide();



            }, 2100);

            function expand(_this) {

                var maxPrisonersSquares = data[0].total;
                for (var i = 0; i < data.length; i++) {
                    if (data[i].total > maxPrisonersSquares)
                        maxPrisonersSquares = data[i].total;
                }

                height = ((Math.ceil(maxPrisonersSquares * 17) / width) * 17);

                var id = $(_this).data('id');
                var bar = state.select('.bar' + id);

                var on = $(_this).data('on');

                var _opacity = on ? 0 : 1;
                var _height = on ? 0 : height + 14;
                var _delay = on ? 1 : 1000;
                var _h = on ? 35 : 0;
                var _o = on ? 1 : 0;
                var _d = on ? 1000 : 1;

                bar.transition()
                    .duration(_d)
                    // .delay(_d)
                    .attr("opacity", _o);
                // .attr("height", _h)

                $(_this).toggleClass('open');
                $(_this).children(".icon-right-dir").toggle();
                $(_this).children(".icon-down-dir").toggle();



                state.selectAll('.squares' + id).transition()
                    .duration(500)
                    // .delay(_delay)
                    .attr("height", _height);



                svg.selectAll('.squares')
                    .data(data)
                    .selectAll('.square' + id)
                    .data(function(d, i) {

                        return data[i].prisonersSquare;
                    }).transition()
                    .duration(1)
                    .delay(function(d, i) {
                        return (i * 3);
                    })
                    .style("opacity", _opacity);
                var newon = on ? false : true;

                $(_this).data('on', newon);
            }
        }
    });
}());
