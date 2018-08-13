import re
from door.request import Request
from door.error import HttpNotFound

class Router(object):
    __slots__ = (
        "static",
        "pattern"
    )
    def __init__(self):
        self.static = {}
        self.pattern = []
    
    def register(self, route, handler):
        if not callable(handler):
            raise Exception("handler must be callable")
        if isinstance(route, str):
            self.static[route] = handler
        elif isinstance(route, re._pattern_type):
            self.pattern.append((route, handler))
        else:
            raise Exception("invalid route type [{}]".format(type(route)))
    
    def match(self, req: Request) -> callable:
        try:
            return self.static[req.path]
        except KeyError:
            pass
        for pair in self.pattern:
            found = pair[0].search(req.path)
            if found is None:
                continue
            req.named = found.groupdict()
            return pair[1]
        raise HttpNotFound(reason="RouteNotFound")
