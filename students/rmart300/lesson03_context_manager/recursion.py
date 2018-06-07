

def factorial(n):

    product = n
    if n > 1:
        product *= factorial(n-1)

    return product

if __name__ == '__main__':

    for i in range(1,11):
        print(f"{i}! = {factorial(3)}")
