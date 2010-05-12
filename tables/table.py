#!/usr/bin/env python
# vim: et ts=4 sw=4


from .metatable import MetaTable


class Table(object):
    __metaclass__ = MetaTable

    def __init__(self, object_list=None, request=None, page=1, **kwargs):
        self._object_list = object_list
        self._request = request

        # if a request was provided, the parameters can override default
        # settings, but not explicit keyword arguments. this is rather
        # verbose right now, but will make more sense once the params
        # are validated before being used.
        if request is not None:
            g = request.GET

            if ("sort" in g) and ("sort" not in kwargs):
                kwargs['order_by'] = g['sort']

            if ("per-page" in g) and ("per_page" not in kwargs):
                kwargs['per_page'] = int(g['per-page'])

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
    def columns(self):
        """Return the list of columns."""
        return self._meta.columns

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
