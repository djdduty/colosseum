# encoding: utf-8

import cinje

from .template import *

from colosseum.web.asset import my_env


from gigantic.parser import parse_heroes
from gigantic.dao.model import Hero

parse_heroes('colosseum/static/build/RxGame/Config/Heroes')


class Controller(object):
	def __init__(self, ctx):
		self._ctx = ctx
	
	def __call__(self):
		return render_hero_page(my_env, Hero.__dataset__)
