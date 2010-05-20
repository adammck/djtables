#!/usr/bin/env python
# vim: et ts=4 sw=4


from fudge import Fake
from nose.tools import assert_raises
from tables.column import Column


def test_sortable_by_order_of_creation():
    a, b, c = Column(), Column(), Column()
    assert sorted([b, a, c]) == [a, b, c]


def test_can_be_bound():
    table  = Fake()
    column = Column()

    column.bind_to(table, "alpha")

    assert column.is_bound == True
    assert column.bound_to == (table, "alpha")


def test_raises_if_rebound():
    table_a = Fake()
    table_b = Fake()
    column = Column()

    column.bind_to(table_a, "beta")

    assert_raises(AttributeError,
        column.bind_to, table_b, "gamma")


def test_can_be_explicitly_named():
    column = Column(name="delta")
    assert column.name == "delta"


def test_can_be_named_by_binding():
    table  = Fake()
    column = Column()

    column.bind_to(table, "epsilon")

    assert column.name == "epsilon"


def test_renders_values_to_unicode():
    assert Column().render(True) == u"True"
    assert Column().render(123) == u"123"


def test_renders_name_to_unicode():
    assert unicode(Column('zeta')) == u"zeta"
