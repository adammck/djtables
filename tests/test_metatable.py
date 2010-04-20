#!/usr/bin/env python
# vim: et ts=4 sw=4


from tables.table import MetaTable


class MockOptions(object):
    def __init__(self, cls):
        if cls is not None:
            for name, value in cls.__dict__.items():
                setattr(self, name, value)


class MockColumn(object):
    pass


class TestTable(object):
    __metaclass__ = MetaTable
    options_class = MockOptions
    column_class  = MockColumn

    alpha = MockColumn()
    beta  = MockColumn()
    gamma = False
    delta = 999

    class Meta:
        one = 1111
        two = 2222


def test_adds_table_options():
    assert hasattr(TestTable, '_meta')
    assert isinstance(TestTable._meta, MockOptions)
    assert TestTable._meta.one == 1111
    assert TestTable._meta.two == 2222


def test_captures_column_attrs():
    assert 'alpha' in TestTable._meta.columns.keys()
    assert 'beta'  in TestTable._meta.columns.keys()
    assert not hasattr(TestTable, 'alpha')
    assert not hasattr(TestTable, 'beta')


def test_ignores_non_column_attrs():
    assert 'gamma' not in TestTable._meta.columns.keys()
    assert 'delta' not in TestTable._meta.columns.keys()
    assert TestTable.gamma == False
    assert TestTable.delta == 999
