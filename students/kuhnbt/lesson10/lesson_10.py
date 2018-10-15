import time

def fibonacci(num):
    if num == 0:
        return 0
    elif num == 1:
        return 1
    else:
        return fibonacci(num-2) + fibonacci(num-1)

cache = {}    
def memoize_fibonacci(idx):
    if idx == 0:
        return 0
    elif idx == 1:
        return 1
    else:
        if cache.get(idx):
            return cache.get(idx)
        cache[idx] = memoize_fibonacci(idx-2) + memoize_fibonacci(idx-1)
        return cache[idx]

start = time.time()
fib_results = [fibonacci(i) for i in range(40)]
end = time.time()

print('Normal fibonacci function took {} seconds'.format(end-start))

start = time.time()
fib_memoized_results = [memoize_fibonacci(i) for i in range(40)]
end = time.time()

print('Memoized fibonacci function took {} seconds'.format(end-start))

print('Results are the same: {}'.format(fib_results == fib_memoized_results))


# Function to apply caching to a generic function

def memoize(func):
    cache = {}
    def memoized_function(n):
        if cache.get(n):
            print(n,"already in cache")
            return cache.get(n)
        result = func(n)
        cache[n] = result
        return result
    
    return memoized_function

# Memoize fibonacci function using a decorator

@memoize
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

start = time.time()
fib_memoized_results_2 = [fib(i) for i in range(40)]
end = time.time()

print('Memoized fibonacci with decorator took {} seconds'.format(end - start))
print('Results are the same: {}'.format(fib_memoized_results_2 == fib_results))

# Now without using a decorator

def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)

memo_fib = memoize(fib)

start = time.time()
fib_memoized_results_3 = [memo_fib(i) for i in range(40)]
end = time.time()

print('Memoized fibonacci with wrapper function took {} seconds'.format(end-start))
print('Results are the same: {}'.format(fib_memoized_results_3 == fib_results))

