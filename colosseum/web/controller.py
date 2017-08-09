# encoding: utf-8

import random
from bson import json_util as json


class Controller(object):
	def __init__(self, context):
		self._ctx = context

	def __call__(self):
		return "Hello, World!"

	def mongoi(self):
		rand = random.randint(0, 100)
		self._ctx.db.test.insert_one({'test': rand})
		return json.dumps(self._ctx.db.test.find_one({'test': rand}))

	def mongor(self):
		results = [element for element in self._ctx.db.test.find()]
		return json.dumps(results)
