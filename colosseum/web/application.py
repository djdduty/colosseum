# encoding: utf-8

from web.core.application import Application

from web.db.mongo import MongoDBConnection
from web.session.mongo import MongoSession

from web.ext.db import DatabaseExtension
from web.ext.acl import ACLExtension, when
from web.ext.session import SessionExtension
from web.ext.annotation import AnnotationExtension
from web.ext.serialize import SerializationExtension

if __debug__:
	from web.ext.debug import DebugExtension
	from web.ext.analytics import AnalyticsExtension

from .controller import Controller
from colosseum.ext import ColosseumExtension


db_uri = 'mongodb://127.0.0.1/test'

debug_extensions = [AnalyticsExtension(), DebugExtension()] if __debug__ else []


application = Application(
		Controller,
		extensions=[
				ACLExtension(default=when.never),
				AnnotationExtension(),
				ColosseumExtension(),
				DatabaseExtension(default=MongoDBConnection(db_uri)),
				SessionExtension(default=MongoSession()),
				SerializationExtension(),
 			] + debug_extensions,
		logging={
				'version': 1,
				'handlers': {
						'db': {
								'class': 'marrow.mongo.util.logger.MongoHandler',
								'uri': db_uri,
								'collection': 'logs',
								'level': 'DEBUG' if __debug__ else 'INFO',
							},
						'console': {
								'class': 'logging.StreamHandler',
								'formatter': 'json',
								'level': 'DEBUG' if __debug__ else 'INFO',
								'stream': 'ext://sys.stdout',
							},
					},
				'loggers': {
						'colosseum': {
								'level': 'DEBUG' if __debug__ else 'INFO',
								'handlers': ['console', 'db'],
								'propagate': False,
							},
						'web': {
								'level': 'INFO' if __debug__ else 'WARN',
								'handlers': ['console', 'db'],
								'propagate': False,
							},
					},
				'root': {
						'level': 'DEBUG' if __debug__ else 'WARN',
						'handlers': ['console', 'db'],
					},
				'formatters': {
						'json': {'()': 'marrow.mongo.util.logger.JSONFormatter'},
						'mongo': {'()': 'marrow.mongo.util.logger.MongoFormatter'},
					},
			}
	)
