"""
This is for function-classes.
They are declared like this:
    def MyFClass(arg1, arg2):
        ...define procedures...
        return gendispatch(locals())

Note that these should NOT have any extraneous local variables;
all top-level local variables should be functions meant to be called.
"""

def gendispatch(parentlocals):
    """
    Generate the dispatch function.
    This is for use in a class-function (something inspired by chapter 2 of SICP)
    Given a bunch of procedure-name-constants in uppercase (globally of course)
      and a bunch of corresponding subprocedures (locally in parent)
    generate the dispatch() routine which is to be returned.
    Note: This should be used like so:
        return gendispatch("<prefix>", locals())

    The parent function's locals have to be passed because of technical constraints.

    Due to how inheritance is implemented, you must not name a local (procedure or not)
    "_exposed".

    See example.py for more details.
    """
    def dispatch(n):
        s = "if n == '_exposed': r = parentlocals\n"  # return the parent locals
                                                      # (a.k.a. procedures and other junk)
        for name, obj in parentlocals.items():
            if callable(obj) and name[0] != '_' :  # it's a non-'private' function
                s += f"elif n.upper() == '{name.upper()}': r = {name}\n"  # add it to the
                                                                          # if-else case tree

        exec(s, globals(), slocals := {
            **parentlocals, 'n': n, 'r': None, "parentlocals": parentlocals
        })
        return slocals['r']  # that's the result

    return dispatch


def fcmerge(base, extend):
    """
    Merges two function-classes.
    Overlapping definitions will favour base2.
    Beware the order of arguments though; it's base1, then base2. Overlapping
    definitions from base2 will be in the base1's place. Use kwargs to be sure.

    "base" should be the base fc /called with initial args/.
    "extend" should be the extending fc /uncalled/.

    Again, see example.py for more details.
    """

    exec(
        f"""
def r({', '
       .join(
           map(
               lambda c: c + "=" + (
                   f'{{**base("_exposed"), **extend(base)("_exposed")}}["{c}"]'
               ),
               {**base("_exposed"), **extend(base)("_exposed")}.keys()
           )
       )
}):
 return gendispatch(locals())
        """,
        globals(),
        slocals := {**locals(), "r": None}  # not sure if this is needed, but...
    )

    return slocals["r"](**base("_exposed"), **extend(base)("_exposed"))
