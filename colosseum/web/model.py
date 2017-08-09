# encoding: utf-8

from marrow.mongo import Index
from marrow.mongo.field import Array, Number, ObjectId, String
from marrow.mongo.trait import Queryable

log = __import__('logging').getLogger(__name__)


class Account(Queryable):
	__collection__ = 'test'

	username = String(required=True)
	name = String()
	locale = String(default='en-CA-u-tz-cator-cu-CAD', assign=True)
	age = Number()

	tag = Array(String(), assign=True)

	_username = Index('username', unique=True)
