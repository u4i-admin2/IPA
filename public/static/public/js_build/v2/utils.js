(function () { 'use strict'; window.ipa = window.ipa || {};

// if (rm.consoleLevel > 2) {
    var _bind = Function.prototype.apply.bind(Function.prototype.bind);

    Object.defineProperty(Function.prototype, 'bind', {
        value: function(obj) {
            var boundFunction = _bind(this, arguments);
            boundFunction.boundObject = obj;
            return boundFunction;
        }
    });
// }

ipa.utils = {};

ipa.utils.consoleEventIndentation = 0;

ipa.utils.dispatchEvent = function (eventType, eventDetail) {
    var event = new CustomEvent(
        eventType,
        {
            detail: eventDetail || {}
        }
    );

    var prefix = '';

    for (var i = 0; i < ipa.utils.consoleEventIndentation; i++) {
        prefix += '  ';
    }

    prefix += (prefix === '' ? '━━┓ ' : '┗━┓ ');

    console.info(prefix + event.type, event.detail);

    ipa.utils.consoleEventIndentation++;

    window.dispatchEvent(event);

    ipa.utils.consoleEventIndentation--;
};

ipa.utils.addEventListener = function (eventType, callback) {
    window.addEventListener(
        eventType,
        function (event) {
            var result = callback(event);

            if (result === false) {
                return;
            }

            var callbackName = callback.name.replace('bound ', '');

            if (callbackName === '') {
                callbackName = '[anonymous function]';
            }

            var callbackBoundObjectName = '[unknown scope]';

            if (typeof callback.boundObject === 'object') {
                callbackBoundObjectName = callback.boundObject.constructor.displayName;

                if (typeof callback.boundObject.instanceDisplayName === 'string') {
                    callbackBoundObjectName += ('#' + callback.boundObject.instanceDisplayName);
                }
            }

            var prefix = '';

            for (var i = 0; i < ipa.utils.consoleEventIndentation; i++) {
                prefix += '  ';
            }

            prefix += (prefix === '' ? '─── ' : '└── ');

            console.info(prefix + callbackBoundObjectName + '.' + callbackName);
        },
        false
    );
};

})();
