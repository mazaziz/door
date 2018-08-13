import re
import json
from door.router import Router
from door.request import Request
from door.response import Response
import door.serializer
import door.error

class Door(object):
    __slots__ = (
        "router",
        "req_dsr",
        "resp_sr",
        "ex_sr"
    )
    def __init__(self, router, req_dsr, resp_sr, ex_sr):
        self.router = router
        self.req_dsr = req_dsr
        self.resp_sr = resp_sr
        self.ex_sr = ex_sr

    def __call__(self, env, start_response):
        req = Request(env, self.req_dsr)
        resp = Response()
        try:
            try:
                handler = self.router.match(req)
                handler(req, resp)
            except Exception as ex:
                self.ex_sr.serialize(ex, req, resp)
            self.resp_sr.serialize(req, resp)
        except Exception as ex:
            resp.code = 500
            resp.body = "{\"error\":{\"code\":500}}".encode("utf8")
            resp.headers = {}
            resp.set_header("Content-Type", "application/json")
            resp.set_header("Content-Length", len(resp.body))
            print(str(ex))
        resp.set_header("x-bg-request-id", req.id)
        start_response(resp.get_status(), [(name, resp.headers[name]) for name in resp.headers])
        return [] if resp.body is None else [resp.body]

def build() -> Door:
    return Door(
        Router(),
        None,
        door.serializer.build_response_serializer(),
        door.serializer.build_exception_serializer()
    )
