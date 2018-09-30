"""
    file to generate report from mongodb for mailroom
"""

from login_database import login_mongodb_cloud


def report():
    with login_mongodb_cloud() as client:
        db = client['dev']
        mailroom = db['mailroom']

    print('\nLast Name______Title__Total Donations__Number of Donations')
    donor_table = mailroom.find()
    for d in donor_table:
        long_tab = (15 - len(d['last_name']))*' '
        short_tab = 3*' '
        end_tab = 20*' '
        print(d['last_name'], long_tab, d['title'], short_tab, d['donations'],
              end_tab, d['num_donations'])


if __name__ == '__main__':
    report()
