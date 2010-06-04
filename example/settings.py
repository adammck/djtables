#!/usr/bin/env python
# vim: et ts=4 sw=4


DEBUG = True
TEMPLATE_DEBUG = DEBUG


DATABASE_ENGINE = "sqlite3"
DATABASE_NAME   = "db.sqlite3"


ROOT_URLCONF = "urls"


INSTALLED_APPS = (
    "djangotables",
    "myapp" )
