# Lesson 10 memory profiler exercise
# Modified from Course 1 Lesson 04 Kata Fourteen
#!/usr/bin/env python3
#using text file from The Project Gutenberg EBook of The Call of the Wild by Jack London
#creates trigrams from Chapter 1 only

@profile
def write_new_book(tri):
    import random
    new_text = ["..."]
    start = (random.choice(list(tri.keys())))
    new_text.append(start[0])
    new_text.append(start[1])
    for i in range(10000):
        nxt = tuple(new_text[-2:])
        if nxt not in tri:
            new_text.append("\n\n Word Count: {}".format(len(new_text)))
            break
        else:
            new_text.append(random.choice(list(tri.get(nxt))))
    with open("New Text by Courtney.txt.", "w", encoding = "utf8") as new_file:
        for word in new_text:
            new_file.write(word)
            new_file.write(" ")

@profile       
def read_book():
    trigrams = {}
    words_in_book = []
    with open("The Call of the Wild.txt", "r", encoding = "utf8") as book:
        lines = book.readlines()
        lines = lines[54:421] #reads only chapter 1, use 3064 for whole book
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
Filename: memprof_trigram_chapter1.py

Line #    Mem usage    Increment   Line Contents
================================================
     7   33.418 MiB   33.418 MiB   @profile
     8                             def write_new_book(tri):
     9   33.418 MiB    0.000 MiB       import random
    10   33.418 MiB    0.000 MiB       new_text = ["..."]
    11   33.418 MiB    0.000 MiB       start = (random.choice(list(tri.keys())))
    12   33.418 MiB    0.000 MiB       new_text.append(start[0])
    13   33.418 MiB    0.000 MiB       new_text.append(start[1])
    14   33.422 MiB    0.000 MiB       for i in range(10000):
    15   33.422 MiB    0.000 MiB           nxt = tuple(new_text[-2:])
    16   33.422 MiB    0.000 MiB           if nxt not in tri:
    17   33.422 MiB    0.000 MiB               new_text.append("\n\n Word Count: {}".format(len(new_text)))
    18   33.422 MiB    0.000 MiB               break
    19                                     else:
    20   33.422 MiB    0.004 MiB               new_text.append(random.choice(list(tri.get(nxt))))
    21   33.422 MiB    0.000 MiB       with open("New Text by Courtney.txt.", "w", encoding = "utf8") as new_file:
    22   33.715 MiB    0.000 MiB           for word in new_text:
    23   33.715 MiB    0.227 MiB               new_file.write(word)
    24   33.715 MiB    0.000 MiB               new_file.write(" ")


Filename: memprof_trigram_chapter1.py

Line #    Mem usage    Increment   Line Contents
================================================
    26   32.461 MiB   32.461 MiB   @profile
    27                             def read_book():
    28   32.461 MiB    0.000 MiB       trigrams = {}
    29   32.461 MiB    0.000 MiB       words_in_book = []
    30   32.461 MiB    0.000 MiB       with open("The Call of the Wild.txt", "r", encoding = "utf8") as book:
    31   32.789 MiB    0.328 MiB           lines = book.readlines()
    32   32.789 MiB    0.000 MiB           lines = lines[54:421] #reads only chapter 1, use 3064 for whole book
    33   32.852 MiB    0.000 MiB       for line in lines:
    34   32.852 MiB    0.004 MiB           for word in line.split():
    35   32.852 MiB    0.031 MiB               words_in_book.append(word)
    36   33.418 MiB    0.000 MiB       for n in range(len(words_in_book)-2):
    37   33.418 MiB    0.062 MiB           pair = words_in_book[n], words_in_book[n+1]
    38   33.418 MiB    0.000 MiB           follower = words_in_book[n+2]
    39   33.418 MiB    0.000 MiB           if pair in trigrams and follower not in trigrams[pair]:
    40   33.418 MiB    0.004 MiB               trigrams[pair].append(follower)
    41   33.418 MiB    0.000 MiB           if pair in trigrams and follower in trigrams[pair]:
    42   33.418 MiB    0.000 MiB               pass
    43                                     else:
    44   33.418 MiB    0.141 MiB               trigrams[pair] = [follower]
    45   33.715 MiB   33.715 MiB       write_new_book(trigrams)

"""    

""" python -m cProfile output (removed frozen importlib, built in,
    and method lines for readability):

         69139 function calls (69096 primitive calls) in 0.079 seconds

   Ordered by: standard name

   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.000    0.000    0.000    0.000 __init__.py:43(normalize_encoding)
        1    0.000    0.000    0.035    0.035 __init__.py:71(search_function)
        1    0.000    0.000    0.000    0.000 bisect.py:1(<module>)
        1    0.000    0.000    0.000    0.000 codecs.py:185(__init__)
        1    0.000    0.000    0.000    0.000 codecs.py:259(__init__)
        1    0.000    0.000    0.000    0.000 codecs.py:308(__init__)
       26    0.000    0.000    0.000    0.000 codecs.py:318(decode)
        1    0.035    0.035    0.035    0.035 codecs.py:93(__new__)
       14    0.000    0.000    0.000    0.000 hashlib.py:116(__get_openssl_constructor)
        1    0.000    0.000    0.003    0.003 hashlib.py:54(<module>)
        8    0.000    0.000    0.000    0.000 hashlib.py:73(__get_builtin_constructor)
        1    0.004    0.004    0.079    0.079 memprof_trigram_chapter1.py:27(read_book)
        1    0.000    0.000    0.079    0.079 memprof_trigram_chapter1.py:8(<module>)
        1    0.016    0.016    0.038    0.038 memprof_trigram_chapter1.py:8(write_new_book)
     6313    0.004    0.000    0.007    0.000 random.py:223(_randbelow)
     6313    0.003    0.000    0.011    0.000 random.py:253(choice)
        1    0.000    0.000    0.004    0.004 random.py:38(<module>)
        1    0.000    0.000    0.000    0.000 random.py:664(SystemRandom)
        1    0.000    0.000    0.000    0.000 random.py:71(Random)
        1    0.000    0.000    0.000    0.000 random.py:87(__init__)
        1    0.000    0.000    0.000    0.000 random.py:96(seed)
        1    0.000    0.000    0.035    0.035 utf_8.py:33(getregentry)
    """