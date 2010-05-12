#!/usr/bin/env python
# vim: et ts=4 sw=4


class Cell(object):
    def __init__(self, column, row):
        self.column = column
        self.row = row

    def __unicode__(self):
        return self.column.render(self.value)

    @property
    def value(self):
        return getattr(self.row, self.column.name)
