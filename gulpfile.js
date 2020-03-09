var gulp = require('gulp'),
    sass = require('gulp-sass'),
    concat = require('gulp-concat'),
    livereload = require('gulp-livereload'),
    jshint = require('gulp-jshint'),
    uglify = require('gulp-uglify'),
    stripDebug = require('gulp-strip-debug'),
    inject = require('gulp-inject'),
    series = require('stream-series'),
    clean = require('gulp-clean'),
    cleanCss = require('gulp-clean-css');
    Buster = require('gulp-cachebust'),
    bust = new Buster(),
    runSequence = require('run-sequence')
    fs = require('fs'),
    postCss = require('gulp-postcss'),
    postCssModules = require('postcss-modules'),
    // Via https://github.com/ben-eb/postcss-discard-duplicates/pull/44
    // GH 2019-07-22: This branch of postcss-discard-duplicates supports
    // a retainFirstOccurrence option that we need to work around
    // https://github.com/css-modules/postcss-modules/issues/32. There’s
    // almost definitely a cleaner solution with up-to-date modules, but
    // this is faster than upgrading Node and the existing build
    // dependencies.
    postCssDiscardDuplicates = require('./node_modules_custom/postcss-discard-duplicates-bsara'),
    postCssModulesValues = require('postcss-modules-values'),
    stringHash = require('string-hash'),
    path = require('path');
;

var cssModuleMappings = {};

// This is an object which defines paths for the styles and JS
var paths = {
    app: {
        cssModules: {
            files: 'css-modules/**/*.module.css',
            dest: 'public/static/public/css'
        },
        styles: {
            files: 'public/static/public/scss/*.scss',
            src: [
                'public/static/public/scss/style.scss',
                'public/static/public/scss/style_fa.scss'
            ],
            dest: 'public/static/public/css',
        },
        stylesdash: {
            files: 'ui/static/ui/scss/*.scss',
            src: ['ui/static/ui/scss/style.scss'],
            dest: 'ui/static/ui/css',
        },
        js: {
            files: [
                'public/static/public/js_build/main/**/*.js',
                'public/static/public/js_build/judges/*.js',
            ],
            dest: 'public/static/public/js'
        },
        jsV2: {
            files: [
                'public/static/public/js_build/v2/**/*.js',
            ],
            dest: 'public/static/public/js'
        },
        jsdash: {
            files: ['ui/static/ui/js_build/*.js', 'ui/static/ui/js_build/*/*.js'],
            dest: 'ui/static/ui/js'
        },
        jslib: {
            files: [
                'public/static/public/js_build/library/main/*.js',
                'public/static/public/js_build/library/extensions/*.js',
                'node_modules/stimulus/dist/stimulus.umd.js'
            ],
            dest: 'public/static/public/js'
        },
        dashboardProd: {
          src: ['ui/static/ui/**/*'],
          dest: 'ui/static/ui' }
    }
};

var cwd = process.cwd();
var isProduction = true;

gulp.task('development', function() {
    isProduction = false;

    runSequence(
        'clean-styles',
        'cleanScripts',
        'sassDash',
        'sassProduction',
        'sassProductionDash',
        'processCssModules',
        'writeCssModuleClassnameMappingsFile',
        'appJs',
        'appJsV2',
        'appJsDashboard',
        'jslibMini-dev',
        'concat-uglify-js',
        'inject-js-build',
        'inject-css'
    );
});

gulp.task('default', function() {
    console.info('Note: Please don’t commit base.html and homebase.html after running production gulp. They should never contain cache-busted CSS or JS references.')

    runSequence(
        'clean-styles',
        'sassDash',
        'sassProduction',
        'sassProductionDash',
        'processCssModules',
        'writeCssModuleClassnameMappingsFile',
        'cleanScripts',
        'appJs',
        'appJsV2',
        'appJsDashboardMini',
        'jslibMini',
        'concat-uglify-js',
        'moveDashboardProdFiles',
        'inject-js-build',
        'inject-css'
    );
});

gulp.task('dev', ['development'], function() {
    livereload.listen();
    // sass
    gulp.watch(paths.app.styles.files, ['development']);
    gulp.watch(paths.app.stylesdash.files, ['development']);
    // js
    gulp.watch(paths.app.js.files, ['development']);
    gulp.watch(paths.app.jsV2.files, ['development']);
    gulp.watch(paths.app.jsdash.files, ['development']);

    gulp.watch(
        paths.app.cssModules.files,
        function () {
            runSequence(
                'processCssModules',
                'writeCssModuleClassnameMappingsFile'
            )
        }
    );
});

gulp.task('build', ['default']);


