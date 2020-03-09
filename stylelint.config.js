module.exports = {
    "extends": [
        "stylelint-config-standard",
        "stylelint-config-css-modules",
    ],
    "ignoreFiles": [
        "public/static/public/scss/**/*",
        "public/static/public/js_build/**/*"
    ],
    "rules": {
        "at-rule-empty-line-before": null,
        "comment-empty-line-before": null,
        "comment-whitespace-inside": null,
        "declaration-empty-line-before": null,
        "indentation": 4,
        "length-zero-no-unit": null,
        "no-descending-specificity": null,
        "rule-empty-line-before": null,
        "selector-list-comma-newline-after": null,
        "shorthand-property-no-redundant-values": null,
        "selector-pseudo-element-colon-notation": null,
    }
};
