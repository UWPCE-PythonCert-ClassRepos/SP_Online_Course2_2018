"""
    Data for database demonstrations
"""


def assignment_furniture_data():
    """
    part 1 data
    """

    furtniture_data = [
        {
            'product type': 'couch',
            'product color': 'red',
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10
        },
        {
            'product type': 'couch',
            'product color': 'red',
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3
        },
        {
            'product type': 'coffee table',
            'product color': 'black',
            'description': 'Wooden table',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25
        },
        {
            'product type': 'chair',
            'product color': 'straw',
            'description': 'Straw chair',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17
        }
    ]

    return furtniture_data

def get_football_data():
    """ New data for serialization. """
    players_by_year = [
        {
            'year': '2018',
            'qb': 'Jake Fromm',
            'rb': 'DeAndre Swift',
            'wr': 'Riley Ridley',
        },
        {
            'year': '2017',
            'qb': 'Jake Fromm',
            'rb': 'Nick Chubb',
            'wr': 'N/A'
        },
        {
            'year': '2016',
            'qb': 'Jacob Eason',
            'rb': 'Sony Michel',
            'wr': 'Isaiah McKenzie'
        }
    ]

    return players_by_year