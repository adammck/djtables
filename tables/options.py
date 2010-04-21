#!/usr/bin/env python
# vim: et ts=4 sw=4


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

        # iterate *the defaults* while moving the options into this
        # object, to leave only the unknown (invalid) attrs.
        for key, value in self._defaults.items():
            setattr(self, key, options.pop(key, value))

        # ignore __magic__ and _private methods from the object.
        invalids = filter(lambda o: not o.startswith("_"), options)

        # invalid options are fatal, like django. this seems kind of
        # heavy-handed (especially since i've wanted to add my own Meta
        # options to models, before), but i'm following for consistency.
        if invalids:
            raise AttributeError(
                "Invalid option(s): %s" %\
                    ", ".join(invalids))


class TableOptions(Options):
    _defaults = {
        'per_page': 20,
        'order_by': None }

