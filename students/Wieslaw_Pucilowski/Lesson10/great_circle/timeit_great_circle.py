lon1, lat1, lon2, lat2 = -72.345, 34.323, -61.823, 32.242
import great_circle_v0
import great_circle_v1
import great_circle_v2
from timeit import timeit as timer

repetitions = 1
loop = 1000000
def run_great_circle_py(repetitions):
    for i in range(repetitions):
        great_circle_v0.great_circle(lon1, lat1, lon2, lat2)

def run_great_circle_cython(repetitions):
    for i in range(repetitions):
        great_circle_v1.great_circle(lon1, lat1, lon2, lat2)

def run_great_circle_cython2(repetitions):
    for i in range(repetitions):
        great_circle_v2.great_circle(lon1, lat1, lon2, lat2)

if __name__ == "__main__":
    
    print("great circle python:", timer(
        'run_great_circle_py(loop)',
        globals=globals(),
        number=repetitions
    ))
    print("great circle cython:", timer(
        'run_great_circle_cython(loop)',
        globals=globals(),
        number=repetitions
    ))
    print("great circle cython C math lib:", timer(
        'run_great_circle_cython2(loop)',
        globals=globals(),
        number=repetitions
    ))