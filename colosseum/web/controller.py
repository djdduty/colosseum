# encoding: utf-8


class Controller(object):
	def __init__(self, context):
		self._ctx = context

	def __call__(self):
		return "Hello, World!"
