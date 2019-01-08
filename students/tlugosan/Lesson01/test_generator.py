#!/usr/bin/env python3

import pytest
import generators as gr

def test_sum_of_int():
    '''0 + 1 + 2 + 3 + 4 + 5 + … = 0, 1, 3, 6, 10, 15 …'''
    s1 = gr.sum_of_int(10)
    assert next(s1) == 0
    assert next(s1) == 1
    assert next(s1) == 3
    assert next(s1) == 6
    assert next(s1) == 10
    assert next(s1) == 15

def test_doubler():
    '''1, 2, 4, 8, 16, 32, ...'''
    d1 = gr.doubler(20)
    assert next(d1) == 1
    assert next(d1) == 2
    assert next(d1) == 4
    assert next(d1) == 8
    assert next(d1) == 16


def test_fibo():
    '''1, 1, 2, 3, 5, 8, 13, 21, 34, ...'''
    f1 = gr.fibo(30)
    assert next(f1) == 1
    assert next(f1) == 1
    assert next(f1) == 2
    assert next(f1) == 3
    assert next(f1) == 5
    assert next(f1) == 8

def test_prime_numbers():
    '''2, 3, 5, 7, 11, 13, 17, 19, 23…'''
    p1 = gr.prime_numbers(30)
    assert next(p1) == 2
    assert next(p1) == 3
    assert next(p1) == 5
    assert next(p1) == 7
    assert next(p1) == 11
    assert next(p1) == 13
    assert next(p1) == 17
    assert next(p1) == 19


def test_squared():
    ''' 1, 4, 9, 16, 25, 36, ...'''
    s1 = gr.squared(40)
    assert next(s1) == 1
    assert next(s1) == 4
    assert next(s1) == 9
    assert next(s1) == 16
    assert next(s1) == 25
    assert next(s1) == 36


def test_cubed():
    '''1, 8, 27, 64, 125, 216'''
    c1 = gr.cubed(300)
    assert next(c1) == 1
    assert next(c1) == 8
    assert next(c1) == 27
    assert next(c1) == 64
    assert next(c1) == 125
    assert next(c1) == 216


def test_count_by():
    ''''''
    cb1 = gr.counting_by(20, 3)
    assert next(cb1) == 1
    assert next(cb1) == 4
    assert next(cb1) == 7
    assert next(cb1) == 10
    assert next(cb1) == 13
    assert next(cb1) == 16
    assert next(cb1) == 19

    cb2 = gr.counting_by(-40, -7)
    assert next(cb2) == 1
    assert next(cb2) == -6
    assert next(cb2) == -13
    assert next(cb2) == -20
    assert next(cb2) == -27
    assert next(cb2) == -34
