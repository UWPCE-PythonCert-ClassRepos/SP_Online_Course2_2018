"""
    loads the database with full of donors to test with
"""

import login_mongodb

def populate_mailroom(donor_items):
    """
        mongo data manipulation
        donor_items should be a list of dictionaries of donor data
    """

    with login_mongodb.login_mongodb_cloud() as client:
        db = client['dev']
        donor_data = db['donor_data']
        donor_data.insert_many(donor_items)
        
donator_data = [
    {
        'first_name': 'Andrew',
        'last_name': 'Braddock',
        'donations': [200, 600],
        'total_donations': 800,
        'average': 400,
        'first_gift': 200,
        'last_gift': 600,
        'transactions': 2,
        'email': 'abraddock@gmail.com',
        'phone': '509-777-9999'
    },
    {
        'first_name': 'Janet',
        'last_name': 'Jackson',
        'donations': [300],
        'total_donations': 300,
        'average': 300,
        'first_gift': 300,
        'last_gift': 300,
        'transactions': 1,
        'email': 'jjackson@gmail.com',
        'phone': '503-334-5029'
    },
    {
        'first_name': 'Joshua',
        'last_name': 'Hoff',
        'donations': [500],
        'average': 500,
        'first_gift': 500,
        'last_gift': 500,
        'total_donations': 500,
        'transactions': 1,
        'email': 'jhoff@gmail.com',
        'phone': '222-333-5555'
    },
    {
        'first_name': 'Melanie',
        'last_name': 'Scott',
        'donations': [400, 550],
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
        'donations': [200, 400, 600],
        'total_donations': 1200,
        'average': 400,
        'first_gift': 200,
        'last_gift': 600,
        'transactions': 3,
        'email': 'tkisel@gmail.com',
        'phone': '509-253-3377'
    },
    ]

if __name__ == '__main__':
    populate_mailroom(donator_data)