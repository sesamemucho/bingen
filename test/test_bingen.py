"""
Tests for `bingen` module.
"""
import pytest
from bingen import bingen
from bingen import element
from bingen import modifiers
from bingen import bg_exc
import BitVector

class TestBingenBasic(object):

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
        # Not a present requirement
        # with pytest.raises(exception.InvalidSize):
        g1 = element.Group(a)

        assert g1.tohex() == '1CD'
        assert g1.size() == 9

    def test_create_group_with_2(self):
        a = element.Int(9, 0x1CD)
        b = element.Int(7, 0x5A)
        g1 = element.Group(a,b)

        assert g1.tohex() == 'B5CD'
        assert g1.size() == 16

    def test_create_group_with_2_groups(self):
        a = element.Int(9, 0x1CD)
        b = element.Int(6, 0x3A)
        g1 = element.Group(a,b)
        g2 = element.Group(a,b)

        g3 = element.Group(g1, g2)

        assert g3.tohex() == '3AE6F5CD'
        assert g3.size() == 30

    def test_create_group_with_2_groups_and_1_element(self):
        a = element.Int(9, 0x1CD)
        b = element.Int(6, 0x3A)
        g1 = element.Group(a,b)
        g2 = element.Group(a,b)
        c = element.Int(4, 0xA)

        g3 = element.Group(g1, g2, c)

        assert g3.tohex() == '2BAE6F5CD'
        assert g3.size() == 34

    @classmethod
    def teardown_class(cls):
        pass

class TestBingenWithModifiers(object):

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def test_create_element_bigendian(self):
        a = element.Int(16, 0xABCD, modifiers=(modifiers.ToBigEndian,))

        assert a.tohex() == 'CDAB'
        assert a.size() == 16

