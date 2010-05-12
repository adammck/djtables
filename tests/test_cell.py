#!/usr/bin/env python
# vim: et ts=4 sw=4


from tables.cell import Cell


class MockColumn:
    name = "a"

    def render(self, x):
        return x.upper()


class MockRow:
    a = "alpha"
    b = "beta"


def test_gets_value_from_row():
    c = Cell(MockColumn(), MockRow())
    assert c.value == "alpha"


def test_renders_via_column():
    c = Cell(MockColumn(), MockRow())
    assert unicode(c) == "ALPHA"
