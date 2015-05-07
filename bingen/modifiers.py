from __future__ import print_function, absolute_import

import numbers
import struct
# from bingen import exception
from bingen import bg_exc
# import bg_exc

s2f = {1*8: 'B',
       2*8: 'H',
       4*8: 'I',
       8*8: 'Q'}

# Modifiers that are functions have no side effects or dependencies


class ModifierBase(object):
    def __init__(self):
        self._ready_to_eval = False
        self._has_been_evaluated = False
        self._value = None

    def ready_to_evaluate(self):
        return self._ready_to_evaluate


class ModifierSingleBase(ModifierBase):
    def __init__(self):
        super(ModifierSingleBase, self).__init__()
        self._ready_to_eval = True


class ModifierRangeBase(ModifierBase):
    def __init__(self, start, end):
        super(ModifierRangeBase, self).__init__()
        self._ready_to_eval = False
        self._start = start
        self._end = end


class ToBigEndian(ModifierSingleBase):
    def __init__(self):
        super(ToBigEndian, self).__init__()

    def evaluate(self, size, value):
        """Convert value to big-endian format"""

        # Must be a scalar type
        if isinstance(value, numbers.Number):
            sv = size
            if sv in s2f:
                fmt = s2f[sv]
                le_bs = struct.pack('<' + fmt, value)
                be_val = struct.unpack('>' + fmt, le_bs)[0]
                print("be_val is {:X}".format(be_val))
                return be_val
            else:
                raise bg_exc.InvalidSize(
                    "Big-endian convertion must be 1, 2, " +
                    "4, or 8 bytes long (is {})".format(
                        size))
        else:
            raise bg_exc.InvalidType("This modifier only works on numbers")
