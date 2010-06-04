#!/usr/bin/env python
# vim: et ts=4 sw=4


import djangotables as tables
from .models import Human


class MyTable(tables.Table):
    name   = tables.Column()
    gender = tables.Column()


#class HumanTable(tables.ModelTable):
#    class Meta:
#        model = Human
#        exclude = ["id"]
#        order_by = "name"
