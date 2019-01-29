import json
from door import http

class HttpResponse:
    def __init__(self, code, **kwargs):
        self.code = code
        self.headers = kwargs.get("headers", {})
        self.body = kwargs.get("body", None)

    def set_header(self, name, value):
        self.headers[name] = f"{value}"

    def _wsgi_start_response(self, response_starter):
        response_starter(http.STATUS_MAPPING[self.code], [(name, self.headers[name]) for name in self.headers])

class Json(HttpResponse):
    def _wsgi_reply(self, response_starter):
        body = json.dumps(self.body).encode()
        self.headers["Content-Length"] = f"{len(body)}"
        self.headers["Content-Type"] = "application/json"
        self._wsgi_start_response(response_starter)
        return [body]

class PlainText(HttpResponse):
    def _wsgi_reply(self, response_starter):
        body = self.body.encode()
        content_length = len(body)
        self.headers["Content-Length"] = f"{content_length}"
        if content_length > 0:
            self.headers["Content-Type"] = "text/plain"
        self._wsgi_start_response(response_starter)
        return [body]

class Blank(HttpResponse):
    def _wsgi_reply(self, response_starter):
        self.headers["Content-Length"] = "0"
        self._wsgi_start_response(response_starter)
        return []
