#!/usr/bin/env python
# vim: et ts=4 sw=4


from tables.table import MetaTable
from tables.column import Column


# unlike the real Options, this mock will accept ANY names
class MockOptions(object):
    def __init__(self, options):
        if options is not None:
            for name, value in options.__dict__.items():
                setattr(self, name, value)


def test_adds_table_options():
    class TableNoMeta(object):
        __metaclass__ = MetaTable
        options_class = MockOptions

    assert hasattr(TableNoMeta, '_meta')
    assert isinstance(TableNoMeta._meta, MockOptions)

    class TableWithMeta(object):
        __metaclass__ = MetaTable
        options_class = MockOptions

        class Meta:
            one = 1
            two = 2

    assert TableWithMeta._meta.one == 1
    assert TableWithMeta._meta.two == 2


def test_captures_column_attrs():
    class AnyColumnSubclass(Column):
        pass

    class AnyTable(object):
        __metaclass__ = MetaTable
        options_class = MockOptions
        alpha = AnyColumnSubclass()
        beta  = Column()

    def check(name):
        assert name in AnyTable._meta.columns.keys()
        assert not hasattr(AnyTable, name)

    check('alpha')
    check('beta')


def test_ignores_non_column_attrs():
    class AnyTable(object):
        __metaclass__ = MetaTable
        options_class = MockOptions
        gamma = False
        delta = 999

    assert len(AnyTable._meta.columns) == 0
    assert AnyTable.gamma == False
    assert AnyTable.delta == 999
