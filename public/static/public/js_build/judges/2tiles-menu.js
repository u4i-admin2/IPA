smallmedia.tilesMenu = (function(){
  var my = {};

  var config = {
  };

  var state = {
    selected: 0
  };

  var elements = {
  };

  var items = [];

  if (ipa.site === 'aea') {
    items = [
      { category: 'total_victims', label: 'Victims' },
      { category: 'total_amputation', label: 'Amputations' },
      { category: 'total_executions', label: 'Death Penalty' },
      { category: 'total_flogging', label: 'Floggings' },
      { category: 'total_mistreatments', label: 'Misconduct' }
    ];
  } else if (ipa.site === 'ipa') {
    items = [
      { category: 'total_verdicts', label: 'Verdicts' },
      { category: 'total_years', label: 'Sentence (yrs)' },
      { category: 'average_years', label: 'Sentence (avg)' },
      { category: 'total_executions', label: 'Death Penalty' },
      { category: 'total_lashes', label: 'Lashes' },
      { category: 'total_mistreatments', label: 'Misconduct' }
    ];
  }

  var enFa = smallmedia.tilesVisLanguage.enFa;

  /*-------
  CONSTRUCT
  -------*/
  function construct() {
    elements.menu = d3.select(config.container)
      .append('div');

    var u = elements.menu
      .selectAll('div.item')
      .data(items);

    u.enter()
      .append('div')
      .classed('item', true)
      .classed('selected', function(d, i) {
        return i === state.selected;
      })
      .classed('contains-information-box', function (d, i) {
        return ['total_lashes', 'total_mistreatments'].includes(d.category);
      })
      .on('click', function(d, i) {
        if (d3.event.target.classList.contains(
          'ipa-information-overlay-trigger-button'
        )) {
          return;
        }

        state.selected = i;
        updateSelectedClassnames();
        config.click(d);
      })
      .html(function(d) {
        var html = '<p>' + enFa(d.label) + '</p>';

        if (d.category === 'total_lashes') {
          html += judgesPrerenderedComponentHtml.informationOverlayTriggerButton.lashes;
        } else if (d.category === 'total_mistreatments') {
          html += judgesPrerenderedComponentHtml.informationOverlayTriggerButton.misconduct;
        }

        return html;
      });
  }

  function updateSelectedClassnames() {
    elements.menu
      .selectAll('div.item')
      .data(items)
      .classed('selected', function(d, i) {
        return i === state.selected;
      });
  }

  /*-
  API
  -*/
  my.init = function(conf) {
    config = _.extend(config, conf);

    construct();
  };

  my.setWidth = function(width) {
    config.width = width;
  };

  my.setNumberOfCols = function(cols) {
    config.numCols = cols;
  };

  return my;
}());
