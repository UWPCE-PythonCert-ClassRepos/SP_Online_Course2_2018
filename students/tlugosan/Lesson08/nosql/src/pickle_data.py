"""
    Data for database demonstrations
"""


def get_bakery_data():
    """
    demonstration data
    """

    bakery_data = [
        {
            'product': 'Princess Cake',
            'size': 'large',
            'serves': 10,
            'price': 30,
            'in_stock_quantity': 7
        },
        {
            'product_type': 'Croissant',
            'size': 'medium',
            'serves': 1,
            'price': 2.99,
            'in_stock_quantity': 50
        },
        {
            'product_type': 'Cinnamon Rolls',
            'size': 'medium',
            'serves': 1,
            'price': 3.99,
            'in_stock_quantity': 60
        },
        {
            'product_type': 'Chocolate Crinkle Cookie',
            'size': 'large',
            'serves': 1,
            'price': 1.5,
            'in_stock_quantity': 150
        },
        {
            'product_type': 'Eclair',
            'size': 'medium',
            'serves': 1,
            'price': 2.99,
            'in_stock_quantity': 25
        }
    ]
    return bakery_data
