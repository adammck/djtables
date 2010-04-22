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


class Table(object):
    __metaclass__ = MetaTable

    def __init__(self, object_list=None, request=None, page=1, **kwargs):
        self._object_list = object_list
        self._request = request

        self._paginator = None
        self.page = page

        if len(kwargs):
            self._meta = self._meta.fork(
                **kwargs)

    @property
    def object_list(self):
        """Return the full object_list."""
        return self._object_list

    @property
    def paginator(self):
        if self._paginator is None:
            self._paginator = self._meta.paginator_class(
                self._object_list, self._meta.per_page)

        return self._paginator

    @property
    def rows(self):
        """Return the list of object on the active page."""

        return map(
            lambda o: self._meta.row_class(self, o),
            self.paginator.page(self.page).object_list
        )

    def cell(self, column, row):
        return self._meta.cell_class(
            column, row)
