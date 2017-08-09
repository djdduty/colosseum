# encoding: utf-8

from colosseum.web.application import application

if __name__ == '__main__':
	application.serve('wsgiref', host='0.0.0.0', port=8005)
