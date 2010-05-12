#!/usr/bin/env python
# vim: et ts=4 sw=4


class Row(object):
    def __init__(self, table, obj):
        self.table = table
        self.obj = obj

    def __getattr__(self, name):
        if hasattr(self.obj, name):
            value = getattr(self.obj, name)

        elif name in self.obj:
            value = self.obj[name]

        else:
            raise AttributeError(name)

        return callable(value) and value() or value

    def __iter__(self):
        for column in self.table._meta.columns:
            yield self.table.cell(column, self)
