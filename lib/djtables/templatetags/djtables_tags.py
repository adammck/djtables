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
    
    @property
    def current_page_number(self):
        return self.table._meta.page
    
    @property
    def first_page_url(self):
        return self.table.get_url(page=1)
    
    @property
    def previous_page_url(self):
        if self.table.paginator.page(self.current_page_number).has_previous():
            return self.table.get_url(page=self.table.paginator.page(self.current_page_number).previous_page_number())
    
    @property
    def next_page_url(self):
        if self.table.paginator.page(self.current_page_number).has_next():
            return self.table.get_url(page=self.table.paginator.page(self.current_page_number).next_page_number())
    
    @property
    def last_page_url(self):
        return self.table.get_url(page=self.table.paginator.num_pages)
    
    def url(self):
        return self.table.get_url(page=self.number)
