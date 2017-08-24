# encoding: utf-8

import cinje

from webob.exc import HTTPNotFound

from web.ext.acl import when

from colosseum.account.controller import Controller as AccountController
from colosseum.player.controller import Controller as PlayerController
from colosseum.hero.controller import Controller as HeroController

from .template.dashboard import render_dashboard


log = __import__('logging').getLogger(__name__)


@when(when.always)
class API(object):
	accounts = AccountController
	player = PlayerController
	hero = HeroController

	def __init__(self, context):
		self._ctx = context

	def __call__(self):
		return render_dashboard()
