#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.template.loader import render_to_string
from .metatable import MetaTable
from .urls import extract, build


class Table(object):
    __metaclass__ = MetaTable

    def __init__(self, object_list=None, request=None, **kwargs):
        self._object_list = object_list
        self._request = request
        self._paginator = None

        if request is not None:
            prefix = kwargs.get('prefix', "")
            kwargs = dict(extract(request.GET, prefix), **kwargs)

        if len(kwargs):
            self._meta = self._meta.fork(
                **kwargs )

    def get_url(self, **kwargs):
        """
        Return an url, relative to the request associated with this
        table. Any keywords arguments provided added to the query
        string, replacing existing values.
        """

        return build(
            self._request.path,
            self._request.GET,
            self._meta.prefix,
            **kwargs )

    @property
    def object_list(self):
        """
        Return this table's object_list, transformed (sorted, reversed,
        filtered, etc) according to its meta options.
        """

        ol = self._object_list

        if self._meta.order_by and hasattr(ol, "order_by"):
            ol = ol.order_by(self._meta.order_by)

        return ol

    def as_html(self): # pragma: no cover
        """
        Return this table as HTML, ready to be inserted into a template.
        To customize the output, set the ``template`` meta option to a
        new template, and use the table_tags to build your own template.
        See README for examples.
        """

        return render_to_string(
            self._meta.template,
            { "table": self } )

    @property
    def paginator(self):
        if self._paginator is None:
            self._paginator = self._meta.paginator_class(
                self.object_list, self._meta.per_page )

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
            self.paginator.page(self._meta.page).object_list )

    def cell(self, column, row):
        return self._meta.cell_class(
            column, row )
