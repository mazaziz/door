def fqn(v) -> str:
    try:
        return "{}.{}".format(v.__module__, v.__name__)
    except AttributeError:
        return "{}.{}".format(v.__class__.__module__, v.__class__.__name__)
