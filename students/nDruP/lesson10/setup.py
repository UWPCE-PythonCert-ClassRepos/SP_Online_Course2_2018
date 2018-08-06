from distutils.core import setup
from Cython.Build import cythonize

setup(name='Fibo_Factorial_hewwo',
      ext_modules=cythonize("some_module.pyx"))
