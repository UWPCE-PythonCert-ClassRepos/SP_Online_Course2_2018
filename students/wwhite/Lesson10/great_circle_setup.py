import setuptools  # important
from distutils.core import setup
from Cython.Build import cythonize

setup(
    name='Great Circle',
    ext_modules=cythonize("great_circle.pyx", build_dir="build"),
                                           script_args=['build'],
                                           options={'build':{'build_lib':'.'}})