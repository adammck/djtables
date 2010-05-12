#!/usr/bin/env python
# vim: et ts=4 sw=4


from .options import TableOptions
from .column import Column


class MetaTable(type):
    def __new__(cls, name, bases, attrs):
        options_class = attrs.pop('options_class', TableOptions)
        column_class = attrs.pop('column_class', Column)

        # grab all of the instances of column_class from attrs, since
        # we're storing them separately (in _meta), we don't want them
        # in the actual table class.
        columns = dict([
            (attname, attrs.pop(attname))
            for attname, value in attrs.items()
            if isinstance(value, column_class)
        ])

        # create the class as usual (but sans attrs).
        attrs['_meta'] = options_class(attrs.pop('Meta', None))
        obj = super(MetaTable, cls).__new__(cls, name, bases, attrs)

        # bind each column, to make it aware of its own name. this
        # avoids having to include the name in the Column constructor.
        for name, column in columns.items():
            column.bind_to(obj, name)

        # store the columns (just the objects; they are already bound to
        # their names) in the order which they were created.
        obj._meta.columns = sorted(columns.values())

        return obj
