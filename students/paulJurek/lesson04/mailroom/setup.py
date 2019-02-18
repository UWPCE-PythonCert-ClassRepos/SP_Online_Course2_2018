#!/usr/bin/env python

"""
simple setup file

"""

import os

from setuptools import setup, find_packages


def get_version():
    """
    Reads the version string from the package __init__ and returns it
    """
    with open(os.path.join("mailroom", "__init__.py")) as init_file:
        for line in init_file:
            parts = line.strip().partition("=")
            if parts[0].strip() == "__version__":
                return parts[2].strip().strip("'").strip('"')
    return None


setup(
    name='mailroom',
    version=get_version(),
    author='Paul Jurek',
    author_email='pjurek3@gmail.com',
    packages=find_packages(),
    # license='LICENSE.txt',
    description='Donation tracking appliation from command line',
    long_description=open('README.md').read(),
)
