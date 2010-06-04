#!/usr/bin/env python
# vim: et ts=4 sw=4


from django import template
register = template.Library()


@register.inclusion_tag("djangotables/cols.html")
def table_cols(table):
    return {
        "columns": [
            ColumnStub(table, column)
            for column in table.columns ] }


@register.inclusion_tag("djangotables/head.html")
def table_head(table):
    return {
        "columns": [
            ColumnStub(table, column)
            for column in table.columns ] }


@register.inclusion_tag("djangotables/body.html")
def table_body(table):
    return {
        "table": table }


@register.inclusion_tag("djangotables/foot.html")
def table_foot(table):
    return {
        "pages": [
            PageStub(table, number)
            for number in table.paginator.page_range ],
        "column_length": len(table.columns) }


class PageStub(object):
    def __init__(self, table, number):
        self.table = table
        self.number = number

    @property
    def is_active(self):
        return self.table._meta.page == self.number

    def url(self):
        return self.table.get_url(page=self.number)


class ColumnStub(object):
    def __init__(self, table, column):
        self.table = table
        self.column = column

    def sort_url(self):
        return self.table.get_url(order_by=self.column.name)

    def is_sorted(self):
        return self.table._meta.order_by == self.column.name

    def sort_direction(self):
        return "asc"

    def __unicode__(self):
        return unicode(self.column)

    def __getattr__(self, name):
        return getattr(self.column, name)
