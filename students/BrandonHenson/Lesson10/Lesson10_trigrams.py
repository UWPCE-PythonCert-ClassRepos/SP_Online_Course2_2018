#!/usr/bin/env python3
import os
import sys
import random
import pathlib
import string
from memory_profiler import profile
from collections import defaultdict


REPLACE_DICT = {punc: '' for punc in string.punctuation}
REPLACE_DICT[';'] = ' '
REPLACE_DICT['#'] = ' '
REPLACE_DICT['-'] = ' '
REPLACE_DICT['@'] = ' '
REPLACE_DICT['*'] = ' '
TRANSLATION_TABLE = str.maketrans(REPLACE_DICT)


def make_trigram_dict(file_path):
    if not file_path.exists():
        return {}

    trigram_dict = defaultdict(list)
    previous_line = ''
    with open(file_path) as reader:
        for line in reader:
            line = line.translate(TRANSLATION_TABLE)
            line = f'{" ".join(previous_line.split()[-2:])} {line}'
            words = [word.upper() for word in line.split()]
            previous_line = line
            for i in range(len(words) - 2):
                trigram_dict[f'{words[i]} {words[i + 1]}'].append(words[i + 2])

    return trigram_dict


def make_trigram_text(trigram_dict, max_len):
    if isinstance(trigram_dict, defaultdict):
        trigram_dict.default_factory = None

    trigram_key = random.choice(list(trigram_dict))
    trigram_txt = list(trigram_key.split())

    while trigram_key in trigram_dict and len(trigram_txt) < max_len:
        trigram_txt.append(random.choice(trigram_dict[trigram_key]))
        trigram_key = f'{trigram_txt[-2]} {trigram_txt[-1]}'

    return ' '.join(trigram_txt)


@profile
def main():
    max_words = 200
    if len(sys.argv) > 1:
        try:
            max_words = int(sys.argv[1])
        except ValueError:
            pass

    path = os.getcwd()
    dirs = os.listdir(path)
    for file in dirs:
        if file.endswith('.txt'):
            print(file)
            book = file
            reader_path = pathlib.Path(os.path.join(os.getcwd(), book))
            trigram_dict = make_trigram_dict(reader_path)
            trigram_text = make_trigram_text(trigram_dict, max_words)
            print(trigram_text)
        else:
            pass


if __name__ == '__main__':
    main()
