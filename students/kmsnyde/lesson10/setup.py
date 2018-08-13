# -*- coding: utf-8 -*-
"""
Created on Wed Aug  8 17:31:53 2018

@author: HP-Home
"""

from distutils.core import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize("polynomial_cy.pyx"))