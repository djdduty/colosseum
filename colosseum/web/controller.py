# encoding: utf-8

import os
from bson import json_util as json
import cinje
import requests

from webob.exc import HTTPNotFound

from web.ext.acl import when
from web.app.static import static

from colosseum.web.model import Account
from colosseum.web.asset import colosseum_scripts, colosseum_styles, my_env
from colosseum.web.template import render_index

from colosseum.player.controller import Controller as PlayerController

from colosseum.hero.controller import Controller as HeroController


log = __import__('logging').getLogger(__name__)


static_path=os.path.normpath(os.path.join(os.path.dirname(__file__), "../static/build"))


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
	player = PlayerController
	hero = HeroController
	
	def __init__(self, context):
		self._ctx = context
	
	def __call__(self):
		return render_index(my_env)
	
	def asset(self):
		return "<script src='"+my_env['colosseum_scripts'].urls()[0]+"'></script><link rel='stylesheet' type='text/css' href='"+my_env['colosseum_styles'].urls()[0]+"'></link>"
	
	#def player(self, player_name=None, **kw):
	#	if player_name is None:
	#		try:
	#			player_name = kw.pop('name')
	#		except:
	#			return render_player_page(my_env, None, None)
	#	
	#	payload = {'usernames[]': player_name.lower()}
	#	log.debug("Fetching motiga profile", extra=dict(params=payload))
	#	r = requests.get('https://stats.gogigantic.com/en/gigantic-careers/usersdata/', params=payload)
	#	log.debug("Fetched motiga profile", extra=dict(url=r.url))
	#	if self._ctx.request.is_xhr:
	#		self._ctx.response.headers['content-type'] = r.headers['content-type']
	#		return r.text
	#	
	#	data = r.json()
	#	name = 'result'
	#	try:
	#		while name == 'result':
	#			name, profile = data['data'].popitem()
	#	except:
	#		profile = None
	#		name = 'Player Not Found'
	#	
	#	return render_player_page(my_env, name, profile)
