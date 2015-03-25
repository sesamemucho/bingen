
import BitVector
import itertools
import struct

from bingen import exception

class Element(object):
    _endian = 'little'
    """Base element for Bingen-bits
    """
    def __init__(self, size, value, **kw)
        self._size = size
        self._value = value
        self._name = kw['name']
        # TODO: Do validation on this:
        self._modifiers = list()
        for m in modifiers:
            if isinstance(m, tuple) and (len(m) == 3):
                No, it can''t be that easy. A modifier needs knowledge of when it
                can be evaluated, and its dependencies. Make it an object.
                self._modifiers.append((m[0], (m[1], m[2])))
            elif callable(m):
                self._modifiers.append((m, ()))
            else:
                raise bingen.InvalidType("Unrecognized modifier \"{}\"".format(m))

class Int(Element):
    def __init__(self, size, value, name="", modifiers=()):
        super(Int, self).__init__(size, value, name=name, modifiers=modifiers)

        self.bv = BitVector.BitVector(intVal=value, size=size)

    def tohex(self):
        return "{:X}".format(self._value)

    def tobv(self):
        return self.bv

    def size(self):
        """Returns length of field in bits."""
        return self._size

class Group(Element):
    def __init__(self, *items):
        super(Group, self).__init__()
        self.items = list()
        self.add_all(items)
#TODO: Calculate length and check, maybe raise InvalidSize

    def add_all(self, items):
        # We're doing little-endian, and BitVector does big-endian
        # TODO: Keep dictionary indexed by name (if present)
        for i in itertools.chain.from_iterable((reversed(items),)):
            print("Adding:", i.tohex())
            self.add_item(i)

    def add_item(self, i):
        self.items.append(i)

    def size(self):
        s = 0
        for b in self.items:
            s += b.size()
        return s

    def tobv(self):
        abv = BitVector.BitVector(size=0)
        for b in self.items:
            abv += b.tobv()
        return abv

    def tohex(self):
        abv = self.tobv()
        # Pad to four bits
        print("length is", abv.length())
        # The pad length should be 3, 2, 1, or 0 (not 4)
        padval = (4 - (abv.length() % 4)) & 0x3
        print("padval is", padval)
        abv.pad_from_left(padval)
        print("length is", abv.length())
        return abv.get_hex_string_from_bitvector().upper()
