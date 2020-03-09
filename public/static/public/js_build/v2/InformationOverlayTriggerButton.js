(function () { 'use strict'; window.ipa = window.ipa || {};

class InformationOverlayTriggerButton extends Stimulus.Controller {
    // ======================
    // === Initialization ===
    // ======================

    connect() {
        /* jshint ignore:start */

        /** @type {HTMLButtonElement} */
        this.element;

        /* jshint ignore:end */

        /** @type {string} */
        this.informationOverlaySlug = this.data.get('informationOverlaySlug');
    }

    // ======================
    // === Event handlers ===
    // ======================

    /**
     *
     * @param {MouseEvent} event
     */
    onClick(event) {
        ipa.utils.dispatchEvent(
            'InformationOverlayTriggerButton_click',
            {
                informationOverlaySlug: this.informationOverlaySlug,
            }
        );
    }
}

InformationOverlayTriggerButton.displayName = 'InformationOverlayTriggerButton';
InformationOverlayTriggerButton.targets = [];

ipa.InformationOverlayTriggerButton = InformationOverlayTriggerButton;

})();
