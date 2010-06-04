#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.core.management import execute_manager
import settings


if __name__ == "__main__":
    execute_manager(settings)
