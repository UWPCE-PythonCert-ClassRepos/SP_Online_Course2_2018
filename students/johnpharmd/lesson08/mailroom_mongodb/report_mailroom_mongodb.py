"""
    file to generate report from mongodb for mailroom
"""

from login_database import login_mongodb_cloud


def report():
    with login_mongodb_cloud() as client:
        db = client['dev']
        mailroom = db['mailroom']
    
    print('Last Name____Title__Total Donations__Number of Donations')
    donor_table = mailroom.find()
    for d in donor_table:
        print(d['last_name'], 10 * ' ', d['title'], d['donations'], d['num_donations'])


if __name__ == '__main__':
    report()
