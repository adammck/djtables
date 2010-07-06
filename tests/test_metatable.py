#!/usr/bin/env python
# vim: et ts=4 sw=4


from djangotables.metatable import MetaTable


class MockOptions(object):
    def __init__(self, cls):
        if cls is not None:
            for name, value in cls.__dict__.items():
                setattr(self, name, value)


class MockColumn(object):
    def bind_to(self, *args):
        self.bound_to = args


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


class TestTableNoMeta(object):
    __metaclass__ = MetaTable
    options_class = MockOptions
    column_class  = MockColumn


def test_explicit_table_options():
    assert hasattr(TestTable, '_meta')
    assert isinstance(TestTable._meta, MockOptions)
    assert TestTable._meta.one == 1111
    assert TestTable._meta.two == 2222


def test_default_table_options():
    assert hasattr(TestTableNoMeta, '_meta')
    assert isinstance(TestTableNoMeta._meta, MockOptions)


def test_captures_column_attrs():
    assert len(TestTable._meta.columns) == 2
    assert not hasattr(TestTable, 'alpha')
    assert not hasattr(TestTable, 'beta')


def test_ignores_non_column_attrs():
    assert TestTable.gamma == False
    assert TestTable.delta == 999


def test_binds_columns_with_table_and_name():

    # extract the bindings of each column, so we can check that each
    # declared column exists _somewhere_ within, because we can't rely
    # on MockColuns coming out in the same order they went in.
    bindings = [
        getattr(c, 'bound_to')
        for c in TestTable._meta.columns]

    assert (TestTable, 'alpha') in bindings
    assert (TestTable, 'beta') in bindings
