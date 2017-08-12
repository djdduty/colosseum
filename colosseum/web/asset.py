# encoding: utf-8

import os

import pkg_resources

from webassets import Bundle
from webassets.filter import get_filter, register_filter

from colosseum.ext.assets import Rollup, PackageResolver

from webassets import Environment


register_filter(Rollup)
es2015 = get_filter('babel', presets='es2015')


colosseum_scripts = Bundle(
		'colosseum.static:js/main.js',
		filters=('rollup',es2015,),
		depends='colosseum.static:js/**/*.js',
		output='app.%(version)s.js'
	)


colosseum_styles = Bundle(
		'colosseum.static:scss/application.scss',
		filters=['scss', 'cssmin'],
		depends='colosseum.static:scss/**/*.scss',
		output='app.%(version)s.css',
	)


static_path=os.path.normpath(os.path.join(os.path.dirname(__file__), "../static/build"))
my_env = Environment(
 		directory=static_path,
		url="/public",
		manifest="json:manifest.json",
		auto_build=__debug__,
	)

my_env.resolver = PackageResolver()

my_env.register('colosseum_scripts', colosseum_scripts)
my_env.register('colosseum_styles', colosseum_styles)
