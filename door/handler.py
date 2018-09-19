from .http import METHODS, Request, Response
from .util import fqn
from .error import HttpMethodNotAllowed

class Handler:
    def __call__(self, req, resp, *args):
        raise Exception("{}.__call__(req, resp, *args) must be implemented".format(fqn(self)))

class RestResouce(Handler):
    def __init__(self):
        self._handlers = {}
        for http_method in METHODS:
            try:
                handler =  getattr(self, "on_{}".format(http_method.lower()))
            except AttributeError:
                continue
            if not callable(handler):
                raise Exception("{} is not callable".format(handler))
            self._handlers[http_method] = handler

    def __call__(self, req: Request, resp: Response, *args):
        try:
            handler = self._handlers[req.method]
        except KeyError:
            raise HttpMethodNotAllowed(self._handlers.keys())
        handler(req, resp, *args)
