import re
from urllib.parse import parse_qs
from door import response

class Request:
    def __getattr__(self, name):
        try:
            return self.__dict__[name]
        except:
            loader = f"_lazy_{name}"
            if loader not in self.__dir__():
                raise AttributeError(f"unknown attribute: {name}")
            self.__dict__[name] = getattr(self, loader)()
            return self.__dict__[name]

    def _lazy_user_agent(self):
        return self.get_header("User-Agent")

    def _lazy_host(self):
        return self.get_header("Host")

    def _lazy_query_params(self):
        if 0 == len(self.query_string):
            return {}
        params = parse_qs(self.query_string, keep_blank_values=True, strict_parsing=True)
        for key in params:
            if 1 == len(params[key]):
                params[key] = params[key][0]
        return params

def default_not_found_handler(req):
    return response.Blank(404)

class Router:
    def __init__(self, not_found_handler=default_not_found_handler):
        self.static = {}
        self.pattern = []
        self.not_found_handler = not_found_handler

    def register(self, path, handler):
        if not callable(handler):
            raise Exception("handler must be callable")
        if isinstance(path, str):
            self.static[path] = handler
        elif isinstance(path, re._pattern_type):
            self.pattern.append((path, handler))
        else:
            raise Exception(f"invalid route path type [{type(path)}]")

    def __call__(self, req):
        try:
            return self.static[req.path]
        except KeyError:
            pass
        for pair in self.pattern:
            found = pair[0].search(req.path)
            if found is None:
                continue
            req.pvars = found.groupdict()
            return pair[1]
        return self.not_found_handler
