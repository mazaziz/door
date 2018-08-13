import random
import string

def fqcn(obj):
    return "{}.{}".format(obj.__class__.__module__, obj.__class__.__name__)

def random_alnum(length: int):
    return "".join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
