module.exports = function(grunt) {
	require('load-grunt-tasks')(grunt);

	grunt.initConfig({
		pkg: grunt.file.readJSON('package.json'),
		watch: {
			src: {
				files: ['src/**/*', 'node_modules/bootstrap-sass'],
				tasks: ['dev'],
			}
		},
		sass: {
			options: {
				includePaths: ['node_modules/bootstrap-sass/assets/stylesheets/', 'src/scss/']
			},
			dist: {
				files: {
					'app/static/css/main.css': 'src/scss/main.scss'
				}
			}
		},
		postcss: {
    		options: {
    			map: true,
	    		processors: [
	        		require("pixrem")(), // add fallbacks for rem units
	        		require("autoprefixer")({browsers: "last 2 versions"}), // add vendor prefixes
	        		require("cssnano")() // minify the result
	      		]
    		},
    		dist: {
		    	src: "app/static/css/*.css"
		    }
    	}
	})

	grunt.registerTask('default', ['dev', 'watch'])
	grunt.registerTask('dev', ['sass', 'postcss'])
}
