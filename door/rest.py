from door.request import Request
from door.response import Response
import door.http
import door.error

class RestHandler(object):
    __slots__ = ("handlers")
    def __init__(self):
        self.handlers = {}
        for method in door.http.METHODS:
            attr = "on_{}".format(method.lower())
            try:
                handler = getattr(self, attr)
                if callable(handler):
                    self.handlers[method] = handler
                else:
                    raise Exception("{} is not callable".format(attr))
            except AttributeError:
                continue

    def __call__(self, req: Request, resp: Response):
        try:
            handler = self.handlers[req.method]
        except KeyError:
            raise door.error.HttpMethodNotAllowed(self.handlers.keys())
        handler(req, resp)
