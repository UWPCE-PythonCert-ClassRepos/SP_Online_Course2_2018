# Lesson 10 memory profiler exercise
# Modified from Course 1 Lesson 04 Kata Fourteen
# !/usr/bin/env python3
# using text file from The Project Gutenberg EBook of The Call of the Wild by Jack London
# creates trigrams from entire book  

@profile
def write_new_book(tri):
    import random
    new_text = ["..."]
    start = (random.choice(list(tri.keys())))
    new_text.append(start[0])
    new_text.append(start[1])
    for i in range(1000000): # increased for memory profiler exercise
        nxt = tuple(new_text[-2:])
        if nxt not in tri:
            new_text.append("\n\n Word Count: {}".format(len(new_text)))
            break
        else:
            new_text.append(random.choice(list(tri.get(nxt))))
    with open("New Text by Courtney Whole Book.txt.", "w", encoding = "utf8") as new_file:
        for word in new_text:
            new_file.write(word)
            new_file.write(" ")

@profile            
def read_book():
    trigrams = {}
    words_in_book = []
    with open("The Call of the Wild.txt", "r", encoding = "utf8") as book:
        lines = book.readlines()
        lines = lines[54:3064] # 421 reads only chapter 1, use 3064 for whole book
    for line in lines:
        for word in line.split():
            words_in_book.append(word)
    for n in range(len(words_in_book)-2):
        pair = words_in_book[n], words_in_book[n+1]
        follower = words_in_book[n+2]
        if pair in trigrams and follower not in trigrams[pair]:
            trigrams[pair].append(follower)
        if pair in trigrams and follower in trigrams[pair]:
            pass
        else:
            trigrams[pair] = [follower]
    write_new_book(trigrams)


if __name__ == '__main__':
    read_book()

""" python -m memory_profiler output:
Filename: memprof_trigram_wholebook.py

Line #    Mem usage    Increment   Line Contents
================================================
     7   39.383 MiB   39.383 MiB   @profile
     8                             def write_new_book(tri):
     9   39.383 MiB    0.000 MiB       import random
    10   39.383 MiB    0.000 MiB       new_text = ["..."]
    11   39.559 MiB    0.176 MiB       start = (random.choice(list(tri.keys())))
    12   39.559 MiB    0.000 MiB       new_text.append(start[0])
    13   39.559 MiB    0.000 MiB       new_text.append(start[1])
    14   46.996 MiB    0.008 MiB       for i in range(1000000): # increased for memory profiler exercise
    15   46.996 MiB    0.062 MiB           nxt = tuple(new_text[-2:])
    16   46.996 MiB    0.000 MiB           if nxt not in tri:
    17                                         new_text.append("\n\n Word Count: {}".format(len(new_text)))
    18                                         break
    19                                     else:
    20   46.996 MiB    0.609 MiB               new_text.append(random.choice(list(tri.get(nxt))))
    21   46.996 MiB    0.000 MiB       with open("New Text by Courtney Whole Book.txt.", "w", encoding = "utf8") as new_file:
    22   47.332 MiB    0.004 MiB           for word in new_text:
    23   47.328 MiB    0.062 MiB               new_file.write(word)
    24   47.328 MiB    0.223 MiB               new_file.write(" ")


Filename: memprof_trigram_wholebook.py

Line #    Mem usage    Increment   Line Contents
================================================
    26   32.824 MiB   32.824 MiB   @profile
    27                             def read_book():
    28   32.824 MiB    0.000 MiB       trigrams = {}
    29   32.824 MiB    0.000 MiB       words_in_book = []
    30   32.824 MiB    0.000 MiB       with open("The Call of the Wild.txt", "r", encoding = "utf8") as book:
    31   33.184 MiB    0.359 MiB           lines = book.readlines()
    32   33.184 MiB    0.000 MiB           lines = lines[54:3064] # 421 reads only chapter 1, use 3064 for whole book
    33   35.383 MiB    0.000 MiB       for line in lines:
    34   35.383 MiB    0.062 MiB           for word in line.split():
    35   35.383 MiB    0.180 MiB               words_in_book.append(word)
    36   39.383 MiB    0.000 MiB       for n in range(len(words_in_book)-2):
    37   39.383 MiB    0.062 MiB           pair = words_in_book[n], words_in_book[n+1]
    38   39.383 MiB    0.000 MiB           follower = words_in_book[n+2]
    39   39.383 MiB    0.000 MiB           if pair in trigrams and follower not in trigrams[pair]:
    40   39.383 MiB    0.062 MiB               trigrams[pair].append(follower)
    41   39.383 MiB    0.000 MiB           if pair in trigrams and follower in trigrams[pair]:
    42   39.383 MiB    0.000 MiB               pass
    43                                     else:
    44   39.383 MiB    0.562 MiB               trigrams[pair] = [follower]
    45   39.699 MiB   39.699 MiB       write_new_book(trigrams)
    
"""    

""" python -m cProfile output (removed frozen importlib, built in,
    and method lines for readability):

         9929918 function calls (9929875 primitive calls) in 4.756 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 __init__.py:43(normalize_encoding)
        1    0.000    0.000    0.000    0.000 __init__.py:71(search_function)
        1    0.000    0.000    0.000    0.000 bisect.py:1(<module>)
        1    0.000    0.000    0.000    0.000 codecs.py:185(__init__)
        1    0.000    0.000    0.000    0.000 codecs.py:259(__init__)
        1    0.000    0.000    0.000    0.000 codecs.py:308(__init__)
       26    0.000    0.000    0.000    0.000 codecs.py:318(decode)
        1    0.000    0.000    0.000    0.000 codecs.py:93(__new__)
       14    0.000    0.000    0.000    0.000 hashlib.py:116(__get_openssl_constructor)
        1    0.000    0.000    0.008    0.008 hashlib.py:54(<module>)
        8    0.000    0.000    0.000    0.000 hashlib.py:73(__get_builtin_constructor)
        1    0.046    0.046    4.753    4.753 memprof_trigram_wholebook.py:27(read_book)
        1    0.003    0.003    4.756    4.756 memprof_trigram_wholebook.py:8(<module>)
        1    1.965    1.965    4.699    4.699 memprof_trigram_wholebook.py:8(write_new_book)
  1000001    0.751    0.000    1.142    0.000 random.py:223(_randbelow)
  1000001    0.561    0.000    1.797    0.000 random.py:253(choice)
        1    0.000    0.000    0.010    0.010 random.py:38(<module>)
        1    0.000    0.000    0.000    0.000 random.py:664(SystemRandom)
        1    0.000    0.000    0.000    0.000 random.py:71(Random)
        1    0.000    0.000    0.000    0.000 random.py:87(__init__)
        1    0.000    0.000    0.000    0.000 random.py:96(seed)
        1    0.000    0.000    0.000    0.000 utf_8.py:33(getregentry)
        
  """