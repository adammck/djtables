#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.core.urlresolvers import reverse
from djtables import Table, Column
from .models import Human


class MyTable(Table):
    name   = Column(link=lambda cell: reverse("edit", args=[cell.row.pk]))
    gender = Column(value=lambda cell: cell.object.get_gender_display())
    phone  = Column(sortable=False)
    
    class Meta:
        per_page = 4
        order_by = "name"
