#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.core.urlresolvers import reverse
import djangotables as tables
from .models import Human


class MyTable(tables.Table):
    name   = tables.Column(link=lambda cell: reverse("edit", args=[cell.row.pk]))
    gender = tables.Column(value=lambda cell: cell.object.get_gender_display())
    phone  = tables.Column(sortable=False)
    
    class Meta:
        per_page = 4
        order_by = "name"


#class HumanTable(tables.ModelTable):
#    class Meta:
#        model = Human
#        exclude = ["id"]
#        order_by = "name"
