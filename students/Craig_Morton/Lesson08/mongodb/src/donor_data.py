"""
    Data for database demonstrations
"""


def get_donor_data():
    """
    demonstration data
    """

    donor_data = [
        {'full_name': 'Bill Gates',
            'donation_count': 7,
            'total_donation': 3000.00,
            'donations': [200.00, 400.00, 600.00, 800.00, 1000.00]},
        {'full_name': 'Jeff Bezos',
            'donation_count': 6,
            'total_donation': 4400.00,
            'donations': [500.00, 500.00, 500.00, 500.0, 500.00, 1900.00]},
        {'full_name': 'Elon Musk',
            'donation_count': 2,
            'total_donation': 3900.00,
            'donations': [2100.00, 1800.00]},
        {'full_name': 'Nikola Tesla',
            'donation_count': 4,
            'total_donation': 10000.00,
            'donations': [3000.00, 2000.00, 1000.00, 4000.00]}
    ]
    return donor_data
