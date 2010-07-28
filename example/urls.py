#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.conf.urls.defaults import *
import myapp.views


urlpatterns = patterns("",
    url(r"^$",           myapp.views.index, name="index"),
    url(r"^(\d+)/edit$", myapp.views.edit,  name="edit") )
