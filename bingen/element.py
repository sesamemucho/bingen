
import BitVector
import itertools
import struct

class Element(object):
    _endian = 'little'

    def __init__(self):
        pass

class Int(Element):
    def __init__(self, size, value, name="", modifiers=()):
        super(Int, self).__init__()
        self._size = size
        self._value = value
        self._name = name
        # TODO: Do validation on this:
        self._modifiers = modifiers

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

    def add_all(self, items):
        # We're doing little-endian, and BitVector does big-endian
        # TODO: Keep dictionary indexed by name (if present)
        for i in itertools.chain.from_iterable((reversed(items),)):
            print("Adding:", i.tohex())
            self.add_item(i)

    def add_item(self, i):
        self.items.append(i)

    def tohex(self):
        abv = BitVector.BitVector(size=0)
        for b in self.items:
            abv += b.tobv()

        # Pad to four bits
        print("length is", abv.length())
        # The pad length should be 3, 2, 1, or 0 (not 4)
        padval = (4 - (abv.length() % 4)) & 0x3
        print("padval is", padval)
        abv.pad_from_left(padval)
        print("length is", abv.length())
        return abv.get_hex_string_from_bitvector().upper()
