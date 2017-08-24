# encoding: utf-8

import os

import pkg_resources

from webassets import Bundle
from webassets.env import Resolver
from webassets.filter import get_filter, register_filter, ExternalTool, option

from webassets import Environment


log = __import__('logging').getLogger(__name__)

class PackageResolver(Resolver):
	def search_for_source(self, ctx, item):
		pkg, _, fname = item.partition(':') # Get the module name, and the resource relative path
		fpath = pkg_resources.resource_filename(pkg, fname) # Find the resource abs path
		return fpath # self.consider_single_directory(fpath, fname) # HINT HINT


class Rollup(ExternalTool):
	"""Use Rollup to bundle assets.

	Requires the Rollup executable to be available externally. You can
	install it using `Node Package Manager <http://npmjs.org/>`_::
	
		$ npm install -g rollup
	
	Supported configuration options:
	ROLLUP_BIN
		The path to the Rollup binary. If not set, assumes ``rollup``
		is in the system path.
	ROLLUP_EXTRA_ARGS
		A list of any additional command-line arguments.
	"""
	
	name = 'rollup'
	max_debug_level = None
	options = {
			'binary': 'ROLLUP_BIN',
			'extra_args': option('ROLLUP_EXTRA_ARGS', type=list)
		}
	
	def input(self, infile, outfile, **kwargs):
		args = [self.binary or 'rollup']
		
		if self.extra_args:
			args.extend(self.extra_args)
		
		args.append(kwargs['source_path'])
		
		self.subprocess(args, outfile, infile)


register_filter(Rollup)
es2015 = get_filter('babel', presets='es2015')


colosseum_scripts = Bundle(
		'colosseum.web:js/main.js',
		filters=('rollup',es2015,),
		depends='colosseum:**/*.js',
		output='app.%(version)s.js'
	)


colosseum_styles = Bundle(
		'colosseum.web:scss/application.scss',
		filters=['scss', 'cssmin'],
		depends='colosseum:**/*.scss',
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
