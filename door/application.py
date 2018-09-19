import traceback
import logging
from .http import RequestBuilder, ResponseBuilder, DefaultRequestBuilder, DefaultResponseBuilder, STATUS_CODES
from .router import Router, DefaultRouter

class WsgiApplication:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.request_builder: RequestBuilder = None
        self.response_builder: ResponseBuilder = None
        self.router: Router = None
        self.hooks = {
            "on_req": [],
            "on_match": [],
            "on_resp": []
        }

    def register_request_builder(self, v):
        if not callable(v):
            raise Exception("request builder must be callable")
        self.request_builder = v

    def register_response_builder(self, v):
        if not callable(v):
            raise Exception("response builder must be callable")
        self.response_builder = v

    def register_router(self, v: Router):
        if not callable(v):
            raise Exception("router must be callable")
        self.router = v

    def register_middleware(self, m):
        try:
            self.hooks["on_req"].append(getattr(m, "on_req"))
        except AttributeError:
            pass
        try:
            self.hooks["on_match"].append(getattr(m, "on_match"))
        except AttributeError:
            pass
        try:
            self.hooks["on_resp"].insert(0, getattr(m, "on_resp"))
        except AttributeError:
            pass

    def __call__(self, env, start_response):
        ex = None
        handler = None
        try:
            req = self.request_builder(env)
            resp = self.response_builder()
            for on_req in self.hooks["on_req"]:
                on_req(req, resp)
            handler, pathvars = self.router(req)
            for on_match in self.hooks["on_match"]:
                on_match(req, resp, handler, pathvars)
            handler(req, resp, *pathvars.values())
        except Exception as e:
            resp.code = 500
            resp.body = None
            resp.headers = {}
            ex = e
        try:
            for on_resp in self.hooks["on_resp"]:
                on_resp(req, resp, handler, ex)
        except Exception as ex:
            resp.code = 500
            resp.body = None
            resp.headers = {}
            traceback.print_exc()
        start_response(STATUS_CODES[resp.code], [(name, resp.headers[name]) for name in resp.headers])
        return [] if resp.body is None else [resp.body]

def build(router=None, request_builder=None, response_builder=None, middleware=None) -> WsgiApplication:
    app = WsgiApplication()
    app.register_router(DefaultRouter() if router is None else router)
    app.register_request_builder(DefaultRequestBuilder() if request_builder is None else request_builder)
    app.register_response_builder(DefaultResponseBuilder() if response_builder is None else response_builder)
    if middleware is not None:
        for mw in middleware:
            app.register_middleware(mw)
    return app
