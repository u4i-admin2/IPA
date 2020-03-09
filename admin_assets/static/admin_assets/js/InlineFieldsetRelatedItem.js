(function () { 'use strict';

window.ipaAdmin.InlineFieldsetRelatedItem = class InlineFieldsetRelatedItem {
    /**
     * @param {HTMLDivElement} element
     * @param {boolean} shouldBeCollapsible
     * @param {boolean shouldBeExpanded}
     */
    constructor(
        element,
        shouldBeCollapsible = false,
        shouldBeExpanded = false
    ) {
        // ==============================
        // === Get element references ===
        // ==============================
        /** @type {HTMLDivElement} */
        this.element = element;

        /** @type {HTMLHeadingElement} */
        this.headingElement = this.element.querySelector('h3');

        /** @type {HTMLSpanElement} */
        this.headingInlineLabelElement = this.headingElement.querySelector('.inline_label');

        /** @type {HTMLSpanElement} */
        this.headingDeleteContainerElement = this.headingElement.querySelector('.delete');

        // =========================
        // === Get initial state ===
        // =========================
        /** @type {string} */
        this.headingInlineLabelElementOriginalText = (
            this.headingInlineLabelElement.textContent
        );

        /** @type {boolean} */
        this.isExpanded = (
            this.element.querySelector('.errorlist') instanceof HTMLElement ||
            shouldBeExpanded
        );

        // ========================================
        // === Bind syncPropertiesWithClassName ===
        // ========================================
        this.syncPropertiesWithClassName = (
            window.ipaAdmin.utils.syncPropertiesWithClassName.bind(
                this,
                this.element,
                [
                    'isExpanded',
                ]
            )
        );

        // =============================
        // === Set up collapsibility ===
        // =============================
        if (shouldBeCollapsible) {
            this.setUpCollapse();
        }

        // ==========================================
        // === Initialize contained DateFieldsets ===
        // ==========================================
        const dateFieldsetElements = this.element.querySelectorAll('.dateFieldset');

        for (const dateFieldsetElement of dateFieldsetElements) {
            new ipaAdmin.DateFieldset(dateFieldsetElement);
        }

        // ============================================================
        // === Set data-inline-fieldset-related-item-is-initialized ===
        // ============================================================
        //
        // This is used in InlineFieldset’s MutationObserver to
        // determine if an .inline-related already has an associated
        // InlineFieldsetRelatedItem instance. django-nested-admin’s
        // drag-and-drop sorting functionality can trigger mutation
        // events on existing elements.
        this.element.setAttribute(
            'data-inline-fieldset-related-item-is-initialized',
            ''
        );
    }

    setUpCollapse() {
        this.updateHeading();

        this.headingElement.addEventListener(
            'click',
            this.onHeadingElementClick.bind(this),
            false
        );

        this.syncPropertiesWithClassName();
    }

    updateHeading() {
        this.headingInlineLabelElement.textContent = (
            this.isExpanded
                ? `${this.headingInlineLabelElementOriginalText} (Hide)`
                : `${this.headingInlineLabelElementOriginalText} (Show)`
        );
    }

    /**
     * @param {Event} event
     */
    onHeadingElementClick(event) {
        if (
            this.headingDeleteContainerElement instanceof HTMLElement &&
            this.headingDeleteContainerElement.contains(event.target)
        ) {
            return;
        }

        this.isExpanded = !this.isExpanded;

        this.updateHeading();
        this.syncPropertiesWithClassName();
    }
};

})();
