# encoding: utf-8

import cinje

from .template import *


from gigantic.parser import parse_heroes, parse_translations
from gigantic.dao.hero import Hero
from gigantic.dao.translation import HeroTranslation

parse_heroes('colosseum/static/build/RxGame/Config/Heroes')
parse_translations('colosseum/static/build/RxGame/Localization')


class Controller(object):
	def __init__(self, ctx):
		self._ctx = ctx
	
	def __call__(self):
		return render_hero_page(Hero.__dataset__, HeroTranslation.__dataset__)
