python -c "from distutils.core import setup; from Cython.Build import cythonize;setup(name='cython app', ext_modules=cythonize('*.pyx'))" build_ext --inplace
