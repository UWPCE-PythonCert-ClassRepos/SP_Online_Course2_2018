def sum_integers(start=0):
    count=start
    while True:
        yield start
        count += 1
        start += count 
        
def doubler(start=1):
    while True:
        yield start
        start*=2
        
def fibonacci():
    a = 0
    b = 1
    yield a
    while True:
        yield b
        temp = b
        b += a
        a = temp
        
def prime_number_generator(start):
    while True:
        for num in range(2, start // 2 + 1):
            if start % num == 0:
                break
        else:
            yield start
        start += 1
            
def x_to_n(x=2, n=2):
    while True:
        yield x
        x = x**n