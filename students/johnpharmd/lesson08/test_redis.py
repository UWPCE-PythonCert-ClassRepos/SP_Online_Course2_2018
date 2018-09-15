"""
    test file for experimenting with redis
"""

# import login_database
# import utilities
from random import choice as rc


def create_random_phone():
    area = rc(['206-', '360-', '425-'])
    prefix = rc(['234-', '321-', '456-', '987-'])
    suffix = rc(['1212', '2789', '3767', '4123', '5555'])
    return area + prefix + suffix


def choose_random_zip():
    return rc(['98101', '98112', '98127', '98155'])


def run_example():
    names = ('Andrew', 'Peter', 'Susan', 'Pam', 'Steven', 'Charlotte')
    # fields = (':telephone', ':zip')
    # r = login_database.login_redis_cloud()

    try:
        for name in names:
            # r.set(customer, create_random_phone())
            # r.set(customer, choose_random_zip())
            print('customer:' + name + ':telephone,', create_random_phone())
            print('customer:' + name + ':zip,', choose_random_zip())

    except Exception as e:
        print(f'Redis error: {e}')


if __name__ == '__main__':
    run_example()
