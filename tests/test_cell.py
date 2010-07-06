#!/usr/bin/env python
# vim: et ts=4 sw=4


from fudge import Fake
from djangotables.cell import Cell


def test_gets_value_from_row():
    column = Fake().has_attr(name="alpha")
    row    = Fake().has_attr(alpha="aaa")
    cell   = Cell(column, row)

    assert cell.value == "aaa"


def test_renders_via_column():
    column = Fake().has_attr(name="beta")
    row    = Fake().has_attr(beta="bbb")
    cell   = Cell(column, row)

    (column
        .provides("render")
        .with_args("bbb")
        .returns("BBB"))

    assert unicode(cell) == u"BBB"
