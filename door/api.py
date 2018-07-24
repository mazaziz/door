import re
import json
from door.http import Request, Response
from door.router import Router
from door.serializers import *
from door.errors import *
import door.utils

class Api(object):
    __slots__ = ("router", "serializers")
    def __init__(self, router=None):
        self.router = router if router is not None else Router()
        self.serializers = {
            "door.errors.HttpError": ExceptionSerializer.for_http_error,
            "door.errors.HttpMethodNotAllowed": ExceptionSerializer.for_http_method_not_allowed,
            "builtins.NoneType": lambda *args: None,
            "builtins.int": BodySerializer.for_numeric,
            "builtins.float": BodySerializer.for_numeric,
            "builtins.dict": BodySerializer.to_json,
            "builtins.list": BodySerializer.to_json,
            "builtins.bytes": BodySerializer.for_bytes,
            "builtins.str": BodySerializer.for_str,
            "builtins.bool": BodySerializer.for_bool
        }

    def register_serializer(self, fqcn: str, serializer: callable):
        if not callable(serializer):
            raise Exception("serializer for {} is not callable".format(fqcn))
        self.serializers[fqcn] = serializer

    def register_route(self, route: str, handler: callable):
        self.router.register(route, handler)

    def _serialize_exception(self, e, req: Request, resp: Response):
        e_class = e.__class__
        while True:
            fqcn = "{}.{}".format(e_class.__module__, e_class.__name__)
            if fqcn in self.serializers:
                self.serializers[fqcn](e, req, resp)
                return
            if 0 != len(e_class.__bases__):
                e_class = e_class.__bases__[0]
                continue
            raise Exception("no exception handler found for {}".format(door.utils.fqcn(e)))
    
    def _handle(self, req: Request, resp: Response):
        try:
            handler = self.router.match(req)
            if handler is None:
                raise HttpNotFound(reason="RouteNotFound")
            handler(req, resp)
        except Exception as e:
            self._serialize_exception(e, req, resp)

    def __call__(self, env, start_response):
        req = Request(env)
        resp = Response()
        try:
            self._handle(req, resp)
            self.serializers[door.utils.fqcn(resp.body)](req, resp)
        except Exception as e:
            resp.code = 500
            resp.body = "{\"error\":{\"code\":500}}".encode("utf8")
            resp.headers = {}
            resp.set_header("Content-Type", "application/json")
            resp.set_header("Content-Length", len(resp.body))
            print("ERROR: unhandled exception [{}.{}]: {}".format(e.__class__.__module__, e.__class__.__name__, e))
        resp.set_header("Server", "bgws")
        resp.set_header("x-bg-request-id", req.id)
        start_response(resp.get_status(), [(name, resp.headers[name]) for name in resp.headers])
        return [] if resp.body is None else [resp.body]
