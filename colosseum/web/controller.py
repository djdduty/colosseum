# encoding: utf-8

import random, os
from bson import json_util as json

from webassets import Environment

from web.ext.acl import when
from web.app.static import static

from colosseum.web.model import Account
from colosseum.web.asset import colosseum_scripts, colosseum_styles
from colosseum.ext.assets import PackageResolver


static_path=os.path.normpath(os.path.join(os.path.dirname(__file__), "../static/build"))
my_env = Environment(
		directory=static_path,
		url="/public",
	)

my_env.resolver = PackageResolver()

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
	public = static(static_path)

	def __init__(self, context):
		self._ctx = context

	def __call__(self):
		return "Hello, World!"

	def asset(self):
		return "<script src='"+my_env['colosseum_scripts'].urls()[0]+"'></script><link rel='stylesheet' type='text/css' href='"+my_env['colosseum_styles'].urls()[0]+"'></link>"
