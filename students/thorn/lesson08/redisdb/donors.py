"""
Sample donors
"""

def get_donors():

    thomas = 'Thomas', {'donations': '500', 'email': 'thomas@thomas.com', 'city': 'Athens', 'state': 'GA', 'zip': '30606'}

    ted =    'Ted', {'donations': '1', 'email': 'ted@ted.com', 'city': 'Memphis', 'state': 'TN', 'zip': '38104'}

    bailey = "Bailey", {'donations': '1000', 'email': 'bailey@bailey.com', 'city': 'Washington', 'state': 'DC', 'zip': '12345'}

    return thomas, ted, bailey

if __name__ == "__main__":
    donors = get_donors()

    for item in donors:
        print(item)