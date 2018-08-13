import door.http

class Response(object):
    __slots__ = (
        "code",
        "body",
        "headers"
    )
    def __init__(self):
        self.code = 200
        self.body = None
        self.headers = {}
    
    def get_status(self) -> str:
        return door.http.STATUS_CODES[self.code]
    
    def set_header(self, name: str, value):
        self.headers[name] = str(value)

    def setnx_header(self, name: str, value):
        if name in self.headers:
            return
        self.headers[name] = str(value)        
