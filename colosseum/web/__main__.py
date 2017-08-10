# encoding: utf-8

import sys
import logging

from webassets.script import CommandLineEnvironment

from colosseum.web.application import application
from colosseum.web.controller import my_env


# Setup a logger
log = logging.getLogger('webassets')
log.addHandler(logging.StreamHandler())
log.setLevel(logging.DEBUG)

args = sys.argv

if __name__ == '__main__':
	if len(sys.argv) == 1:
		application.serve('wsgiref', host='0.0.0.0', port=8005)
	else:
		cmdenv = CommandLineEnvironment(my_env, log)
		if sys.argv[1] == 'build':
			cmdenv.build()
