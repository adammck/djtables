#!/usr/bin/env python
# vim: et ts=4 sw=4


from setuptools import setup


setup(
    name="djtables",
    version="0.1.0",
    license="BSD",

    author="Adam Mckaig",
    author_email="adam.mckaig@gmail.com",

    description="Declarative HTML table builder for Django",
    url="http://github.com/adammck/djtables",

    package_dir={"": "lib"},
    packages=["djtables"])
