#!/usr/bin/env python
# vim: et ts=4 sw=4


from fudge import Fake
from nose.tools import assert_raises
from djtables.column import Column, WrappedColumn


def test_sortable_by_order_of_creation():
    a, b, c = Column(), Column(), Column()
    assert sorted([b, a, c]) == [a, b, c]


def test_can_be_bound():
    table  = Fake()
    column = Column()

    column.bind_to(table, "alpha")

    assert column.is_bound == True
    assert column.bound_to == (table, "alpha")


def test_raises_if_rebound():
    table_a = Fake()
    table_b = Fake()
    column = Column()

    column.bind_to(table_a, "beta")

    assert_raises(AttributeError,
        column.bind_to, table_b, "gamma")


def test_can_be_explicitly_named():
    column = Column(name="delta")
    assert column.name == "delta"


def test_can_be_named_by_binding():
    table  = Fake()
    column = Column()

    column.bind_to(table, "epsilon")

    assert column.name == "epsilon"


def test_renders_values_to_unicode():
    bool_cell = Fake().has_attr(value=True)
    int_cell = Fake().has_attr(value=123)

    assert Column().render(bool_cell) == u"True"
    assert Column().render(int_cell) == u"123"


def test_value_can_be_wrapped():
    cell = Fake().has_attr(value="abc")
    column = Column(value=lambda cell: cell.value.upper())
    assert column.render(cell) == u"ABC"


def test_renders_name_to_unicode():
    assert unicode(Column('zeta')) == u"zeta"


def test_wrapped_column_wraps_column_attrs():
    table  = Fake()
    column = Fake().has_attr(eta=123)

    wrapped_column = WrappedColumn(table, column)
    wrapped_column.iota = 456

    assert wrapped_column.eta == 123
    assert wrapped_column.iota == 456

    # this isn't a very good test. because __magic__ methods can't be
    # mocked by fudge, we'll just check unicode(WrappedColumn) returns
    # the predictable output of unicode(Fake).
    assert unicode(wrapped_column) == "fake:column"


def test_wrapped_column_is_sorted_via_table():
    meta     = Fake().has_attr(order_by="kappa")
    table    = Fake().has_attr(_meta=meta)
    column_a = Fake().has_attr(name="kappa")
    column_b = Fake().has_attr(name="mu")

    wrapped_column_a = WrappedColumn(table, column_a) # sorted
    wrapped_column_b = WrappedColumn(table, column_b) # unsorted

    assert wrapped_column_a.is_sorted == True
    assert wrapped_column_b.is_sorted == False
    assert wrapped_column_a.sort_direction == "asc"
    assert wrapped_column_b.sort_direction == None

    meta.has_attr(order_by="-mu")
    assert wrapped_column_a.is_sorted == False
    assert wrapped_column_b.is_sorted == True
    assert wrapped_column_a.sort_direction == None
    assert wrapped_column_b.sort_direction == "desc"


def test_wrapped_column_has_sort_url():
    meta   = Fake().has_attr(order_by="nu")
    table  = Fake().has_attr(_meta=meta)
    column_a = Fake().has_attr(name="nu")
    column_b = Fake().has_attr(name="xi")

    # mock out url building, to avoid awakening django.
    table.provides("get_url").calls(
        lambda order_by: ["omicron", order_by])

    wrapped_column_a = WrappedColumn(table, column_a)
    wrapped_column_b = WrappedColumn(table, column_b)

    assert wrapped_column_a.sort_url == ["omicron", "-nu"]
    assert wrapped_column_b.sort_url == ["omicron", "xi"]


def test_can_link():
    cell = Fake().has_attr(value="pi")
    linked_column = Column(link=lambda cell: cell.value.upper())
    unlinked_column = Column()

    assert linked_column.has_link == True
    assert linked_column.link(cell) == u"PI"

    assert unlinked_column.has_link == False
    assert unlinked_column.link(cell) == None


def test_can_specify_css_class():
    column_with_css = Column(css_class="rho")
    column_no_css = Column()

    assert column_with_css.has_css_class == True
    assert column_with_css.css_class == "rho"

    assert column_no_css.has_css_class == False
    assert column_no_css.css_class == None
