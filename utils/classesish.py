def gendispatch(prefix, parentlocals):
    def dispatch(n):
        s = "if n == None: r = None\n"
        for name, obj in parentlocals.items():
            if callable(obj):
                s += f"elif n == {prefix.upper()}{name.upper()}: r = {name}\n"
        exec(s, globals(), locals := {**parentlocals, 'n': n, 'r': None})
        return locals['r']
    return dispatch
