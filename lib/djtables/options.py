#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.core.paginator import Paginator
from .row import Row
from .cell import Cell


class Options(object):
    _defaults = { }

    def __init__(self, options=None, **kwargs):

        # if an object was given, pluck our options from its attrs (like
        # django's confusingly-named Meta class). copy the attrs first,
        # to avoid trashing the object while we iterate it.
        options = (options is not None)\
            and options.__dict__.copy() or {}

        # keyword args are hard-coded options, so should override those
        # from the options object. (but they must still be valid.)
        options.update(kwargs)

        # store each option (except for _private and __magic__). setattr
        # will raise if ANY are invalid, like django. this seems kind of
        # heavy-handed (especially since i've wanted to add my own Meta
        # options to models before), but i'm following for consistency.
        for key in options.keys():
            if not key.startswith("_"):
                value = options.pop(key)
                setattr(self, key, value)

        # store any defaults which were not overridden.
        for key, value in self._defaults.items():
            if not hasattr(self, key):
                setattr(self, key, value)

    def __setattr__(self, name, value):
        if name in self._defaults:  object.__setattr__(self, name, value)
        else:  raise AttributeError("Invalid option: %s" % name)

    def fork(self, **kwargs):
        return self.__class__(self, **kwargs)


class TableOptions(Options):
    _defaults = {
        'paginator_class': Paginator,
        'row_class': Row,
        'cell_class': Cell,

        'prefix': "",
        'order_by': None,
        'per_page': 20,
        'page': 1,

        "template": "djtables/table.html",

        'columns': []
    }
