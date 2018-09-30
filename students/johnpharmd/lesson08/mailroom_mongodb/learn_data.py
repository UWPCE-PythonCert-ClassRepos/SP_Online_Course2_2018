"""
    Data for database demonstrations
"""


def get_mailroom_data():
    """
        makes JSON object from mailroom donors_list, stores in txt file
    """

    donors_list = [
       {
            'last_name': 'Gates', 'title': 'Mr.', 'donations': 150000,
            'num_donations': 3
       },
       {
            'last_name': 'Brin', 'title': 'Mr.', 'donations': 150000,
            'num_donations': 3
       },
       {
            'last_name': 'Cerf', 'title': 'Mr.', 'donations': 50000,
            'num_donations': 2
       },
       {
            'last_name': 'Musk', 'title': 'Mr.', 'donations': 100000,
            'num_donations': 1
       },
       {
            'last_name': 'Berners-Lee', 'title': 'Mr.',
            'donations': 50000, 'num_donations': 2
       },
       {
            'last_name': 'Wojcicki', 'title': 'Ms.',
            'donations': 125000, 'num_donations': 1
       },
       {
            'last_name': 'Avey', 'title': 'Ms.', 'donations': 200000,
            'num_donations': 2
       }
    ]
    return donors_list


def get_baseball_data():
    """
        AL standings selected data
    """

    baseball_data = [
        {
            'team_name': 'Boston', 'wins': 103, 'losses': 47,
            'wins_in_last_ten': 7, 'streak': 'W2'
        },
        {
            'team_name': 'NY Yankees', 'wins': 91, 'losses': 58,
            'wins_in_last_ten': 4, 'streak': 'L2'
        },
        {
            'team_name': 'Tampa Bay', 'wins': 83, 'losses': 66,
            'wins_in_last_ten': 8, 'streak': 'W3'
        },
        {
            'team_name': 'Toronto', 'wins': 68, 'losses': 82,
            'wins_in_last_ten': 5, 'streak': 'W3'
        },
        {
            'team_name': 'Baltimore', 'wins': 43, 'losses': 107,
            'wins_in_last_ten': 2, 'streak': 'L1'
        },
        {
            'team_name': 'Cleveland', 'wins': 83, 'losses': 66,
            'wins_in_last_ten': 4, 'streak': 'L1'
        },
        {
            'team_name': 'Minnesota', 'wins': 69, 'losses': 81,
            'wins_in_last_ten': 5, 'streak': 'W2'
        },
        {
            'team_name': 'Detroit', 'wins': 61, 'losses': 89,
            'wins_in_last_ten': 4, 'streak': 'L1'
        },
        {
            'team_name': 'Chi White Sox', 'wins': 59, 'losses': 90,
            'wins_in_last_ten': 3, 'streak': 'L1'
        },
        {
            'team_name': 'Kansas City', 'wins': 52, 'losses': 98,
            'wins_in_last_ten': 6, 'streak': 'L2'
        },
        {
            'team_name': 'Houston', 'wins': 94, 'losses': 56,
            'wins_in_last_ten': 7, 'streak': 'L1'
        },
        {
            'team_name': 'Oakland', 'wins': 90, 'losses': 60,
            'wins_in_last_ten': 7, 'streak': 'L2'
        },
        {
            'team_name': 'Seattle', 'wins': 83, 'losses': 67,
            'wins_in_last_ten': 5, 'streak': 'W1'
        },
        {
            'team_name': 'LA Angels', 'wins': 74, 'losses': 76,
            'wins_in_last_ten': 6, 'streak': 'W1'
        },
        {
            'team_name': 'Texas', 'wins': 64, 'losses': 86,
            'wins_in_last_ten': 3, 'streak': 'L2'
        }
    ]
    return baseball_data


def get_furniture_data():
    """
    demonstration data
    """

    furniture_data = [
        {
            'product': 'Red couch',
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10
        },
        {
            'product': 'Blue couch',
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3
        },
        {
            'product': 'Coffee table',
            'description': 'Plastic',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25
        },
        {
            'product': 'Red couch',
            'description': 'Leather high back',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17
        },
        {
            'product': 'Blue recliner',
            'description': 'Leather high back',
            'monthly_rental_cost': 19.99,
            'in_stock_quantity': 6
        },
        {
            'product': 'Chair',
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 45
        }
    ]
    return furniture_data
