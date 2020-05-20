class Q(type):
    def __new__(mcs, name, bases, attrs):
        handlers = {}
        if name == "F":
            return type.__new__(mcs, name, bases, attrs)
        for action, func in attrs.items():
            if action == "handlers":
                continue
            if action.startswith("__"):
                continue
            handlers[action] = func
        attrs["handlers"] = handlers
        return type.__new__(mcs, name, bases, attrs)


class F(metaclass=Q):
    pass

class V(F):
    def fuck(self):
        return "shit"

print(V.handlers)