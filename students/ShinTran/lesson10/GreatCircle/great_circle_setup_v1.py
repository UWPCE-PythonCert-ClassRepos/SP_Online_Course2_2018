'''
Shin Tran
Pyton 220
Assignment 10

Dig into the compile and link steps required by Cython.
Work with setup files or any of the other methods to generate cython libraries
'''

from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='Great Circle v1',
    ext_modules=cythonize("great_circle_v1.pyx"),
)
