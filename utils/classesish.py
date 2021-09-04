def gendispatch(prefix, parentlocals):
    """
    Generate the dispatch function.
    This is for use in a class-function (something inspired by chapter 2 of SICP)
    Given a bunch of procedure-name-constants in uppercase (globally of course)
      and a bunch of corresponding subprocedures (locally in parent)
    generate the dispatch() routine which is to be returned.
    Note: This should be used like so:
        gendispatch("<prefix>", locals())
    locals have to be passed because of technical constraints
    """
    def dispatch(n):
        s = "if n == None: r = None\n"
        for name, obj in parentlocals.items():
            if callable(obj):  # if it's a function
                s += f"elif n == {prefix.upper()}{name.upper()}: r = {name}\n"  # add it to the if-else case tree

        exec(s, globals(), locals := {**parentlocals, 'n': n, 'r': None})  # run the if-else case tree
        return locals['r']  # that's the result

    return dispatch
