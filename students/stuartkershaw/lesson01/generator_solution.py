def intsum(i=0, cur=0):
    while True:
        cur += i
        yield cur
        i += 1
