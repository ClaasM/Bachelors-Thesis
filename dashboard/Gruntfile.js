'use strict';

module.exports = function (grunt) {

  // Load grunt tasks automatically, when needed TODO why
  require('jit-grunt')(grunt, {
    useminPrepare: 'grunt-usemin',
    ngtemplates: 'grunt-angular-templates',
    cdnify: 'grunt-google-cdn',
    buildcontrol: 'grunt-build-control',
    shell: 'grunt-shell'
  });

  // Time how long tasks take. Can help when optimizing build times
  require('time-grunt')(grunt);

  // Define the configuration for all the tasks
  grunt.initConfig({

    // Configure which site to open when the "open" task is run
    open: {
      server: {
        url: 'http://localhost:5000'
      }
    },

    // Configure which files to watch and which tasks to run when they change
    watch: {
      //When javascript changes, inject it into
      injectJS: {
        files: [
          'client/**/*.js',
          '!client/bower_components/**',
          '!client/index.js'
        ],
        tasks: ['injector:scripts']
      },
      injectSass: {
        files: ['client/**/*.{scss,sass}', '!client/bower_components/**'],
        tasks: ['injector:sass']
      },
      sass: {
        files: ['client/**/*.{scss,sass}', '!client/bower_components/**'],
        tasks: ['sass', 'postcss']
      },
      gruntfile: {
        files: ['Gruntfile.js']
      },
      livereload: {
        files: [
          '{.tmp,dist}/**/*.{js,css,html}',
          'client/**/*.{png,jpg,jpeg,gif,webp,svg}',
          '!client/bower_components/**'
        ],
        options: {
          livereload: true
        }
      },
      flask: {
        files: ['server/**/*.py'],
        tasks: ['flask', 'wait'],
        options: {
          livereload: true,
          spawn: false //Without this option specified flask won't be reloaded
        }
      },
      bower: {
        files: ['bower.json'],
        tasks: ['wiredep']
      }
    },

    // Empties folders to start fresh
    clean: {
      dist: {
        files: [{
          dot: true,
          src: [
            '.tmp',
            'dist/!(.git*|.openshift|Procfile)**'
          ]
        }]
      },
      server: '.tmp'
    },

    // Add vendor prefixed styles. Postcss can do much more though
    postcss: {
      options: {
        map: true,
        processors: [
          require('autoprefixer')({browsers: ['last 2 version']})
        ]
      },
      dist: {
        files: [{
          expand: true,
          cwd: '.tmp/',
          src: '{,*/}*.css',
          dest: '.tmp/'
        }]
      }
    },

    // Automatically inject Bower components into the app
    wiredep: {
      options: {
        exclude: [
          //TODO why are these excluded?
          /bootstrap.js/,
          '/json3/',
          '/es5-shim/',
          /font-awesome\.css/,
          /bootstrap\.css/,
          /bootstrap-sass-official/,
          /bootstrap-social\.css/
        ]
      },
      client: {
        src: 'client/index.html',
        ignorePath: 'client/',
      }
    },

    // Renames files for browser caching purposes
    filerev: {
      dist: {
        src: [
          'dist/client/!(bower_components){,*/}*.{js,css,png,jpg,jpeg,gif,webp,svg}' //TODO No idea if this works
        ]
      }
    },

    // Reads HTML for usemin blocks to enable smart builds that automatically
    // concat, minify and revision files. Creates configurations in memory so
    // additional tasks can operate on them
    useminPrepare: {
      html: ['client/index.html'],
      options: {
        dest: 'dist/client'
      }
    },

    // Performs rewrites based on rev and the useminPrepare configuration
    usemin: {
      html: ['dist/client/{,!(bower_components)/**/}*.html'],
      css: ['dist/client/!(bower_components){,*/}*.css'],
      js: ['dist/client/!(bower_components){,*/}*.js'],
      options: {
        assetsDirs: [
          'dist/client'
        ],
        // This is so we update image references in our ng-templates
        patterns: {
          js: [
            [/(assets\/images\/.*?\.(?:gif|jpeg|jpg|png|webp|svg))/gm, 'Update the JS to reference our revved images']
          ]
        }
      }
    },

    // The following *-min tasks produce minified files in the dist folder
    imagemin: {
      dist: {
        files: [{
          expand: true,
          cwd: 'client/',
          src: '{,*/}*.{png,jpg,jpeg,gif,svg}',
          dest: 'dist/client/'
        }]
      }
    },

    // Allow the use of non-minsafe AngularJS files. Automatically makes it
    // minsafe compatible so Uglify does not destroy the ng references
    ngAnnotate: {
      dist: {
        files: [{
          expand: true,
          cwd: '.tmp/concat',
          src: '**/*.js',
          dest: '.tmp/concat'
        }]
      }
    },

    // Package all the html partials into a single javascript payload
    ngtemplates: {
      options: {
        // This should be the name of your apps angular module
        module: 'Dashboard',
        htmlmin: {
          collapseBooleanAttributes: true,
          collapseWhitespace: true,
          removeAttributeQuotes: true,
          removeEmptyAttributes: true,
          removeRedundantAttributes: true,
          removeScriptTypeAttributes: true,
          removeStyleLinkTypeAttributes: true
        },
        usemin: 'index.js'
      },
      main: {
        cwd: 'dist',
        src: ['client/**/*.html', '!client/bower_components/**'],
        dest: '.tmp/templates.js'
      },
      tmp: {
        cwd: '.tmp',
        src: ['client/**/*.html', '!client/bower_components/**'],
        dest: '.tmp/tmp-templates.js'
      }
    },

    // Replace Google CDN references
    cdnify: {
      dist: {
        html: ['dist/client/*.html']
      }
    },

    // Copies remaining files to places other tasks can use
    copy: {
      dist: {
        files: [{
          expand: true,
          dot: true,
          cwd: 'dist',
          dest: 'dist/client',
          src: [
            '*.{ico,png,txt}',
            '.htaccess',
            'bower_components/**/*',
            'assets/images/{,*/}*.{webp}',
            'assets/fonts/**/*',
            'index.html'
          ]
        }, {
          expand: true,
          cwd: '.tmp/images',
          dest: 'dist/client/assets/images',
          src: ['generated/*']
        }, {
          expand: true,
          dest: 'dist',
          src: [
            'server/**/*'
          ]
        }]
      },
      styles: {
        expand: true,
        cwd: 'dist',
        dest: '.tmp/',
        src: ['client/**/*.css', '!client/bower_components/**']
      }
    },

    buildcontrol: {
      options: {
        dir: 'dist',
        commit: true,
        push: true,
        connectCommits: false,
        message: 'Built %sourceName% from commit %sourceCommit% on branch %sourceBranch%'
      },
      //TODO this should be able to automatically push to aws or something
    },

    // Compiles Sass to CSS
    sass: {
      server: {
        options: {
          compass: false
        },
        files: {
          '.tmp/client/index.css': 'client/index.scss'
        }
      }
    },

    injector: {
      options: {},
      // Inject application script files into index.html (doesn't include bower)
      scripts: {
        options: {
          transform: function (filePath) {
            filePath = filePath.replace('/client/', '');
            filePath = filePath.replace('/.tmp/', '');
            return '<script src="' + filePath + '"></script>';
          },
          sort: function (a, b) {
            var module = /\.module\.js$/;
            var aMod = module.test(a);
            var bMod = module.test(b);
            // inject *.module.js first
            return (aMod === bMod) ? 0 : (aMod ? -1 : 1);
          },
          starttag: '<!-- injector:js -->',
          endtag: '<!-- endinjector -->'
        },
        files: {
          'client/index.html': [
            [
              'client/**/*.js',
              '!client/bower_components/**',
              '!client/index.js'
            ]
          ]
        }
      },

      // Inject component scss into index.scss
      sass: {
        options: {
          transform: function (filePath) {
            // index.scss is already located in /client
            return '@import \'' + filePath.replace('/client/', '') + '\';';
          },
          starttag: '// injector',
          endtag: '// endinjector'
        },
        files: {
          'client/index.scss': [
            'client/**/*.{scss,sass}',
            '!client/index.{scss,sass}',
            '!client/bower_components/**',
          ]
        }
      },

      // Inject component css into index.html
      css: {
        options: {
          transform: function (filePath) {
            filePath = filePath.replace('/client/', '');
            filePath = filePath.replace('/.tmp/', '');
            return '<link rel="stylesheet" href="' + filePath + '">';
          },
          starttag: '<!-- injector:css -->',
          endtag: '<!-- endinjector -->'
        },
        files: {
          'client/index.html': [
            'client/**/*.css',
            '!client/bower_components/**',
          ]
        }
      }
    },

    shell: {
      python: {
        options: {
          stdout: true
        },
        command: [
          //'~/.virtualenvs/thesis/bin/activate',
          'python run.py',
        ].join(' && ')
      }
    }
  });

  // Used for delaying livereload until after server has restarted
  grunt.registerTask('wait', function () {
    grunt.log.ok('Waiting for server reload...');

    var done = this.async();

    setTimeout(function () {
      grunt.log.writeln('Done waiting!');
      done();
    }, 1500);
  });

  grunt.registerTask('serve', function () {
    grunt.task.run([
      'clean:server',
      'injector:sass',
      'sass',
      'injector',
      'wiredep:client',
      'postcss',
      'shell:python',
      'wait',
      'open',
      'watch'
    ]);
  });

  grunt.registerTask('build', [
    'clean:dist',
    'sass',
    'imagemin',
    'injector',
    'wiredep:client',
    'useminPrepare',
    'postcss',
    'ngtemplates',
    'concat',
    'ngAnnotate',
    'copy:dist',
    'cdnify',
    'cssmin',
    'uglify',
    'filerev',
    'usemin'
  ]);
};
