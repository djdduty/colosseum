#!/usr/bin/env python
# encoding: utf-8

import os

from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))


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

		tests_require = [
				'pytest-runner',
				'coverage',
				'pytest',
				'pytest-cov',
				'pytest-spec',
				'pytest-flakes',
			],

		install_requires = [
				'WebCore',
				'web.dispatch.object',
				'web.dispatch.resource',
			],

		extras_require = dict(
				development = [
						'pytest-runner',
						'coverage',
						'pytest',
						'pytest-cov',
						'pytest-spec',
						'pytest-flakes',
					],
			),

		zip_safe = True,

		entry_points = {
				}
	)
