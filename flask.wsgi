import sys

#Append path
sys.path.insert(0, '/srv/vhosts/technocake.xyz/bgj/ggj-cards')
from webinterface import app as application


import pprint, traceback

class LoggingMiddleware:

    def __init__(self, application):
        self.__application = application

    def __call__(self, environ, start_response):
        errors = environ['wsgi.errors']
        pprint.pprint(('REQUEST', environ), stream=errors)

        def _start_response(status, headers, *args):
            try:
                pprint.pprint(('RESPONSE', status, headers), stream=errors)
                return start_response(status, headers, *args)
            except:
                traceback.print_exc()
        return self.__application(environ, _start_response)

application = LoggingMiddleware(application)
