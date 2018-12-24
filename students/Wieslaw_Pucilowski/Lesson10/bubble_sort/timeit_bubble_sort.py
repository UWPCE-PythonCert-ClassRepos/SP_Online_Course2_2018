import random
from timeit import timeit as timer
import bubble_sort
import bubble_sort_cython


if __name__ == "__main__":
    
    my_list = random.sample(range(1000), 1000)
    repetitions = 100
    
    print("bubble sort python:", timer(
        'bubble_sort.bubble(my_list)',
        globals=globals(),
        number=repetitions
    ))
    
    print("bubble sort cython:", timer(
        'bubble_sort_cython.bubble(my_list)',
        globals=globals(),
        number=repetitions
    ))