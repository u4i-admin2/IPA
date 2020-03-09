(function () { 'use strict';

// Ensure that code runs as entire document is parsed, but no sooner
if (document.readyState === 'interactive' || document.readyState === 'complete') {
    new ipa.Ipa();
} else {
    document.onreadystatechange = function () {
        if (document.readyState === 'interactive' || document.readyState === 'complete') {
            document.onreadystatechange = null;
            console.info('Document parsed – initializing.');
            new ipa.Ipa();
        }
    };
}

})();
