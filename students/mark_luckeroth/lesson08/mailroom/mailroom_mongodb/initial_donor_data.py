"""
    Data for database initialization
"""


def get_donor_data():
    """
    demonstration data
    """

    donor_data = [
        {
            'name': 'Peter Pan',
            'amount': [10., 10., 10., 10.]
        },
        {
            'name': 'Paul Hollywood',
            'amount': [5., 5000., 5., 5.]
        },
        {
            'name': 'Mary Berry',
            'amount': [100.]
        },
        {
            'name': 'Jake Turtle',
            'amount': [123., 456., 789.]
        },
        {
            'name': 'Raja Koduri',
            'amount': [60., 60000.]
        }
    ]
    return donor_data