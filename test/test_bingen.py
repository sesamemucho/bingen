"""
Tests for `bingen` module.
"""
import pytest
from bingen import bingen
from bingen import element
import BitVector

class TestBingen(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        assert element.Int(8, 3).tohex() == '3'

    def test_BitVector(self):
        assert element.Int(8, 3).tobv() == BitVector.BitVector(intVal=3, size=8)

    def test_bv2(self):
        assert element.Int(16, 0xABCD).tobv().get_hex_string_from_bitvector().upper() == "ABCD"

    def test_bv3(self):
        a = element.Int(9, 0x1CD)
        b = element.Int(7, 0x55)

        c = b.tobv() + a.tobv()
        assert c.get_hex_string_from_bitvector().upper() == "ABCD"

    def test_create_group(self):
        a = element.Int(9, 0x1CD)
        g1 = element.Group(a)

        assert g1.tohex() == '1CD'

    def test_create_group_with_2(self):
        a = element.Int(9, 0x1CD)
        b = element.Int(7, 0x5A)
        g1 = element.Group(a,b)

        assert g1.tohex() == 'B5CD'

    @classmethod
    def teardown_class(cls):
        pass
