def func1(juice):
    n = 0
    for i in range(juice):
        n += i
    return n


big_range = 15000000
func1(big_range)
n = 0
for i in range(big_range):
    n += i
print(n)
