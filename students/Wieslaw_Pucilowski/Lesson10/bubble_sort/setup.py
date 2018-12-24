from distutils.core import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("bubble_sort_cython.pyx")
)
