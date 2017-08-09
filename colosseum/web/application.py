# encoding: utf-8


from web.core import Application
from web.ext.db import DatabaseExtension
from web.db.mongo import MongoDBConnection

from colosseum.web.controller import Controller


application = Application(
		Controller,
		extensions=[
				DatabaseExtension(default=MongoDBConnection('mongodb://127.0.0.1/test')),
			],
	)
