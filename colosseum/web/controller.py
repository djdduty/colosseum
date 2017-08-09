# encoding: utf-8

import random
from bson import json_util as json

from colosseum.web.model import Account


class AccountController(object):
	__dispatch__ = 'resource'

	def __init__(self, context):
		self._ctx = context
		Account.bind(context.db.default)

	def post(self, *arg, **kwarg):
		user = Account(*arg, **kwarg)
		result = user.insert_one()
		assert result.acknowledged and result.inserted_id == user
		self._ctx.response.headers['content-type'] = 'application/json'
		return json.dumps(user)

	def get(self):
		result = [item for item in Account.find()]
		self._ctx.response.headers['content-type'] = 'application/json'
		return json.dumps(result)


class Controller(object):
	accounts = AccountController

	def __init__(self, context):
		self._ctx = context

	def __call__(self):
		return "Hello, World!"
