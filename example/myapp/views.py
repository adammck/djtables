#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.shortcuts import render_to_response
from .tables import MyTable
from .models import Human


def index(req):
    return render_to_response(
        "myapp/index.html", {
            "table": MyTable(Human.objects.all(), request=req) } )
