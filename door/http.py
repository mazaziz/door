from .util import fqn

METHODS = (
    "CONNECT",
    "DELETE",
    "GET",
    "HEAD",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT"
)

STATUS_CODES = {
    200: "200 OK",
    201: "201 Created",
    405: "405 Method Not Allowed",
    301: "301 Moved Permanently",
    400: "400 Bad Request",
    401: "401 Unauthorized",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    409: "409 Conflict",
    415: "415 Unsupported Media Type",
    429: "429 Too Many Requests",
    500: "500 Internal Server Error",
    503: "503 Service Unavailable"
}

class Request:
    def __init__(self, env: dict):
        self.env = env
        self.path = env["PATH_INFO"]
        self.method = env["REQUEST_METHOD"]

class Response:
    def __init__(self):
        self.code = 200
        self.body = None
        self.headers = {}

class RequestBuilder:
    def __call__(self, env: dict) -> Request:
        raise Exception("{}.__call__(env: dict) must be implemented".format(fqn(self)))

class ResponseBuilder:
    def __call__(self) -> Response:
        raise Exception("{}.__call__() must be implemented".format(fqn(self)))

class DefaultRequestBuilder(RequestBuilder):
    def __call__(self, env):
        return Request(env)

class DefaultResponseBuilder(ResponseBuilder):
    def __call__(self):
        return Response()
