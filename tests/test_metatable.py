#!/usr/bin/env python
# vim: et ts=4 sw=4


from tables.table import MetaTable
from tables.column import Column


def test_captures_column_attrs():
    class AnyColumnSubclass(Column):
        pass

    class AnyTable(object):
        __metaclass__ = MetaTable
        alpha = AnyColumnSubclass()
        beta  = Column()

    def check(name):
        assert name in AnyTable.columns.keys()
        assert not hasattr(AnyTable, name)

    check('alpha')
    check('beta')


def test_ignores_non_column_attrs():
    class AnyTable(object):
        __metaclass__ = MetaTable
        gamma = False
        delta = 999

    assert len(AnyTable.columns) == 0
    assert AnyTable.gamma == False
    assert AnyTable.delta == 999


def test_preserves_column_order():
    class AnyTable(object):
        __metaclass__ = MetaTable
        epsilon = Column()
        zeta    = Column()
        eta     = Column()

    assert AnyTable.columns.keys() == [
        'epsilon', 'zeta', 'eta']
