# encoding: utf-8

from marrow.package.host import PluginManager


class ColosseumExtension(object):
	needs={'mongodb'}
	
	def __init__(self):
		pass
	
	def start(self, context):
		types = PluginManager('colosseum.web.document')
		
		for Doc in types:
			if not Doc.__collection__ or not hasattr(Doc, 'bind'): continue
	
		Doc.bind(context.db.default)
