#!/usr/bin/env python
# vim: et ts=4 sw=4


class Column(object):
    creation_counter = 0

    def __init__(self):

        # like django fields, keep track of the order which columns are
        # created, so they can be sorted later. (unfortunately, python
        # attrs are passed to __new__ as an unsorted dict, so we must
        # keep track of this manually to avoid random column order.)
        self.creation_counter = Column.creation_counter
        Column.creation_counter += 1

        self.bound_to = None

    def __lt__(self, other):
        """Allow columns to be sorted by order of creation."""
        return self.creation_counter < other.creation_counter

    def bind_to(self, table, name):
        if self.bound_to is not None:
            raise TypeError(
                "Column is already bound to '%s' as '%s'" %\
                    self.bound_to)

        self.bound_to = (table, name)

    @property
    def is_bound(self):
        return (self.bound_to is not None)
