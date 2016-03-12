module.exports = function(grunt) {
	require('load-grunt-tasks')(grunt);

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		watch: {
			src: {
				files: ['src/', 'node_modules/bootstrap-sass'],
				tasks: ['dev'],
			}
		},
		sass: {
			options: {
				sourceMap: true,
				includePaths: ['node_modules/bootstrap-sass/assets/stylesheets/']
			},
			dist: {
				files: {
					'app/static/css/main.css': 'src/scss/main.scss'
				}
			}
		}
	})

	grunt.registerTask('default', ['dev', 'watch'])
	grunt.registerTask('dev', ['sass'])
}
