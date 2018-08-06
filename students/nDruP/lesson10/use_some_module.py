import some_module
import cProfile
from timeit import timeit as timer

#print(timer(lambda: some_module.run_fact()))
#print(timer(lambda: some_module.run_fibo()))
#print(timer(lambda: some_module.alt_run_fibo()))

#cProfile.run('some_module.run_fact()')
#cProfile.run('some_module.run_fibo()')
#cProfile.run('some_module.alt_run_fibo()')

if __name__ == '__main__':
    pr = cProfile.Profile()

    pr.enable()
    some_module.run_fact()
    some_module.run_fibo()
    some_module.alt_run_fibo()
    pr.disable()
    pr.print_stats(sort='time')
