"""
    Data for database demonstrations
"""


def get_furniture_data():
    """
    demonstration data
    """

    furniture_data = [
        {
            'product': 'Couch',
            'color': 'Red',
            'description': 'Leather low back',
            'monthly_rental_cost': 12.99,
            'in_stock_quantity': 10
        },
        {
            'product': 'Couch',
            'color': 'Blue',
            'description': 'Cloth high back',
            'monthly_rental_cost': 9.99,
            'in_stock_quantity': 3
        },
        {
            'product': 'Coffee table',
            'color': 'Brown',
            'description': 'Plastic',
            'monthly_rental_cost': 2.50,
            'in_stock_quantity': 25
        },
        {
            'product': 'Couch',
            'color': 'Red',
            'description': 'Leather high back',
            'monthly_rental_cost': 15.99,
            'in_stock_quantity': 17
        },
        {
            'product': 'Recliner',
            'color': 'Blue',
            'description': 'Leather high back',
            'monthly_rental_cost': 19.99,
            'in_stock_quantity': 6
        },
        {
            'product': 'Chair',
            'color': 'Green',
            'description': 'Plastic',
            'monthly_rental_cost': 1.00,
            'in_stock_quantity': 45
        },
        {
            'product': 'Couch',
            'color': 'Green',
            'description': 'Nice and cheap',
            'monthly_rental_cost': 0.01,
            'in_stock_quantity': 0
        },
        {
            'product': 'Couch',
            'color': 'Black',
            'description': 'Expensive, but very nice',
            'monthly_rental_cost': 9999.99,
            'in_stock_quantity': 42
        },
        {
            'product': 'Paper weight',
            'color': 'Red',
            'description': 'Desk accessory, very beautiful',
            'monthly_rental_cost': 75.00,
            'in_stock_quantity': 100
        },
    ]
    return furniture_data


def print_furniture_item(doc):
    print(f" Product: {doc['product']},"
          f" Color: {doc['color']},"
          f" Description: {doc['description']},"
          f" Cost: {doc['monthly_rental_cost']},"
          f" Stock: {doc['in_stock_quantity']}")
