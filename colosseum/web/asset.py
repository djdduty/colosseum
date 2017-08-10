# encoding: utf-8

import os

from webassets import Bundle


colosseum_scripts = Bundle(
		os.path.join(os.path.dirname(__file__), '../static/js/main.js'),
		output='app.js'
	)

colosseum_styles = Bundle(
		os.path.join(os.path.dirname(__file__), '../static/scss/application.scss'),
		filters=['scss', 'autoprefixer', 'cssmin'],
		depends=os.path.join(os.path.dirname(__file__), '../static/scss/**/*.scss'),
		output='app.css',
	)
