class HttpError(Exception):
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
    def __init__(self, allowed):
        super().__init__(405)
        self.allowed = allowed

class HttpBadRequest(HttpError):
    def __init__(self, message="bad request", reason=None):
        super().__init__(400, message=message, reason=reason)

class HttpConflict(HttpError):
    def __init__(self, message="conflict", reason=None):
        super().__init__(409, message=message, reason=reason)

class HttpUnsupportedMediaType(HttpError):
    def __init__(self, message="unsupported media type", reason=None):
        super().__init__(415, message=message, reason=reason)
