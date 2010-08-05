#!/usr/bin/env python
# vim: et ts=4 sw=4


from nose.tools import raises
from djtables.options import Options


class TestOptions(Options):
    _defaults = {
        'letter': "A",
        'number': 111 }


def test_provides_defaults():
    o = TestOptions()
    assert o.letter == "A"
    assert o.number == 111


def test_accepts_kwargs():
    o = TestOptions(letter="B")
    assert o.letter == "B"
    assert o.number == 111


def test_accepts_object():
    class Meta:
        number = 333

    o = TestOptions(Meta)
    assert o.letter == "A"
    assert o.number == 333


@raises(AttributeError)
def test_raises_on_invalid_kwargs():
    TestOptions(a=1, b=2, c=3)


@raises(AttributeError)
def test_raises_on_invalid_getattr():
    TestOptions().invalid


@raises(AttributeError)
def test_raises_on_invalid_setattr():
    TestOptions().invalid = None


def test_is_forkable():
    t1 = TestOptions()
    t2 = t1.fork(letter="C")
    t3 = t1.fork(number=444)

    assert t2.letter == "C"
    assert t3.number == 444

    assert t1.letter == "A"
    assert t1.number == 111
