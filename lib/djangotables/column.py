#!/usr/bin/env python
# vim: et ts=4 sw=4


import datetime
from django.template import defaultfilters


class Column(object):

    """
    This class represents a table column. It is responsible for holding
    metadata, and rending table cells. Like Django model/fields, columns
    are usually created within the table class which they are bound to.
    """

    creation_counter = 0

    def __init__(self, name=None, value=None, link=None, sortable=True):
        self._name = name
        self._value = value
        self._link = link
        self.sortable = sortable

        # like django fields, keep track of the order which columns are
        # created, so they can be sorted later. (unfortunately, python
        # attrs are passed to __new__ as an unsorted dict, so we must
        # keep track of this manually to avoid random column order.)
        self.creation_counter = Column.creation_counter
        Column.creation_counter += 1

        self.bound_to = None

    def __lt__(self, other):
        """Allow columns to be sorted by order of creation."""
        return self.creation_counter < other.creation_counter

    def __unicode__(self):
        return self.name

    def bind_to(self, table, name):
        """
        Bind this column to a table, and assign it a name. This method
        can only be called once per instance, because a Column cannot be
        bound to multiple tables. (The sort order would be ambiguous.)
        """

        if self.bound_to is not None:
            raise AttributeError(
                "Column is already bound to '%s' as '%s'" %\
                    self.bound_to)

        self.bound_to = (table, name)

    @property
    def is_bound(self):
        """Return true if this column is bound to a table."""
        return (self.bound_to is not None)

    @property
    def name(self):
        """Return the column name, whether explicit or implicit."""
        return self._name or self.bound_to[1]

    def value(self, cell):
        """
        Extract the value of ``cell``, ready to be rendered.

        If this Column was instantiated with a ``value`` attribute, it
        is called here to provide the value. (For example, to provide a
        calculated value.) Otherwise, ``cell.value`` is returned.
        """

        if self._value is not None:
            return self._value(cell)

        else:
            return cell.value

    def render(self, cell):
        """
        Render ``cell``, ready for display. The default behavior is to
        simply cast its value to unicode, but this may be overridden by
        child classes to do something more useful.
        """

        return unicode(self.value(cell))

    @property
    def has_link(self):
        """Return True if this column contains links."""
        return self._link is not None

    def link(self, cell):
        """
        Return the URL which ``cell`` should link to, or None if this
        column does not contain links.

        If this Column was instantiated with a ``link`` attribute, it is
        called here (with a single parameter of ``cell``), to provide
        the value. Otherwise, None is returned.
        """

        if self.has_link:
            return self._link(cell)

        return None


class DateColumn(Column):

    """
    This class provides a simple way to render a Date field, using the
    Django 'date' template filter. The ``format`` argument specifies the
    string in ``Django date format``_, **not** ``Python date format``_.
    If ``format`` is None the ``DATE_FORMAT`` setting is used.

    .. `Django date format``: http://docs.djangoproject.com/en/dev/ref/templates/builtins/#ttag-now
    .. `Python date format``: http://docs.python.org/library/datetime.html#strftime-strptime-behavior
    """

    def __init__(self, format=None, *args, **kwargs):
        super(DateColumn, self).__init__(*args, **kwargs)
        self._format = format

    def render(self, cell):
        return defaultfilters.date(
            self.value(cell),
            self._format)


class WrappedColumn(object):

    """
    This class wraps a Column instance, and binds it to a Table instance
    to provide useful properties to the template. This represents a per-
    render instance of the column, containing its volatile state, such
    as sort order. (More properties, such as visibility, filtering, and
    grouping may come later.)

    All of the attributes (and methods) of the wrapped Column can be
    accessed via this class, with help from some __getattr__ magic.
    """

    def __init__(self, table, column):
        self.table = table
        self.column = column

    @property
    def sort_url(self):
        """
        Return the URL to sort the linked table by this column. If the
        table is already sorted by this column, the order is reversed.

        Since there is no canonical URL for a table the current URL (via
        the HttpRequest linked to the Table instance) is reused, and any
        unrelated parameters will be included in the output.
        """

        prefix = (self.sort_direction == "asc") and "-" or ""
        return self.table.get_url(order_by=prefix + self.name)

    @property
    def is_sorted(self):
        return self.sort_direction is not None

    @property
    def sort_direction(self):
        """
        Return the direction in which the linked table is is sorted by
        this column ("asc" or "desc"), or None this column is unsorted.
        """

        if self.table._meta.order_by == self.name:
            return "asc"

        elif self.table._meta.order_by == ("-" + self.name):
            return "desc"

        else:
            return None

    def __unicode__(self):
        return unicode(self.column)

    def __getattr__(self, name):
        return getattr(self.column, name)