// TASKS for PUBLIC
gulp.task('sass', function() {
    var stream = gulp.src(paths.app.styles.src)
        .pipe(sass({
            outputStyle: 'expanded',
            sourceComments: 'map',
            includePaths: [paths.app.styles.inc]
        }))
        .on('error', function(err) {
            displayError(err);
        })
        .pipe(gulp.dest(paths.app.styles.dest));
    return stream;
});

gulp.task('sassProduction', function() {
    var stream = gulp.src(paths.app.styles.src)
        .pipe(sass({
            outputStyle: 'compressed'
        }));

    if (isProduction) {
        stream = stream.pipe(bust.resources());
    }

    stream = stream
        .on('error', function(err) {
            displayError(err);
        })
        .pipe(gulp.dest(paths.app.styles.dest));

    return stream;
});

// TASKS for DASHBOARD
gulp.task('sassDash', function() {
    var stream = gulp.src(paths.app.stylesdash.src)
        .pipe(sass({
            outputStyle: 'expanded',
            sourceComments: 'map',
            includePaths: [paths.app.stylesdash.inc]
        }))
        .on('error', function(err) {
            displayError(err);
        })
        .pipe(gulp.dest(paths.app.stylesdash.dest));
    return stream;
});

gulp.task('sassProductionDash', function() {
    var stream = gulp.src(paths.app.stylesdash.src)
        .pipe(sass({
            outputStyle: 'compressed'
        }));

    if (isProduction) {
        stream = stream.pipe(bust.resources())
    }

    stream = stream
        .on('error', function(err) {
            displayError(err);
        })
        .pipe(gulp.dest(paths.app.stylesdash.dest));

    return stream;
});

gulp.task('appJsDashboard', [], function() {
    var stream = gulp.src(paths.app.jsdash.files)
        .pipe(concat('appDash.js'))
        .pipe(gulp.dest(paths.app.jsdash.dest));
    return stream;
});

gulp.task('appJsDashboardMini', function() {
    var stream = gulp.src(paths.app.jsdash.files)
        .pipe(concat('appDash.js'))
        .pipe(stripDebug())
        .pipe(uglify({ mangle: false }))
        .pipe(gulp.dest(paths.app.jsdash.dest));
    return stream;
});

gulp.task('moveDashboardProdFiles', function() {
    var stream = gulp.src(paths.app.dashboardProd.src)
      .pipe(gulp.dest(paths.app.dashboardProd.dest));
    return stream;
});


gulp.task('appJs', [], function() {
    var stream = gulp.src(paths.app.js.files);

    if (isProduction) {
        stream = stream
            .pipe(concat('app.min.js'))
            .pipe(stripDebug())
            .pipe(uglify({ mangle: false }));
    } else {
        stream = stream
            .pipe(jshint())
            .pipe(jshint.reporter('default'))
            .pipe(concat('app.js'));
    }

    stream = stream.pipe(gulp.dest(paths.app.js.dest));

    return stream;
});

gulp.task('appJsV2', [], function() {
    var stream = gulp.src(paths.app.jsV2.files);

    if (isProduction) {
        stream = stream
            .pipe(concat('appV2.js'))
            .pipe(stripDebug());
    } else {
        stream = stream
            .pipe(jshint())
            .pipe(jshint.reporter('default'))
            .pipe(concat('appV2.js'));
    }

    stream = stream.pipe(gulp.dest(paths.app.jsV2.dest));

    return stream;
});

gulp.task('jslib', [], function() {
    var stream = gulp.src(paths.app.jslib.files)
        .pipe(concat('lib.js'))
        .pipe(gulp.dest(paths.app.jslib.dest));
    return stream;
});

gulp.task('jslibMini-dev', function() {
    var stream = gulp.src(paths.app.jslib.files)
        .pipe(concat('lib.min.js'))
        .pipe(gulp.dest(paths.app.jslib.dest));
    return stream;
});

gulp.task('jslibMini', function() {
    var stream = gulp.src(paths.app.jslib.files)
        .pipe(concat('lib.min.js'))
        .pipe(uglify({ mangle: false }))
        .pipe(gulp.dest(paths.app.jslib.dest));
    return stream;
});

gulp.task('concat-uglify-js', function() {
    var srcFiles = [
        paths.app.js.dest + '/lib.*.js',
        paths.app.js.dest + '/app*.js'
    ];

    var stream = gulp.src(srcFiles)
        .pipe(concat('united.min.js'));

    if (isProduction) {
        stream = stream
            .pipe(stripDebug())
            .pipe(bust.resources());
    }

    stream = stream.pipe(gulp.dest(paths.app.jslib.dest));

    return stream;
});

