#!/usr/bin/env python
# vim: et ts=4 sw=4


from .metatable import MetaTable
from .urls import extract


class Table(object):
    __metaclass__ = MetaTable

    def __init__(self, object_list=None, request=None, **kwargs):
        self._object_list = object_list
        self._request = request
        self._paginator = None

        if request is not None:
            kwargs = dict(
                extract(request.GET),
                **kwargs)

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
    def columns(self):
        """Return the list of columns."""
        return self._meta.columns

    @property
    def rows(self):
        """Return the list of object on the active page."""

        return map(
            lambda o: self._meta.row_class(self, o),
            self.paginator.page(self._meta.page).object_list
        )

    def cell(self, column, row):
        return self._meta.cell_class(
            column, row)
