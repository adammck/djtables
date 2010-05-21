#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.http import QueryDict
from tables.urls import extract, build


def test_returns_empty_dict():
    assert extract(QueryDict("", encoding="utf-8")) == { }


def test_extracts_order_by():
    qs = QueryDict("order_by=x", encoding="utf-8")
    assert extract(qs) == { 'order_by': "x" }


def test_casts_page_number_to_int():
    qs = QueryDict("page=1", encoding="utf-8")
    assert extract(qs) == { 'page': 1 }


def test_prepends_prefixes_to_parameters():
    qs = QueryDict("a-order_by=x;b-order_by=y", encoding="utf-8")
    assert extract(qs, prefix="a-") == { 'order_by': "x" }
    assert extract(qs, prefix="b-") == { 'order_by': "y" }


def test_accepts_multiple_values_in_query_string():
    qs = QueryDict("order_by=x&order_by=y", encoding="utf-8")
    assert extract(qs) == { 'order_by': "y" }


def test_rebuilds_urls():
    qs = QueryDict("order_by=x", encoding="utf-8")
    assert build("/", qs) == "/?order_by=x"


def test_adds_parameters():
    qs = QueryDict("order_by=x", encoding="utf-8")
    assert build("/", qs, page=1) == "/?order_by=x&page=1"


def test_overrides_parameters():
    qs = QueryDict("order_by=x", encoding="utf-8")
    assert build("/", qs, order_by="y") == "/?order_by=y"
