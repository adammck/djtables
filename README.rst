DjTables: Declarative Tables for Django
=======================================

This is a Django app which renders querysets (and other sequences) into semantic HTML tables. It provides an API for defining tables (similar to django.forms), and template tags for rendering them.

This repo is **not** a fork of `Michael Elsdörfer's django-tables project`_. The two projects provide similar-looking interfaces, but are philosophically quite different. (I'm attempting to provide considerably more drop-in functionality, probably at the cost of tighter coupling.) You should definitely check out Michael's project. It's better documented than mine.

.. _Michael Elsdörfer's django-tables project: http://github.com/miracle2k/django-tables


Example
-------

This repo includes a demo Django project, which uses DjTables to display a sortable, paginated table of fictional people. It should be running at:

  http://djtables.adammck.com


Usage
=====


Defining Your Tables
--------------------

Your table(s) can be defined anywhere, but I like to keep them in a module named "tables.py" in your app. The most common use-case is to display a list of the instances of a model. Luckily, this is simple::

  class UsersTable(djtables.ModelTable):
      class Meta:
          model = Human

...and that's it. Additional columns can be defined in the class body (like Django models and forms), and the Meta (options) class can be used to override the default behavior of the table. A more complex example::

  class UsersTable(djtables.ModelTable):
      age = djtables.BooleanColumn(value=lambda u: u.get_age())

      class Meta:
          model = User
          exclude = ["password"]
          order_by = "date_joined"
          order_dir = "desc"
          default_page = -1
          per_page = 20


Instantiating a Table in Your View
----------------------------------

Here's where it gets awesome. Since the table class already knows which model it's rendering, you don't need to fuss around extracting the GET parameters, fetching a queryset, sorting it, and paginating it. Just instantiate the table, and it and pass it along to the template::

  def users_list(request):
      return render_to_response("template.html", {
          "users": UsersTable(request)
      })

Sorting and pagination come for free. the following requests are all handled in the way which (I hope) you would expect:

 - /users
 - /users?page=2
 - /users?sort=username
 - /users?sort=username;page=3

Table options can also be set per-instance, by passing them to the constructor. This is useful if the same table is rendered by multiple views, or multiple tables are rendered by a single view. For example::

  def users_and_groups_lists(request):
      return render_to_response("template.html", {
          "users": UsersTable(request, prefix="usr-"),
          "groups": GroupsTable(request, prefix="grp-")
      })

Both tables are rendered as usual, except the GET parameters used to navigate them prefixed to avoid clashes. The following are valid:

 - /whatever
 - /whatever?usr-page=2
 - /whatever?grp-sort=name
 - /whatever?usr-sort=username;usr-page=3;grp-page=2


Rendering a Table in Your Template
----------------------------------

If you don't have any special requirements for the HTML output, tables can render themselves like a Django form::

  {{ users.as_html }}

This is just a short way of saying::

  <table class="users">
      {% table_cols users %}
      {% table_head users %}
      {% table_body users %}
      {% table_foot users %}
  </table>

Any part of this template can be replaced with your own, without having to replace the entire thing (which is quite large).


License
=======
djtables is free software, available under the BSD license.
