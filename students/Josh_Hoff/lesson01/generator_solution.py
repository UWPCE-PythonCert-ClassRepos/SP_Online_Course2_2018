def intsum():
    count = 0
    list = [0]
    n = 50
    while count < n:
        yield sum(list)
        count += 1
        list += [count]
    
def intsum2():
    count = 0
    list = [0]
    n = 50
    while count < n:
        yield sum(list)
        count += 1
        list += [count]
    
def doubler():
    count = 1
    n = 50000
    while count < n:
        yield count
        count *= 2
    
    
def fib():
    n = 0
    num0 = 0
    num1 = 1
    count = 1
    yield count
    while n < 100:
        if count % 2 == 0:
            num0 = num0 + num1
        else:
            num1 = num0 + num1
        n = num1 + num0
        count += 1
        yield n
        
            
    
def prime():
    primes = [2, 3, 5, 7, 11]
    primes += [x for x in range(2, 100) if x % 2 != 0 and x % 3 != 0 and x % 5 != 0 and x % 7 != 0 and x % 11 != 0]
    for i in primes:
        yield i
