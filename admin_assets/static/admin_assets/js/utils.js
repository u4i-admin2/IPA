(function () { 'use strict';

window.ipaAdmin.utils = {};

window.ipaAdmin.utils.syncPropertiesWithClassName = function(elem, propertyNames) {
    var className = elem.className;
    var i;
    var propertyClassNameSegment;
    var propertyName;
    var regExpMatch;

    for (i = 0; i < propertyNames.length; i++) {
        propertyName = propertyNames[i];

        propertyClassNameSegment = null;
        if (this[propertyName] === true) {
            propertyClassNameSegment = propertyName;
        } else if (
            typeof this[propertyName] === 'string' ||
            typeof this[propertyName] === 'number'
        ) {
            propertyClassNameSegment = propertyName + '-' + this[propertyName];
        }

        regExpMatch = className.match('(' + propertyName + '-?[^\\s]*)(?:\\s|$)');
        if (Array.isArray(regExpMatch) && propertyClassNameSegment === null) {
            className = className.replace(regExpMatch[1], '');
        } else if (Array.isArray(regExpMatch)) {
            className = className.replace(
                regExpMatch[1],
                propertyClassNameSegment
            );
        } else if (!Array.isArray(regExpMatch) && propertyClassNameSegment) {
            className += (' ' + propertyClassNameSegment);
        }
    }

    elem.className = className;
};

})();
