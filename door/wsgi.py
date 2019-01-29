import traceback
from door import core, request

class Application(core.Application):
    def __call__(self, env, start_response):
        try:
            resp = self.run(env)
            return resp._wsgi_reply(start_response)
        except:
            traceback.print_exc()
            start_response("500 Internal Server Error", [("Content-Length", "0"), ("Connection", "close")])
            return []

class Request(request.Request):
    def get_header(self, name, default=None):
        return self._env.get(f"HTTP_{name}".replace("-", "_").upper(), default)

    def _lazy_remote_addr(self):
        return self._env["REMOTE_ADDR"]

    def _lazy_query_string(self):
        return self._env["QUERY_STRING"]

    def _lazy_content_length(self):
        v = self._env.get("CONTENT_LENGTH")
        if v is not None:
            v = int(v)
        return v

class RequestBuilder:
    def __init__(self):
        self.req_class = Request

    def __call__(self, env):
        req = self.req_class()
        req.method = env["REQUEST_METHOD"]
        req.path = env["PATH_INFO"]
        req._env = env
        return req