gulp.task('inject-js-build', function() {
    var buildStream = gulp.src([paths.app.js.dest + '/united.*.js'], { read: false });
    var stream = gulp.src(['public/templates/base.html', 'public/templates/homebase.html'])
        .pipe(inject(
            series(buildStream),
            {
                ignorePath: '/public',
                transform: djangoStaticJsReferenceInjectTransform,
            }
        ))
        .pipe(gulp.dest('public/templates/'));
    return stream;
});

gulp.task('clean-styles', function() {
    var stream = gulp.src(paths.app.styles.dest, { read: false })
        .pipe(clean());

    return stream;
});

gulp.task('inject-css', function() {
    return gulp.src(['public/templates/base.html', 'public/templates/homebase.html'])
        .pipe(inject(
            gulp.src(
                paths.app.styles.dest + (isProduction ? '/style.*.css' : '/style.css'),
                {
                    read: false
                }
            ),
            {
                starttag: '<!--inject:ltr:css-->',
                ignorePath: '/public',
                transform: djangoStaticCssReferenceInjectTransform,
            }
        ))
        .pipe(inject(
            gulp.src(
                paths.app.styles.dest + (isProduction ? '/style_fa.*.css' : '/style_fa.css'),
                {
                    read: false
                }
            ),
            {
                starttag: '<!--inject:rtl:css-->',
                ignorePath: '/public',
                transform: djangoStaticCssReferenceInjectTransform,
            }
        ))
        .pipe(inject(
            gulp.src(
                paths.app.styles.dest + (isProduction ? '/modules.*.css' : '/modules.css'),
                {
                    read: false
                }
            ),
            {
                starttag: '<!--inject:modules:css-->',
                ignorePath: '/public',
                transform: djangoStaticCssReferenceInjectTransform,
            }
        ))
        .pipe(gulp.dest('public/templates/'));
});

// Clean functions
gulp.task('cleanScripts', function() {
    var stream = gulp.src('public/static/public/js/*.js', { read: false })
        .pipe(clean());
    return stream;
});

gulp.task(
    'processCssModules',
    function () {
        var stream = gulp
            .src(paths.app.cssModules.files)
            .pipe(
                postCss([
                    postCssModules({
                        generateScopedName: function(name, filename, css) {
                            var moduleName = path.basename(
                                filename,
                                '.module.css'
                            );

                            var cssContentHash = stringHash(css).toString(36).substr(0, 5);

                            return moduleName + '_' + name + '_' + cssContentHash;
                        },
                        getJSON: function (cssFileName, json) {
                            var moduleName = path.basename(
                                cssFileName,
                                '.module.css'
                            );

                            // Defined at top of file; used by
                            // writeCssModuleClassnameMappingsFile task
                            cssModuleMappings[moduleName] = json;
                        },
                    }),
                    postCssModulesValues(),
                ])
            )
            .pipe(
                concat('modules.css')
            )
            .pipe(
                postCss([
                  postCssDiscardDuplicates({
                    retainFirstOccurrence: true
                  })
                ])
            );

        if (isProduction) {
            stream = stream
            .pipe(
                cleanCss()
            )
            .pipe(
                bust.resources()
            );
        }

        stream = stream.pipe(
            gulp.dest(paths.app.cssModules.dest)
        );

        return stream;
    }
);

gulp.task(
    'writeCssModuleClassnameMappingsFile',
    function (done) {
        var staticDirectoryPath = `${__dirname}/static`;

        if (!fs.existsSync(staticDirectoryPath)) {
            fs.mkdirSync(staticDirectoryPath);
        }

        fs.writeFileSync(
            `${staticDirectoryPath}/css-module-classname-mappings.json`,
            JSON.stringify(cssModuleMappings)
        );

        done();
    }
);

function djangoStaticCssReferenceInjectTransform(filepath, file, i, length) {
    return (
        '<link rel="stylesheet" href="'
        + "{% static '"
        + filepath.replace('/static/', '')
        + "' %}"
        + '">'
    );
}

function djangoStaticJsReferenceInjectTransform(filepath, file, i, length) {
    return (
        '<script src="'
        + "{% static '"
        + filepath.replace('/static/', '')
        + "' %}"
        + '"></script>'
    );
}

// CRAP ////////////////////////////////////////////////////////////////////////
var displayError = function(error) {
    var errorString = '[' + error.plugin + ']'
    errorString += ' ' + error.message.replace("\n", '')
    if (error.fileName)
        errorString += ' in ' + error.fileName
    if (error.lineNumber)
        errorString += ' on line ' + error.lineNumber
    console.error(errorString);
}
