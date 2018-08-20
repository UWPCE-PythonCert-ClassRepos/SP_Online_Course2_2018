#!/usr/bin/env python3

# complicated_example.py


def main():
    x = 'main'
    one()


def one():
    y = 'one'
    two()


def two():
    z = 'two'
    long_loop()


def long_loop():
    z_count = 0
    for i in range(2, 1001, 5):
        for j in range(3, 1001, 7):
            for k in range(12, 1001):

                z = k / (i % k + j % k)
                # secret_print(z)
                z_count += 1
                print (z_count, 'z:', z, '  i, j, k:', i, j, k)

def secret_print(num):
    num


if __name__ == '__main__':
    print(main())
    print('last statement')
