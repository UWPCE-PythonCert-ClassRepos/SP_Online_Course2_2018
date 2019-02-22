from distutils.core import setup
from Cython.Build import cythonize

setup(
      name = 'Great Circle v4',
      ext_modules=cythonize("great_circle_v4.pyx"),
)