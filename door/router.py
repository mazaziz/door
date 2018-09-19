import re
from .handler import Handler
from .util import fqn
from .error import HttpNotFound

class Router:
    def __call__(self, req) -> (Handler, dict):
        raise Exception("{}.__call__(req) must be implemented".format(fqn(self)))

class DefaultRouter(Router):
    def __init__(self):
        self.static = {}
        self.pattern = []

    def register(self, path, handler: Handler):
        if not callable(handler):
            raise Exception("handler must be callable")
        if isinstance(path, str):
            self.static[path] = handler
        elif isinstance(path, re._pattern_type):
            self.pattern.append((path, handler))
        else:
            raise Exception("invalid route path type [{}]".format(type(path)))

    def __call__(self, req):
        try:
            return self.static[req.path], {}
        except KeyError:
            pass
        for pair in self.pattern:
            found = pair[0].search(req.path)
            if found is None:
                continue
            return pair[1], found.groupdict()
        raise HttpNotFound(reason="RouteNotFound")
