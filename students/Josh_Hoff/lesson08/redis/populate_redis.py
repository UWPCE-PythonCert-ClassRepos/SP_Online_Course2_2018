"""
    loads the database with full of donors to test with
"""

import login_redis

def populate_mailroom(donor_items):
    """
        mongo data manipulation
        donor_items should be a list of dictionaries of donor data
    """
    try:
        r = login_redis.login_redis_cloud()
        r.set('customer_count', 99)
        for dict in donator_data:
            r.hset(f'{dict["first_name"]} {dict["last_name"]}', 'total_donations', dict['total_donations'])
            r.hset(f'{dict["first_name"]} {dict["last_name"]}', 'average', dict['average'])
            r.hset(f'{dict["first_name"]} {dict["last_name"]}', 'first_gift', dict['first_gift'])
            r.hset(f'{dict["first_name"]} {dict["last_name"]}', 'last_gift', dict['last_gift'])
            r.hset(f'{dict["first_name"]} {dict["last_name"]}', 'transactions', dict['transactions'])
            r.hset(f'{dict["first_name"]} {dict["last_name"]}', 'email', dict['email'])
            r.hset(f'{dict["first_name"]} {dict["last_name"]}', 'phone', dict['phone'])
            r.hset(f'{dict["first_name"]} {dict["last_name"]}', 'cust_num', f"{dict['first_name'][0]}{r.incr('customer_count')}")
            r.hset(f'{dict["first_name"]} {dict["last_name"]}', r.incr('invoice'), dict['donation1'])
            r.rpush(r.hget(f'{dict["first_name"]} {dict["last_name"]}', "cust_num"), r.get('invoice'))
            r.hset(f'{dict["first_name"]} {dict["last_name"]}', r.incr('invoice'), dict['donation2'])
            r.rpush(r.hget(f'{dict["first_name"]} {dict["last_name"]}', "cust_num"), r.get('invoice'))
            
    except Exception as e:
        print(f'Redis error: {e}')

donator_data = [
    {
        'first_name': 'Andrew',
        'last_name': 'Braddock',
        'total_donations': 800,
        'average': 400,
        'first_gift': 200,
        'last_gift': 600,
        'transactions': 2,
        'email': 'abraddock@gmail.com',
        'phone': '509-777-9999',
        'cust_num': 'A100',
        'donation1': 200,
        'donation2': 600
    },
    {
        'first_name': 'Janet',
        'last_name': 'Jackson',
        'donation1': 300,
        'donation2': 500,
        'total_donations': 800,
        'average': 400,
        'first_gift': 300,
        'last_gift': 500,
        'transactions': 2,
        'email': 'jjackson@gmail.com',
        'phone': '503-334-5029',
        'cust_num': 'J100'
    },
    {
        'first_name': 'Joshua',
        'last_name': 'Hoff',
        'donation1': 100,
        'donation2': 400,
        'average': 500,
        'first_gift': 100,
        'last_gift': 500,
        'total_donations': 500,
        'transactions': 2,
        'email': 'jhoff@gmail.com',
        'phone': '222-333-5555'
    },
    {
        'first_name': 'Melanie',
        'last_name': 'Scott',
        'donation1': 400,
        'donation2': 550,
        'total_donations': 950,
        'average': 475,
        'first_gift': 400,
        'last_gift': 550,
        'transactions': 2,
        'email': 'abraddock@gmail.com',
        'phone': '604-867-5309'
    },
    {
        'first_name': 'Tatsiana',
        'last_name': 'Kisel',
        'donation1': 600,
        'donation2': 600,
        'total_donations': 1200,
        'average': 600,
        'first_gift': 600,
        'last_gift': 600,
        'transactions': 2,
        'email': 'tkisel@gmail.com',
        'phone': '509-253-3377'
    },
    ]


if __name__ == '__main__':
    populate_mailroom(donator_data)