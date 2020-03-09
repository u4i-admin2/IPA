(function () { 'use strict';

class Admin {
    constructor() {
        /** @type {HTMLBodyElement} */
        const adminBodyElement = document.body;

        // --------------------
        // --- DateFieldset ---
        // --------------------
        // Note: Only top-level dateFieldsets are initialized here.
        //
        // dateFieldsets inside inline related items are initialized in
        // InlineFieldsetRelatedItem. This is so that the DateFieldset
        // can be initialized by new InlineFieldsetRelatedItems created
        // by InlineFieldset’s MutationObserver.

        const topLevelDateFieldsetElements = (
            adminBodyElement.querySelectorAll('div:not(.inline-related) > .ipaFieldset.dateFieldset')
        );

        for (const topLevelDateFieldsetElement of topLevelDateFieldsetElements) {
            new ipaAdmin.DateFieldset(topLevelDateFieldsetElement);
        }

        // ---------------------
        // --- InlineFieldset ---
        // ---------------------
        const inlineFieldsetElements = (
            adminBodyElement.querySelectorAll('.ipaInline')
        );

        for (const inlineFieldsetElement of inlineFieldsetElements) {
            new ipaAdmin.InlineFieldset(inlineFieldsetElement);
        }

        // -----------------------------------------
        // --- django_select2 inline selects fix ---
        // -----------------------------------------
        //
        // See:
        // * https://github.com/applegrew/django-select2/issues/294
        // * https://github.com/applegrew/django-select2/issues/435

        const global$ = jQuery;
        const $ = django.jQuery;

        $(document).on(
            'formset:added',
            function (_event, row, _prefix) {
                const relatedWidgetWrappers = row.find('.related-widget-wrapper');

                for (const relatedWidgetWrapper of relatedWidgetWrappers) {
                    for (
                        const select2Container
                        of relatedWidgetWrapper.querySelectorAll('.select2-container')
                    ) {
                        select2Container.remove();
                    }

                    for (
                        const select2select
                        of relatedWidgetWrapper.querySelectorAll('select.django-select2')
                    ) {
                        global$(select2select).select2();
                    }
                }
            }
        );
    }
}

window.ipaAdmin.Admin = Admin;

})();
