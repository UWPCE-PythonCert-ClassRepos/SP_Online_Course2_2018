@profile
def my_func():
    for i in range(20):
        a = [1] * (10 ** 6)
        b = [2] * (2 * 10 ** 7)
        del b
    return a

if __name__ == '__main__':
    my_func()