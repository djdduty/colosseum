# encoding: utf-8

import random
from bson import json_util as json

from webassets import Environment

from web.ext.acl import when

from colosseum.web.model import Account
from colosseum.web.asset import colosseum_scripts, colosseum_styles
from colosseum.ext.assets import PackageResolver


my_env = Environment(
		directory="../static/build",
		url="/static",
	)

# my_env.resolver = PackageResolver()

my_env.register('colosseum_scripts', colosseum_scripts)
my_env.register('colosseum_styles', colosseum_styles)

class AccountController(object):
	__dispatch__ = 'resource'
	
	def __init__(self, context):
		self._ctx = context
	
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


@when(when.always)
class Controller(object):
	accounts = AccountController

	def __init__(self, context):
		self._ctx = context

	def __call__(self):
		return "Hello, World!"

	def asset(self):
		return my_env['colosseum_scripts'].urls()
