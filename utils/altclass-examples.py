from altclass import *
def Pair(a, b):
    # Getters and setters will be generated locally
    return gendispatch(Pair, locals())  # MUST be present for /all/ function-classes

def Coord_ext(_base, c):  # return the actual extender
    def gen_unique_id():
        return 2**_base("_a")() * 3**_base("_b")() * 5**c  # ;)

    return gendispatch(Coord_ext, locals())  # must still be present, even for
                                             # classes meant to extend others

print(Pair(1, 2)("_a")())  # call the getter for a
print(Pair(1, 2)("_b")())

Coord = lambda a, b, c: fcmerge(Coord, Pair(a, b), Coord_ext, (c,))  # extend
print(Coord(1, 2, 3)("_a")())  # call the getter for a
print(Coord(1, 2, 3)("_b")())
print(Coord(1, 2, 3)("_c")())
print(Coord(1, 2, 3)("gen_unique_id")())
