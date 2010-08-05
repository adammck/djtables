#!/usr/bin/env python
# vim: et ts=4 sw=4


from setuptools import setup


setup(
    name="djtables",
    version="0.1.1",
    license="BSD",

    install_requires = [
        "django"
    ],

    package_dir={"": "lib"},
    packages=["djtables"],
    include_package_data=True,

    author="Adam Mckaig",
    author_email="adam.mckaig@gmail.com",

    description="Declarative HTML table builder for Django",
    url="http://github.com/adammck/djtables"
)
