from distutils.core import setup
from Cython.Build import cythonize

setup(
    name="great_circle_v1",
    ext_modules=cythonize("great_circle_v1.pyx")
)
