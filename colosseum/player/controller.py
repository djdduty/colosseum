# encoding: utf-8

import json
import requests

from webob.exc import HTTPNotFound

from colosseum.web.template import render_player_page
from colosseum.web.asset import my_env


log = __import__('logging').getLogger(__name__)


motiga_player = "https://stats.gogigantic.com/en/gigantic-careers/usersdata/" # usernames[]=
motiga_search = "https://stats.gogigantic.com/en/gigantic-careers/playersearch/" # username=search page_num=0 page_size=25 platform=arc

def motiga_fetch(url, **kwargs):
		log.debug("Fetching motiga data", extra=dict(url=url, params=kwargs))
		r = requests.get(url, params=kwargs)
		if r.status_code != 200:
			raise ValueError()
		
		data = r.json()
		if 'data' not in data:
			raise ValueError()

		if __debug__:
			log.debug("Fetched motiga data", extra=dict(data=data))
		return data.pop('data')


class PlayerResource(object):
	__dispatch__ = 'resource'

	def __init__(self, context, collection, resource):
		self._ctx = context
		
		self._result = resource.pop('result')
		self._name, self._data = resource.popitem()

	def get(self, *arg, **kwarg):
		return render_player_page(my_env, self._name, self._data)


class Controller(object):
	__dispatch__ = 'resource'
	__resource__ = PlayerResource
	
	def __init__(self, context):
		self._ctx = context
	
	def __getitem__(self, index):
		try:
			name = str(index)
		except ValueError:
			raise KeyError("Could not parse index")

		profile = motiga_fetch(motiga_player, **{'usernames[]': name})
		return profile
	
	def get(self, *arg, **kwarg):
		search = ''
		try:
			search = kwarg.pop('search')
		except:
			pass

		self._ctx.response.headers['content-type'] = 'application/json'
		return motiga_fetch(motiga_search, username=search, page_num=0, page_size=25, platform='arc')
