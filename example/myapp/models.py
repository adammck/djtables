#!/usr/bin/env python
# vim: et ts=4 sw=4


from django.conf import settings
from django.db import models


GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female") )


class Human(models.Model):
    name   = models.CharField(max_length=30, unique=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    dob    = models.DateField(verbose_name="Date of Birth")
    phone  = models.CharField(max_length=12)
    email  = models.EmailField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<%s: %s>' %\
            (type(self).__name__, self)
