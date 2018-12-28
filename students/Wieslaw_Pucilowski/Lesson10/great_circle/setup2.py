from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize


ext_modules = [
    Extension("great_circle_v2",
              sources=["great_circle_v2.pyx"],
              libraries=["m"]  # Unix-like specific
              )
]

setup(
        name='Great Circle v2',
         ext_modules=cythonize(ext_modules)
)
