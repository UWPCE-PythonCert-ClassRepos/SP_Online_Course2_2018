# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 15:05:47 2018

@author: HP-Home
"""

import timeit

py = timeit.timeit('''polynomial_py.iterate(5, 17)''', setup='import polynomial_py', number=100)

cy = timeit.timeit('''polynomial_cy.iterate(5, 17)''', setup='import polynomial_cy', number=100)

print(cy, py)
print('Cython is {}x faster'.format(py/cy))