#!/usr/bin/env python
# vim: et ts=4 sw=4


from tables.column import Column


def test_sortable_by_order_of_creation():
    a, b, c = Column(), Column(), Column()
    assert sorted([b, a, c]) == [a, b, c]


def test_can_be_bound():
    c = Column(); c.bind_to(1, 2)
    assert c.bound_to == (1, 2)
