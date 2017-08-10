#!/usr/bin/env python
# encoding: utf-8

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

tests_require = [
		'pytest-runner',
		'coverage',
		'pytest',
		'pytest-cov',
		'pytest-spec',
		'pytest-flakes',
	]

setup(
		name = "colosseum.web",
		version = "0.0.1",

		description = "Colosseum, a web project for gigantic hero building",
		long_description = "",
		url = "https://github.com/djdduty/colosseum",
		license = "",
		keywords = [],

		packages = find_packages(exclude=['test', 'example', 'conf', 'benchmark', 'tool', 'doc']),
		include_package_data = True,
		package_data = {'': [
				'README.md',
			]},

		namespace_packages = [
				'colosseum',
			],

		setup_requires = [
				'pytest-runner',
			],

		tests_require = tests_require,

		install_requires = [
				'WebCore <3.0',
				'web.dispatch.object',
				'web.dispatch.resource',
				'marrow.mongo',
			],

		extras_require = dict(
				development = tests_require + [
						'ptpython',
						'ipython',
						'pudb',
						'backlash',
					],
			),

		zip_safe = True,

		entry_points = {
			'colosseum.web.document': [
					'Account = colosseum.web.model:Account',
				],
			}
	)
