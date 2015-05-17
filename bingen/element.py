from __future__ import absolute_import

import BitVector
import itertools
# import struct

# from bingen import exception
from bingen import bg_exc
# import bg_exc


class Element(object):
    _endian = 'little'
    _name_index = 0
    """Base element for Bingen-bits
    """
    def __init__(self, size, value, **kw):
        self._size = size
        self._value = value
        self._name = kw['name']
        # TODO: Do validation on this:
        self._modifiers = list()
        if 'modifiers' in kw:
            for m in kw['modifiers']:
                if isinstance(m, tuple) and (len(m) == 3):
                    # TODO
                    # No, it can''t be that easy. A modifier needs
                    # knowledge of when it can be evaluated, and its
                    # dependencies. Make it an object.
                    self._modifiers.append((m[0], (m[1], m[2])))
                elif callable(m):
                    self._modifiers.append((m, ()))
                else:
                    raise bg_exc.InvalidType(
                        "Unrecognized modifier \"{}\"".format(m))
        else:
            self._modifiers = ()

        if 'label' in kw:
            self._label = kw['label']
        else:
            self._label = "_Element{:04d}".format(Element._name_index)
            Element._name_index += 1


    def evaluate(self, value):
        for mods in self._modifiers:
            modifier = mods[0]()
            value = modifier.evaluate(self._size, value)

        return value


class Int(Element):
    def __init__(self, size, value, name="", **kw):
        super(Int, self).__init__(size, value, name=name, **kw)

    def tohex(self):
        return "{:X}".format(self.evaluate(self._value))

    def tobv(self):
        self.bv = BitVector.BitVector(
            intVal=self.evaluate(self._value),
            size=self._size)
        return self.bv

    def size(self):
        """Returns length of field in bits."""
        return self._size

    def label(self):
        return self._label

class Group(Element):
    _name_tmpl = 'Group{:04d}'
    _name_index = 0

    def __init__(self, *items, **kw):
        self.items = list()
        self._size = 0
        self.add_all(items)
        if 'name' in kw:
            self._name = kw['name']
        else:
            Group._name_index += 1
            self._name = Group._name_tmpl.format(Group._name_index)

            # TODO: Calculate length and check, maybe raise InvalidSize
        super(Group, self).__init__(self.size(), self.tohex(), name=self._name)

    def add_all(self, items):
        # We're doing little-endian, and BitVector does big-endian
        # TODO: Keep dictionary indexed by name (if present)
        XXX: TODO: This is a problem, because I expect the first element
        TODO: added to a group to be the, well, first element.
        for i in itertools.chain.from_iterable((reversed(items),)):
            print("Adding:", i.tohex())
            self._add_item(i)

        self._recalculate_size()

    def add_item(self, i):
        self._add_item(i)
        self._recalculate_size()

    def _add_item(self, i):
        self.items.append(i)

    def size(self):
        return self._size

    def _recalculate_size(self):
        s = 0
        for b in self.items:
            s += b.size()
        self._size = s

    def length_between(self, start, end):
        """Calculate length in bits between beginning of element that
        has label <start> and beginning of element that has label
        <end>.
        """
        len = 0
        accumulate = False
        print("start is \"{}\", end is \"{}\"".format(start, end))
        for item in self.items:
            print("Checking label {}".format(item.label()))
            if accumulate:
                if item.label() == end:
                    break
                len += item.size()
                continue

            if item.label() == start:
                accumulate = True

        return len

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
