(function () { 'use strict'; window.ipa = window.ipa || {};

class InformationOverlay extends Stimulus.Controller {
    // ======================
    // === Initialization ===
    // ======================

    connect() {
        /* jshint ignore:start */

        /** @type {HTMLDivElement} */
        this.element;

        /** @type {HTMLDivElement} */
        this.overlayTarget;

        /* jshint ignore:end */

        /** @type {string} */
        this.slug = this.data.get('slug');

        /** @type {string} */
        this.instanceDisplayName = this.slug;

        ipa.utils.addEventListener(
            'InformationOverlayTriggerButton_click',
            this.onInformationOverlayTriggerButtonClick.bind(this)
        );
    }

    // ======================
    // === Event handlers ===
    // ======================

    /**
     * @param {MouseEvent} event
     */
    onClick(event) {
        if (event.target !== this.overlayTarget) {
            return false;
        }

        this.overlayTarget.classList.remove('isVisible');
    }

    /**
     * @param {MouseEvent} event
     */
    onCloseButtonClick(event) {
        this.close();
    }

    /**
     * @param {ipa.InformationOverlayTriggerButtonClickedEvent} event
     */
    onInformationOverlayTriggerButtonClick(event) {
        if (event.detail.informationOverlaySlug !== this.slug) {
            return false;
        }

        this.open();
    }

    // ===============
    // === Methods ===
    // ===============

    close() {
        this.overlayTarget.classList.remove('isVisible');
    }

    open() {
        this.overlayTarget.classList.add('isVisible');
    }
}

InformationOverlay.displayName = 'InformationOverlay';
InformationOverlay.targets = ['overlay'];

ipa.InformationOverlay = InformationOverlay;

})();
