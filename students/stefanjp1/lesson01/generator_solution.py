
def intsum():
    x = 0
    x_sum = 0
    while True:
        x_sum += x
        yield x_sum
        x += 1

def intsum2():
    x = 0
    x_sum = 0
    while True:
        x_sum += x
        yield x_sum
        x += 1

def doubler():
    x = 1
    while True:
        yield x
        x = x + x
        
def fib():
    x = 1
    x_1 = 0
    x_2 = 0
    while True:
        yield x
        x_2 = x_1
        x_1 = x
        x = x_1 + x_2

def prime():
    x = 2
    while True:
        valid_divisors = 0
        
        for div in range(1,x+1):
            if x % div == 0:
                valid_divisors += 1
                
        if valid_divisors == 2 or x == 2:
            yield x
            x += 1
            
        else:
            x += 1