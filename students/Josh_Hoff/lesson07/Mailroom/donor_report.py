"""
    Donor report pulling data from the database
"""

from create_mailroom import *

if __name__ == '__main__':
    donorq = (Donor.select().order_by(Donor.donor_name)).prefetch(Donation)
    for i in donorq:
        print(i.donor_name)
        for x in i.name_person:
            print(f'  Invoice: {x.dono_number} : ${x.dono}')
        print(f'  Total Donations: ${i.donations}')
        for x in i.person_name:
            print(f'   Transactions - {x.transactions}')
            print(f'   Average Donation - ${x.average:.2f}')
            print(f'   First Donation - ${x.first_gift}')
            print(f'   Latest Donation - ${x.last_gift}')