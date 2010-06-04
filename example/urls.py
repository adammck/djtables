#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.conf.urls.defaults import *
import myapp.views


urlpatterns = patterns("",
    url("$", myapp.views.index) )
