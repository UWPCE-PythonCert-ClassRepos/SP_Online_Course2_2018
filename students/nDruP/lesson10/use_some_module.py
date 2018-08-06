import some_module
import cProfile
#from timeit import timeit as timer

print(some_module.hewwo())

#print(timer(lambda: run_fact()))

#print(timer(lambda: run_fibo()))

#print(timer(lambda: alt_run_fibo()))


cProfile.run('some_module.run_fact()')
cProfile.run('some_module.run_fibo()')
cProfile.run('some_module.alt_run_fibo()')
