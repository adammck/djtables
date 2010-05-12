#!/usr/bin/env python
# vim: et ts=4 sw=4


from nose.tools import raises
from tables.table import Table
from tables.column import Column
from tables.row import Row


class TestTable(Table):
    name   = Column()
    weapon = Column()


def test_accepts_dicts():
    obj = {
        'name': "Leonardo",
        'weapon': "Katana"
    }

    row = Row(TestTable(), obj)
    assert row.name == obj['name']
    assert row.weapon == obj['weapon']


def test_accepts_objects():
    class MockObject(object):
        def __init__(self, name, weapon):
            self.name = name
            self.weapon = weapon

    obj = MockObject("Michelangelo", "Nunchaku")
    row = Row(TestTable(), obj)

    assert row.name == obj.name
    assert row.weapon == obj.weapon


def test_calls_callables():
    obj = {
        'name': lambda: "Donatello",
        'weapon': lambda: "Bo Staff",
    }

    row = Row(TestTable(), obj)
    assert row.name == "Donatello"
    assert row.weapon == "Bo Staff"


@raises(AttributeError)
def test_raises_on_invalid_column():
    row = Row(TestTable(), {})
    row.whatever # boom


def test_is_iterable():
    data = {
        'name': "Raphael",
        'weapon': "Sai"
    }

    row = Row(TestTable(), data)
    assert iter(row)
