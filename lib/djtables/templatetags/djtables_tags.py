#!/usr/bin/env python
# vim: et ts=4 sw=4


from django import template
register = template.Library()

from ..column import WrappedColumn


@register.inclusion_tag("djtables/cols.html")
def table_cols(table):
    return {
        "columns": [
            WrappedColumn(table, column)
            for column in table.columns ] }


@register.inclusion_tag("djtables/head.html")
def table_head(table):
    return {
        "columns": [
            WrappedColumn(table, column)
            for column in table.columns ] }


@register.inclusion_tag("djtables/body.html")
def table_body(table):
    return {
        "rows": table.rows,
        "num_columns": len(table.columns) }


@register.inclusion_tag("djtables/foot.html")
def table_foot(table):
    paginator = Paginator(table)

    return {
        "num_columns": len(table.columns),
        "page": paginator.current(),
        "paginator": paginator,
    }


class Paginator(object):
    def __init__(self, table):
        self.table = table

    def current(self):
        return Page(self, self.table._meta.page)

    @property
    def num_pages(self):
        return self.table.paginator.num_pages

    def first(self):
        return Page(self, 1)

    def last(self):
        return Page(self, self.num_pages)


class Page(object):
    def __init__(self, paginator, number):
        self.paginator = paginator
        self.number = number

    @property
    def is_first(self):
        return self.number == 1

    @property
    def is_last(self):
        return self.number == self.paginator.num_pages

    def previous(self):
        if not self.is_first:
            return Page(
                self.paginator,
                self.number-1)

    def next(self):
        if not self.is_last:
            return Page(
                self.paginator,
                self.number+1)

    def url(self):
        return self.paginator.table.get_url(page=self.number)
