#!/usr/bin/env python
# vim: et ts=4 sw=4


from fudge import Fake
from djangotables.cell import Cell


def test_gets_value_from_row():
    column = Fake().has_attr(name="alpha")
    row    = Fake().has_attr(alpha="aaa")
    cell   = Cell(column, row)

    assert cell.value == "aaa"


def test_proxies_object_from_row():
    column = Fake().has_attr()
    row    = Fake().has_attr(obj="xyz")
    cell   = Cell(column, row)

    assert cell.object == "xyz"


def test_renders_via_column():
    column = Fake().has_attr(name="beta")
    row    = Fake().has_attr(beta="bbb")
    cell   = Cell(column, row)

    (column
        .provides("render")
        .with_args(cell)
        .returns("BBB"))

    assert unicode(cell) == u"BBB"


def test_can_link():
    column = Fake().has_attr(name="gamma")
    row    = Fake().has_attr(gamma="ggg")
    cell   = Cell(column, row)

    (column
        .provides("link")
        .with_args(cell)
        .returns("GGG"))

    assert cell.link == u"GGG"
