all: bubble_sort_cython.c bubble_sort_cython.html

bubble_sort_cython.c: bubble_sort_cython.pyx setup.py
    python setup.py build_ext --inplace

bubble_sort_cython.html: bubble_sort_cython.pyx
    cython -a bubble_sort_cython.pyx