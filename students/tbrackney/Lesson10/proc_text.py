"""
File Name: proc_text.py
Author: Travis Brackney
Class: Python 220 - Self paced online
Date Created 3/20/2019
Python Version: 3.7.0

Compares memory usage processing a large text file using various methods.

Methods break the file into a list of strings, mirrors them, and creates
a new string with the results
"""

from memory_profiler import profile


# @profile
def read_text(input_file):
    """
    reads input from text file and splits into an array of one word strings
    """

    with open(input_file, 'r', encoding='utf8') as file:
        input = file.read()
        input = input.replace('\n', ' ')  # removes endlines
        return input.split()




def map_text(w):
    """
    simple map function to turn words into palindromes
    """
    return w + w[::-1]


def filter_text(w):
    """
    returns if word is over 4 characters long
    """
    return len(w) > 4


@profile
def map_filter(file):
    """
    processes text using map and filter functions above
    """
    input = read_text(file)
    output0 = map(map_text, filter(filter_text, input))
    return ' '.join(output0)


@profile
def map_lambda(file):
    """
    same filter function using inline lambdas
    """
    input = read_text(file)
    output1 = map(lambda w: w + w[::-1], filter(lambda w: len(w) > 4, input))
    return ' '.join(output1)

@profile
def comprehension(file):
    """
    Processes text using a list comprehension
    """
    input = read_text(file)
    list = [w + w[::-1] for w in input if (len(w) > 4)]
    return ' '.join(list)


if __name__ == '__main__':
    # Reads from text copy of Pride and Predujice by Jane Austen
    in_file = 'pride.txt'
    comp_string = comprehension(in_file)
    map_string = map_filter(in_file)
    map_lambda_string = map_lambda(in_file)

    # assert all lists are the same
    assert comp_string == map_string
    assert comp_string == map_lambda_string
    print(f'Length of comprehension list: {len(comp_string)}')
    print(f'Length of map list: {len(map_string)}')
    print(f'Length of map lambda list: {len(map_lambda_string)}')
    # print(map_lambda_list)
