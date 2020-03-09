(function () { 'use strict'; window.ipa = window.ipa || {};

function Ipa() {
    this.init();
}

Ipa.prototype.init = function () {
    var stimulusApplication = Stimulus.Application.start();

    stimulusApplication.register(
        'ipa-information-overlay',
        ipa.InformationOverlay
    );

    stimulusApplication.register(
        'ipa-information-overlay-trigger-button',
        ipa.InformationOverlayTriggerButton
    );
};

ipa.Ipa = Ipa;

})();
