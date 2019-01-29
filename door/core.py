
class Application:
    def __init__(self, req_builder, router):
        self.req_builder = req_builder
        self.router = router
        self.knock_hooks = []

    def run(self, ctx):
        req = self.req_builder(ctx)
        for hook in self.knock_hooks:
            resp = hook(req)
            if resp is not None:
                return resp
        handler = self.router(req)
        return handler(req)
