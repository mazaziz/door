from door.utils import random_alnum

METHODS = ("CONNECT", "DELETE", "GET", "HEAD", "OPTIONS", "PATCH", "POST", "PUT")
STATUS = {
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
    429: "429 Too Many Requests",
    500: "500 Internal Server Error",
    503: "503 Service Unavailable"
}

class Request(object):
    __slots__ = ("method", "path", "id", "named")
    def __init__(self, wsgi, id_length=16):
        self.method = wsgi["REQUEST_METHOD"]
        self.path = wsgi["PATH_INFO"]
        self.id = random_alnum(id_length)
        self.named = {}

class Response(object):
    __slots__ = ("code", "body", "headers")
    def __init__(self):
        self.code = 200
        self.body = None
        self.headers = {}
    
    def get_status(self) -> str:
        return STATUS[self.code]
    
    def set_header(self, name: str, value):
        self.headers[name] = str(value)
