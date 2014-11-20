
import struct

class Int(object):
    def __init__(self, size, value):
        self.size = size
        self.value = value

    def tohex(self):
        return "{:X}".format(self.value)

