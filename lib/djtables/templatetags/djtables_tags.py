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
    return {
        "pages": [
            WrappedPage(table, number)
            for number in table.paginator.page_range ],
        "num_columns": len(table.columns) }


class WrappedPage(object):
    def __init__(self, table, number):
        self.table = table
        self.number = number

    @property
    def is_active(self):
        return self.table._meta.page == self.number

    def url(self):
        return self.table.get_url(page=self.number)
