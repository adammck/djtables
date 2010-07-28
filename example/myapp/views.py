#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.shortcuts import render_to_response, get_object_or_404
from .tables import MyTable
from .models import Human


def index(req):
    return render_to_response(
        "myapp/index.html", {
            "table": MyTable(Human.objects.all(), request=req) } )


def edit(req, pk):
    return render_to_response(
        "myapp/edit.html", {
            "human": get_object_or_404(Human, pk=pk) } )
