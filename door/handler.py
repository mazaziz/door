from door import http, response

class RestResource:
    def __init__(self):
        self._handlers = {}
        for method in http.METHODS:
            try:
                handler =  getattr(self, f"on_{method.lower()}")
            except AttributeError:
                continue
            if not callable(handler):
                raise Exception(f"{handler} is not callable")
            self._handlers[method] = handler

    def __call__(self, req):
        try:
            handler = self._handlers[req.method]
        except KeyError:
            return response.Blank(405, headers={"Allow": ", ".join(self._handlers.keys())})
        return handler(req)
