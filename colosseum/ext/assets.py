# encoding: utf-8

import os

from webassets.env import Resolver


log = __import__('logging').getLogger(__name__)

class PackageResolver(Resolver):
	def search_for_source(self, ctx, item):
		parts = item.split(':', 1)
		if len(parts) != 2:
			raise ValueError('"%s" not valid; a module path with relative file path after : is required' % item)

		package, path = parts
		m = __import__(package)

		return self.consider_single_directory(os.path.dirname(m.__file__), path)
