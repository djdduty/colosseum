# encoding: utf-8

import os
import cinje

from web.app.static import static

from colosseum.static.asset import my_env

from .template.application import render_application
from .api import API


log = __import__('logging').getLogger(__name__)

static_path=os.path.normpath(os.path.join(os.path.dirname(__file__), "../static/build"))


class SPADispatcher():
	"""
	A WebCore2 dispatcher which routes all non xhr, text/html requests to an SPA controller, and all other requests
	to an API root controller.
	"""
	def __call__(self, context, obj, path):
		if context.request.is_xhr or 'Authentication' in context.request.headers or 'text/html' not in context.request.accept:
			yield None, obj.api, False
		else:
			yield None, obj.spa, False


class SPA(object):
	__dispatch__ = 'object'
	public = static(static_path)
	
	def __init__(self, ctx):
		self._ctx = ctx
	
	def __call__(self, *args, **kw):
		request = self._ctx.request.copy()
		request.headers['X-Requested-With'] = 'XMLHttpRequest'
		response = request.get_response(self._ctx.app)
		
		log.debug("Got sub-response: ", extra=dict(status=response.status))
		if response.status_code != 200:
			self._ctx.response.status = response.status_code
			self._ctx.response.headers = response.headers
			return response.body
		
		return render_application(my_env, response.body.decode('utf-8'))
	
	def health(self, *arg, **kwarg):
		return "Healthy"


class Controller():
	__dispatch__ = SPADispatcher()

	api = API
	spa = SPA
