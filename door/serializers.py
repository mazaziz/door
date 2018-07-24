from door.http import Request, Response
from door.errors import *

class BodySerializer:
    @staticmethod
    def for_str(req: Request, resp: Response):
        resp.body = resp.body.encode("utf8")
        resp.set_header("Content-Type", "text/plain; charset=utf-8")
        resp.set_header("Content-Length", len(resp.body))

    @staticmethod
    def for_bool(req: Request, resp: Response):
        resp.body = ("true" if resp.body else "false").encode("ascii")
        resp.set_header("Content-Type", "text/plain")
        resp.set_header("Content-Length", len(resp.body))

    @staticmethod
    def for_numeric(req: Request, resp: Response):
        resp.body = str(resp.body).encode("ascii")
        resp.set_header("Content-Type", "text/plain")
        resp.set_header("Content-Length", len(resp.body))

    @staticmethod
    def to_json(req: Request, resp: Response):
        import json
        resp.body = json.dumps(resp.body, ensure_ascii=False, indent=2).encode("utf8")
        resp.set_header("Content-Type", "application/json")
        resp.set_header("Content-Length", len(resp.body))

    @staticmethod
    def for_bytes(req: Request, resp: Response):
        resp.set_header("Content-Length", len(resp.body))

class ExceptionSerializer:
    @staticmethod
    def for_http_error(e: HttpError, req: Request, resp: Response):
        resp.code = e.code
        error = {"code": e.code}
        if e.message is not None:
            error["message"] = e.message
        if e.reason is not None:
            error["reason"] = e.reason
        resp.body = {"error": error}

    @staticmethod
    def for_http_method_not_allowed(e: HttpMethodNotAllowed, req: Request, resp: Response):
        resp.code = 405
        resp.set_header("Allow", ", ".join(e.allowed))
        resp.body = {
            "error": {
                "code": resp.code,
                "message": "http {} is not allowed on this path".format(req.method),
                "reason": "MethodNotAllowed"
            }
        }
