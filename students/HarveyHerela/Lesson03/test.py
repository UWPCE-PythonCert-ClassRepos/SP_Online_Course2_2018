def factorial(num):
    if num <= 1:
        return 1
    else:
        return num * factorial(num-1)
    

if __name__ == "__main__":
    results = (1, 1, 2, 6, 24, 120, 720, 5040, 40320, 362880, 3628800, 39916800, 479001600, 6227020800, 87178291200)
    
    for i in range(0, len(results)):
        assert results[i] == factorial(i)

    
    
