class HttpError(Exception):
    __slots__ = ("code", "message", "reason")
    def __init__(self, code, message=None, reason=None):
        self.code = code
        self.message = message
        self.reason = reason

class HttpNotFound(HttpError):
    def __init__(self, message="not found", reason=None):
        super().__init__(404, message=message, reason=reason)

class HttpInternalServerError(HttpError):
    def __init__(self, message="internal server error", reason=None):
        super().__init__(500, message=message, reason=reason)

class HttpMethodNotAllowed(HttpError):
    __slots__ = ("allowed")
    def __init__(self, allowed):
        super().__init__(405)
        self.allowed = allowed
