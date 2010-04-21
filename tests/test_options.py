#!/usr/bin/env python
# vim: et ts=4 sw=4


from nose.tools import raises
from tables.options import Options


class TestOptions(Options):
    _defaults = {
        'letter': "A",
        'number': 999 }


def test_provides_defaults():
    o = TestOptions()
    assert o.letter == "A"
    assert o.number == 999


@raises(AttributeError)
def test_raises_on_invalid_getattr():
    TestOptions().invalid


def test_accepts_kwargs():
    o = TestOptions(letter="B")
    assert o.letter == "B"
    assert o.number == 999


def test_accepts_object():
    class Meta:
        number = 111

    o = TestOptions(Meta)
    assert o.letter == "A"
    assert o.number == 111


@raises(AttributeError)
def test_raises_on_invalid_kwargs():
    TestOptions(a=1, b=2, c=3)
