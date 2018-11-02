'''
Sean Tasaki
10/27/2018
Lesson03
'''


def factorial(num):
    if num < 1:
        return 1
    else:
        return num * factorial(num-1)

def answer(num):
        print('{}! = {}.'.format(num, factorial(num)))

if __name__ == '__main__':

    for num in range(0, 20):
        answer(num)
    
    