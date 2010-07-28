#!/usr/bin/env python
# vim: et ts=4 sw=4


import datetime
from djangotables.column import DateColumn


# hackery: since this column uses a django template filter, we must
# configure the django settings explicitly before testing it.
def setup():
    from django.conf import settings
    settings.configure()


def test_datecolumn_formats_dates():
    date = datetime.date(2010, 1, 1)
    column = DateColumn(format="D d M Y")
    assert column.render(date) == "Fri 01 Jan 2010"
