"""
initial donor db dataset
"""
__author__ = "Wieslaw Pucilowski"

def get_donor_data():
    """
    returns dataset
    """
    donor_data = [
        {
            'name': {'first_name': 'Brandon', 'last_name': 'Dekinson'},
            'location': 'Bothell',
            'donations' : [10, 20, 30]
        },
        {
            'name': {'first_name': 'Susan', 'last_name': 'Vegas'},
            'location': 'New York',
            'donations' : [100, 99]
        },
        {
            'name': {'first_name': 'Abdul', 'last_name': 'Alhambra'},
            'location': 'Damascus',
            'donations' : [999]
        },
        {
            'name': {'first_name': 'Ivan', 'last_name': 'Smirnoff'},
            'location': 'Moscow',
            'donations' : [100, 200]
        },
        {
            'name': {'first_name': 'Speedy', 'last_name': 'Gonzales'},
            'location': 'Los Angeles',
            'donations' : [97, 45]
        }
    
    ]

    return donor_data