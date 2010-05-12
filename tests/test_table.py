#!/usr/bin/env python
# vim: et ts=4 sw=4


from tables.table import Table
from tables.column import Column
from django.http import HttpRequest, QueryDict


DATA = [
    {'name': "Leonardo",     'weapon': "Katana"  },
    {'name': "Michelangelo", 'weapon': "Nunchaku"},
    {'name': "Donatello",    'weapon': "Bo Staff"},
    {'name': "Raphael",      'weapon': "Sai"     }]


class TestTable(Table):
    name   = Column()
    weapon = Column()


def test_kwargs_override_options():
    m = TestTable._meta.__dict__
    t1 = TestTable(per_page=1)
    t2 = TestTable(per_page=2)

    assert t1._meta.per_page == 1
    assert t2._meta.per_page == 2

    # check that the class meta hasn't been touched.
    assert TestTable._meta.__dict__ == m


def test_request_override_options():
    req = HttpRequest()
    req.GET = QueryDict(
        "sort=name&per-page=3",
        encoding="utf-8")

    t = TestTable(request=req)
    assert t._meta.order_by == "name"
    assert t._meta.per_page == 3


def test_class_exposes_columns_via_meta():
    c = TestTable._meta.columns
    assert c[0].name == "name"
    assert c[1].name == "weapon"


def test_instance_exposes_columns():
    c = TestTable().columns
    assert c[0].name == "name"
    assert c[1].name == "weapon"


def test_has_paginator():
    t = TestTable(DATA)
    p = t.paginator

    # p must quack like a django paginator, so check for some common
    # methods to ensure that it's actually a paginator returned.
    assert p.count == len(DATA)
    assert p.num_pages == 1


def test_returns_object_list():
    t = TestTable(DATA)
    d = t.object_list
    assert d == DATA


def test_returns_rows():
    class MockRow(object):
        def __init__(self, table, obj):
            self.table = table
            self.obj = obj

    t = TestTable(DATA, row_class=MockRow)

    for n in range(len(DATA)):
        assert isinstance(t.rows[n], MockRow)
        assert t.rows[n].obj == DATA[n]


def test_returns_rows_on_active_page():
    t = TestTable(DATA, per_page=2)
    assert len(t.rows) == 2


def test_spawns_cells():
    class MockCell(object):
        def __init__(self, column, row):
            self.column = column
            self.row = row

    t = TestTable(DATA, cell_class=MockCell)
    c = t.cell(111, 222)

    assert c.column == 111
    assert c.row    == 222
