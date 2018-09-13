"""
    Data for database demonstrations
"""


def assignment_furniture_data():
    """
    part 1 data
    """

    furtniture_data = [
        {
            'product': {
                'type': 'couch',
                'color': 'red',
            },
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10
        },
        {
            'product': {
                'type': 'couch',
                'color': 'blue',
            },
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3
        },
        {
            'product': {
                'type': 'coffee table',
                'color': 'black',
            },
            'description': 'Wooden table',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25
        },
        {
            'product': {
                'type': 'chair',
                'color': 'straw',
            },
            'description': 'Straw chair',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17
        }
    ]

    return furtniture_data


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
