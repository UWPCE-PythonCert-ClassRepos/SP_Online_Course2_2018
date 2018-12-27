all: great_circle_v1.c great_circle_v1.html great_circle_v2.c great_circle_v2.html

great_circle_v1.c: great_circle_v1.pyx setup.py
    python setup.py build_ext --inplace

great_circle_v1.html: great_circle_v1.pyx
    cython -a great_circle_v1.pyx

great_circle_v2.c: great_circle_v2.pyx setup2.py
    python setup2.py build_ext --inplace

great_circle_v2.html: great_circle_v2.pyx
    cython -a great_circle_v2.pyx