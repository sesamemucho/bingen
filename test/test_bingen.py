"""
Tests for `bingen` module.
"""
import pytest
from bingen import bingen
from bingen import element


class TestBingen(object):

    @classmethod
    def setup_class(cls):
        pass

    def test_something(self):
        assert element.Int(8, 3).tohex() == '3'

    @classmethod
    def teardown_class(cls):
        pass
