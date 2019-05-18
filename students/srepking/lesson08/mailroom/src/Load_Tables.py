def get_people_data():
    """
    Create some people for the mailroom MongoDB database.
    """

    people_data = [
        {
            'donor': 'Shane',
            'donations': [6, 5, 10],
        },
        {
            'donor': 'Pete',
            'donations': [7,8],
        },
        {
            'donor': 'Zach',
            'donations': [10],
        },
        {
            'donor': 'Fitz',
            'donations': [1],
        },
        {
            'donor': 'Joe',
            'donations': [5, 4, 3, 2, 1],
        }

    ]
    return people_data
