"""
    Data for database demonstrations
"""


def create_product(p_type, colour, desc, cost, stock):
    return {
            'product_type': p_type,
            'color': colour,
            'description': desc,
            'monthly_rental_cost': cost,
            'in_stock_quantity': stock
    }


def get_furniture_data():
    """
    demonstration data
    """

    furniture_data = [
        create_product('Couch', 'Red', 'Leather low back', 12.99, 10),
        create_product('Couch', 'Blue', 'Cloth high back', 9.99, 3),
        create_product('Coffee Table', 'Brown', 'Plastic', 2.50, 25),
        create_product('Couch', 'Red', 'Leather high back', 15.99, 17),
        create_product('Recliner', 'Blue', 'Leather high back', 19.99, 6),
        create_product('Chair', 'Blue', 'Plastic', 1.00, 45),
        create_product('Chair', 'Red', 'Rubber', 20.00, 2),
        create_product('Recliner', 'Red', 'Leather high back', 89.99, 89),
        create_product('Couch', 'Red', 'Cloth high back', 19.99, 3),
        create_product('Couch', 'Red', 'Cloth low back', 746.99, 6),
        create_product('Couch', 'Red', 'Plastic', 345.54, 99)
    ]
    return furniture_data
