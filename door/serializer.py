from door.request import Request
from door.response import Response
from door.error import *
import door.util

def serialize_resp_builtins_str(req: Request, resp: Response):
    resp.body = resp.body.encode("utf8")
    resp.set_header("Content-Type", "text/plain; charset=utf-8")
    resp.set_header("Content-Length", len(resp.body))

def serialize_resp_builtins_bytes(req: Request, resp: Response):
    resp.set_header("Content-Length", len(resp.body))

def serialize_resp_builtins_bool(req: Request, resp: Response):
    resp.body = ("true" if resp.body else "false").encode("ascii")
    resp.set_header("Content-Type", "text/plain")
    resp.set_header("Content-Length", len(resp.body))

def serialize_resp_builtins_none_type(req: Request, resp: Response):
    resp.set_header("Content-Length", 0)

def serialize_resp_any_numeric(req: Request, resp: Response):
    resp.body = str(resp.body).encode("ascii")
    resp.set_header("Content-Type", "text/plain")
    resp.set_header("Content-Length", len(resp.body))

def serialize_resp_to_json(req: Request, resp: Response):
    import json
    resp.body = json.dumps(resp.body, ensure_ascii=False, indent=2).encode("utf8")
    resp.set_header("Content-Type", "application/json")
    resp.set_header("Content-Length", len(resp.body))

class ResponseBodySerializer(object):
    __slots__ = ("registry")
    def __init__(self):
        self.registry = {}
    
    def serialize(self, req: Request, resp: Response):
        body_fqcn = door.util.fqcn(resp.body)
        if body_fqcn not in self.registry:
            raise Exception("no serializer configured for the response body of type [{}]".format(body_fqcn))
        self.registry[body_fqcn](req, resp)
    
    def register(self, body_fqcn: str, serializer: callable):
        if not callable(serializer):
            raise Exception("serializer for {} is not callable".format(body_fqcn))
        self.registry[body_fqcn] = serializer

def build_response_serializer() -> ResponseBodySerializer:
    rs = ResponseBodySerializer()
    rs.register("builtins.str", serialize_resp_builtins_str)
    rs.register("builtins.bool", serialize_resp_builtins_bool)
    rs.register("builtins.bytes", serialize_resp_builtins_bytes)
    rs.register("builtins.NoneType", serialize_resp_builtins_none_type)
    rs.register("builtins.int", serialize_resp_any_numeric)
    rs.register("builtins.float", serialize_resp_any_numeric)
    rs.register("builtins.dict", serialize_resp_to_json)
    rs.register("builtins.list", serialize_resp_to_json)
    return rs

def serialize_ex_http_error(e: HttpError, req: Request, resp: Response):
    resp.code = e.code
    error = {
        "code": e.code
    }
    if e.message is not None:
        error["message"] = e.message
    if e.reason is not None:
        error["reason"] = e.reason
    resp.body = {"error": error}

def serialize_ex_http_method_not_allowed(e: HttpMethodNotAllowed, req: Request, resp: Response):
    resp.code = 405
    resp.set_header("Allow", ", ".join(e.allowed))
    resp.body = {
        "error": {
            "code": resp.code,
            "message": "http {} is not allowed on this path".format(req.method),
            "reason": "MethodNotAllowed"
        }
    }

class ExceptionSerializer(object):
    __slots__ = ("registry")
    def __init__(self):
        self.registry = {}
    
    def register(self, ex_fqcn: str, serializer: callable):
        if not callable(serializer):
            raise Exception("serializer for the exception [{}] is not callable".format(ex_fqcn))
        self.registry[ex_fqcn] = serializer

    def serialize(self, ex: Exception, req: Request, resp: Response):
        ex_class = ex.__class__
        while True:
            fqcn = "{}.{}".format(ex_class.__module__, ex_class.__name__)
            if fqcn in self.registry:
                self.registry[fqcn](ex, req, resp)
                return
            if 0 != len(ex_class.__bases__):
                ex_class = ex_class.__bases__[0]
                continue
            raise Exception("unhandled exception [{}]: {}".format(door.util.fqcn(ex), ex))

def build_exception_serializer() -> ExceptionSerializer:
    es = ExceptionSerializer()
    es.register("door.error.HttpError", serialize_ex_http_error)
    es.register("door.error.HttpMethodNotAllowed", serialize_ex_http_method_not_allowed)
    return es
