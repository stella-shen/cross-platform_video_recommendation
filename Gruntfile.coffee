module.exports = (grunt) ->
  grunt.loadNpmTasks 'grunt-contrib-less'
  grunt.loadNpmTasks 'grunt-autoprefixer'
  grunt.loadNpmTasks 'grunt-contrib-watch'
  grunt.loadNpmTasks 'grunt-contrib-copy'
  grunt.loadNpmTasks 'grunt-contrib-coffee'

  grunt.initConfig(
    path:
      src: 'BiliV/static_src'
      tgt: 'BiliV/static'
      tmp: 'tmp'
    less:
      dev:
        files: [
          expand: true
          cwd: '<%= path.src %>/less/'
          src: ['**/*.less', '!**/_*.less']
          dest: '<%= path.tmp %>/compiled_css/'
          ext: '.css'
        ]
    autoprefixer:
      dev:
        options:
          browsers: ['last 2 versions']
        files: [
          expand: true
          cwd: '<%= path.tmp %>/compiled_css/'
          src: ['**/*.css']
          dest: '<%= path.tgt %>/css/'
          ext: '.css'
        ]
    coffee:
      compile:
        files: [
          expand: true
          cwd: '<%= path.src %>/coffee/'
          src: ['**/*.coffee']
          dest: '<%= path.tgt %>/js/'
          ext: '.js'
        ]
    copy:
      vendor:
        files: [
          expand: true
          cwd: '<%= path.src %>/'
          src: ['**/*', '!coffee/**/*', '!less/**/*']
          dest: '<%= path.tgt %>/'
        ]
    watch:
      asset_css:
        files: ['<%= path.src %>/less/**/*']
        tasks: ['css']
        options : { nospawn : true }
      asset_js:
        files: ['<%= path.src %>/coffee/**/*']
        tasks: ['js']
        options : { nospawn : true }
      asset_jade:
        files: ['<%= path.src %>/**/*']
        tasks: ['copy']
        options : { nospawn : true }
  )

  grunt.registerTask 'css', [
    'less:dev'
    'autoprefixer:dev'
  ]

  grunt.registerTask 'js', [
    'coffee'
  ]

  grunt.registerTask 'dev', [
    'default'
    'watch'
  ]

  grunt.registerTask 'default', [
    'css'
    'js'
    'copy'
  ]

