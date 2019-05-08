import donors_sql as d
from create_mr_tables import *


connect = d.Individual('mailroom.db')
#connect.add_donation('Shane', 6)
#connect.add_donation('TED', 5)
#connect.add_donation('JERRY', 7)
#database.close
#connect_group = d.Group('mailroom.db')
#connect_group.print_donors()
#print('Testing Group.search for know entry')
#print(connect_group.search('Shane'))
#print('Testing Group.search for missing entry')
#print(connect_group.search('Zach'))
#print(connect.number_donations('Shane'))
#print(connect.sum_donations('Shane'))
#print(connect.avg_donations('Shane'))
#database.close()
#connect.add_donation('Shane', 99)
#connect.add_donation('Shane', 1)
#print(connect.last_donation('Shane'))
#database.close()
#print(connect_group.summary())








# After deleting Shane in mailroom_sql, see if all donations are deleted.
database.connect(reuse_if_open=True)
logger.info('Connected to database')
database.execute_sql('PRAGMA foreign_keys = ON;')

with database.transaction():
    logger.info('Checking database for entries by Shane after delete')
    query = Donations.select().where(Donations.donor_name == 'Shane')
    donation_list = []  # Create a list of donations for 'name'.
    for result in query:
        # logger.info(f'{result.donor_name}')
        donation_list.append(int(result.donation))
    print(donation_list)
