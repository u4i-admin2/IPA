(function () { 'use strict';

window.ipaAdmin.DateFieldset = class DateFieldset {
    constructor(element) {
        /** @type {HTMLFieldSetElement} */
        this.element = element;

        /** @type {HTMLInputElement} */
        this.gregorianYearInputElement;

        /** @type {HTMLInputElement} */
        this.gregorianMonthInputElement;

        /** @type {HTMLInputElement} */
        this.gregorianDayInputElement;

        /** @type {HTMLInputElement} */
        this.jalaaliYearInputElement;

        /** @type {HTMLInputElement} */
        this.jalaaliMonthInputElement;

        /** @type {HTMLInputElement} */
        this.jalaaliDayInputElement;

        const fieldNames = this.getFieldNames();

        if (fieldNames === null) {
            console.error(
                'Couldn’t initialize DateFieldset since fieldNames couldn’t be determined.',
                this.element
            );

            return;
        }

        (
            {
                'gregorianYear': this.gregorianYearInputElement,
                'gregorianMonth': this.gregorianMonthInputElement,
                'gregorianDay': this.gregorianDayInputElement,
                'jalaaliYear': this.jalaaliYearInputElement,
                'jalaaliMonth': this.jalaaliMonthInputElement,
                'jalaaliDay': this.jalaaliDayInputElement,
            } = this.getInputElements(fieldNames)
        );

        for (const gregorianInputElement of [
            this.gregorianYearInputElement,
            this.gregorianMonthInputElement,
            this.gregorianDayInputElement,
        ]) {
            gregorianInputElement.addEventListener(
                'input',
                this.onGregorianDateSelectChanged.bind(this),
                false,
            );
        }

        for (const jalaaliInputElement of [
            this.jalaaliYearInputElement,
            this.jalaaliMonthInputElement,
            this.jalaaliDayInputElement,
        ]) {
            jalaaliInputElement.addEventListener(
                'input',
                this.onJalaaliDateSelectChanged.bind(this),
                false,
            );
        }
    }

    getFieldNames() {
        const classList = this.element.classList;

        if (classList.contains('dateFieldsetReportDetention')) {
            return {
                'gregorian': {
                    'year': 'detention_year',
                    'month': 'detention_month',
                    'day': 'detention_day',
                },
                'jalaali': {
                    'year': 'detention_year_fa',
                    'month': 'detention_month_fa',
                    'day': 'detention_day_fa',
                },
            };
        }

       return null;
    }

    getInputElements(fieldNames) {
        let inputElements = {};

        for (const [
            inputElementKey,
            inputElementFieldName,
        ] of [
            [
                'gregorianYear',
                fieldNames.gregorian.year,
            ],
            [
                'gregorianMonth',
                fieldNames.gregorian.month,
            ],
            [
                'gregorianDay',
                fieldNames.gregorian.day,
            ],
            [
                'jalaaliYear',
                fieldNames.jalaali.year,
            ],
            [
                'jalaaliMonth',
                fieldNames.jalaali.month,
            ],
            [
                'jalaaliDay',
                fieldNames.jalaali.day,
            ],
        ]) {
            const inputElement = this.element.querySelector(
                `.field-box.field-${inputElementFieldName} input`
            );

            if (inputElement instanceof HTMLInputElement) {
                inputElements[inputElementKey] = inputElement;
            } else {
                throw new Error(`Couldn’t get a reference to DateFieldset <select> element: #id_${inputElementFieldName}`);
            }
        }

        return inputElements;
    }

    onGregorianDateSelectChanged(event) {
        let jalaaliDateValues;

        try {
            const gregorianDateValues = this.getDateValuesFromInputs(
                this.gregorianYearInputElement,
                this.gregorianMonthInputElement,
                this.gregorianDayInputElement,
            )

            jalaaliDateValues = (
                ipaAdmin.jalaaliJs.toJalaali.apply(null, gregorianDateValues)
            );
        } catch (error) {
            console.info('Couldn’t convert Gregorian date to Jalaali.');

            return;
        }

        this.jalaaliYearInputElement.value = jalaaliDateValues.jy;
        this.jalaaliMonthInputElement.value = jalaaliDateValues.jm;
        this.jalaaliDayInputElement.value = jalaaliDateValues.jd;
    }

    onJalaaliDateSelectChanged(event) {
        let gregorianDateValues;

        try {
            const jalaaliDateValues = this.getDateValuesFromInputs(
                this.jalaaliYearInputElement,
                this.jalaaliMonthInputElement,
                this.jalaaliDayInputElement,
            )

            gregorianDateValues = (
                ipaAdmin.jalaaliJs.toGregorian.apply(null, jalaaliDateValues)
            );
        } catch (error) {
            console.info('Couldn’t convert Jalaali date to Gregorian.');

            return;
        }

        this.gregorianYearInputElement.value = gregorianDateValues.gy;
        this.gregorianMonthInputElement.value = gregorianDateValues.gm;
        this.gregorianDayInputElement.value = gregorianDateValues.gd;
    }

    getDateValuesFromInputs(yearInput, monthInput, dayInput) {
        const yearValue = parseInt(yearInput.value);
        const monthValue = parseInt(monthInput.value);
        const dayValue = parseInt(dayInput.value);

        for (const dateSegmentValue of [
            yearValue,
            monthValue,
            dayValue,
        ]) {
            if (
                Number.isNaN(dateSegmentValue) ||
                dateSegmentValue < 1
            ) {
                throw new Error('Date was invalid — aborting conversion.');
            }
        }

        return [
            yearValue,
            monthValue,
            dayValue
        ];
    }
};

})();
