(function () { 'use strict';

window.ipaAdmin.InlineFieldset = class InlineFieldset {
    /** @param {HTMLFieldSetElement} element */
    constructor(element) {
        this.element = element;

        /** @type {HTMLDivElement} */
        this.relatedItemsContainer = this.element.querySelector('.djn-items');

        /** @type {Array<HTMLDivElement>} */
        this.relatedItemElements = this.relatedItemsContainer.querySelectorAll('.inline-related:not(.empty-form)');

        /** @type {boolean} */
        this.relatedItemsShouldBeCollapsible = (
            this.element.classList.contains('fieldsetInlineRelatedItemsCollapsible')
        )

        for (const relatedItem of this.relatedItemElements) {
            if (
                relatedItem.getAttribute(
                    'data-inline-fieldset-related-item-is-initialized'
                ) === null
            ) {
                new ipaAdmin.InlineFieldsetRelatedItem(
                    relatedItem,
                    this.relatedItemsShouldBeCollapsible,
                    false,
                );
            }
        }

        this.relatedItemElementObserver = new MutationObserver(
            this.onElementMutations.bind(this)
        );

        this.relatedItemElementObserver.observe(
            this.relatedItemsContainer,
            {
                childList: true,
                subtree: true,
            }
        );
    }

    /**
     * @param {Array<MutationRecord>} mutationList
     * @param {MutationObserver} observer
     */
    onElementMutations(mutationList, observer) {
        for (const mutation of mutationList) {
            for (const addedNode of mutation.addedNodes) {
                if (
                    addedNode instanceof HTMLElement
                    && addedNode.classList.contains('inline-related')
                    && !addedNode.classList.contains('ui-sortable-placeholder')
                    && (
                        addedNode.getAttribute(
                            'data-inline-fieldset-related-item-is-initialized'
                        ) === null
                    )
                ) {
                    new ipaAdmin.InlineFieldsetRelatedItem(
                        addedNode,
                        this.relatedItemsShouldBeCollapsible,
                        true
                    );
                }
            }
        }
    }
};

})();
