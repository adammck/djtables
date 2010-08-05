#!/usr/bin/env python
# vim: et ts=4 sw=4


import datetime
from fudge import Fake
from djtables.column import DateColumn


# override the django DATE_FORMAT setting to make it predictable.
def setup():
    from django.conf import settings
    settings.__old_date_format = settings.DATE_FORMAT
    settings.DATE_FORMAT = "Y-m-d"


# restore the previous setting, to avoid screwing with global state.
def teardown():
    from django.conf import settings
    settings.DATE_FORMAT = settings.__old_date_format
    del settings.__old_date_format


def test_datecolumn_formats_dates():
    date = datetime.date(2010, 1, 1)
    cell = Fake().has_attr(value=date)
    column = DateColumn(format="D d M Y")
    assert column.render(cell) == "Fri 01 Jan 2010"


def test_datecolumn_defaults_to_DATE_FORMAT():
    date = datetime.date(2010, 1, 1)
    cell = Fake().has_attr(value=date)
    column = DateColumn()
    assert column.render(cell) == "2010-01-01"
