"""
    Data for database demonstrations
"""


def get_furniture_data():
    """
    Lesson 8 Part 1, seperate the product field into two fields, one
    called 'product type' and one called 'color'. Added two extra
    furniture items as well.
    """

    furniture_data = [
        {
            'product_type': 'couch',
            'color': 'Red',
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10
        },
        {
            'product_type': 'couch',
            'color': 'Blue',
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3
        },
        {
            'product_type': 'Coffee table',
            'color': 'black',
            'description': 'Plastic',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25
        },
        {
            'product_type': 'couch',
            'color': 'Red',
            'description': 'Leather high back',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17
        },
        {
            'product_type': 'recliner',
            'color': 'Blue',
            'description': 'Leather high back',
            'monthly_rental_cost': 19.99,
            'in_stock_quantity': 6
        },
        {
            'product_type': 'Chair',
            'color': 'Blue',
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 45
        },
        {
            'product_type': 'Chair',
            'color': 'Red',
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 15
        },
        {
            'product_type': 'Chair',
            'color': 'Green',
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 60
        }
    ]
    return furniture_data
