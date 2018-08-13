import door.util

class Request(object):
    __slots__ = (
        "_env",
        "_deserializer",
        "method",
        "path",
        "id",
        "named",
        "content_type",
        "content_length",
        "body"
    )
    def __init__(self, env: dict, deserializer=None, id_length=16):
        self._env = env
        self._deserializer = deserializer
        self.method = self._env["REQUEST_METHOD"]
        self.path = self._env["PATH_INFO"]
        self.content_type = self._env.get("CONTENT_TYPE", None)
        self.content_length = int(self._env.get("CONTENT_LENGTH", 0))
        self.id = door.util.random_alnum(id_length)
        self.named = {}
        self.body = None
        print("")
        for k in self._env:
            if isinstance(self._env[k], str):
                print("{}={}".format(k, self._env[k]))
            else:
                print("{}={}".format(k, type(self._env[k])))
    
    def deserialize(self):
        self.body = self._deserializer.deserialize(self)
