"""
    demonstrate use of Redis
"""


import login_database


def build_mailroom():
    """
        uses non-presistent Redis only (as a cache)

    """

    try:
        r = login_database.login_redis_cloud()
        r.set('andy', 'andy@somewhere.com')
        email = r.get('andy')
        r.delete('andy')

        r.rpush('Peter Pan', '456-555-7946')
        r.rpush('Peter Pan', '97456')
        r.rpush('Peter Pan', 'PeterPan@email.com')
        r.rpush('Paul Hollywood', '503-555-6547')
        r.rpush('Paul Hollywood', 'Unknown')
        r.rpush('Paul Hollywood', 'Unknown')
        r.rpush('Mary Berry', '456-555-9874')
        r.rpush('Mary Berry', '97453')
        r.rpush('Mary Berry', 'MaryBerry@email.com')
        r.rpush('Jake Turtle', '503-555-6822')
        r.rpush('Jake Turtle', '97229')
        r.rpush('Jake Turtle', 'JakeTurtle@email.com')
        r.rpush('Raja Koduri', '503-555-6651')
        r.rpush('Raja Koduri', '92145')
        r.rpush('Raja Koduri', 'RajaKoduri@email.com')

        customer_names = ['Peter Pan', 'Paul Hollywood', 'Mary Berry',
                            'Jake Turtle', 'Raja Koduri']
        for customer in customer_names:
            phone = r.lindex(customer, 0)
            zipcode = r.lindex(customer, 1)
            email = r.lindex(customer, 2)
            print(f'Customer {customer} is located in {zipcode} and can be'
                    f' reached by phone at {phone} or by email at {email}')


    except Exception as e:
        print(f'Redis error: {e}')

if __name__ == '__main__':
    build_mailroom()