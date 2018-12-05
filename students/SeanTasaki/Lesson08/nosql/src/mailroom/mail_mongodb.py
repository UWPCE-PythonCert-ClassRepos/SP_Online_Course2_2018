
from pprint import pprint as pp
import mr_login_database
import mr_utilities
import logging
import pymongo
import sys


logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

def populate_donors():

    donor_data = [     
        {'name': {'first_name': 'Bob', 'last_name': 'Dylan'},
            'donation': 5},
            
        {
            'name': {'first_name': 'Italo', 'last_name': 'Calvino'},
            'donation': 500},
        {
            'name': {'first_name': 'Florence', 'last_name': 'Feist'},
            'donation': 2400},
        {
            'name': {'first_name': 'Filippo', 'last_name': 'Berio'},
            'donation': 300},
        {
            'name': {'first_name': 'Wim', 'last_name': 'Wenders'},
            'donation': 1000},     
    ]
    return donor_data

with mr_login_database.login_mongodb_cloud() as client:
    log.info('\n\nStep 1: We are going to use a database called donors')
    log.info('\n\nBut if it doesnt exist mongodb creates it')
    db = client['donors']

    log.info('\n\nAnd in that database use a collection called Donor')
    log.info('\n\nIf it doesnt exist mongodb creates it')

    donor = db['donor']

    log.info('\n\nClear collection if data already exists')
    donor.delete_many({})

    log.info('Insert an item into the document')
    new_donor = {'name': {'first_name': 'Sean', 'last_name': 'Tasaki'},
                 'donation': 555.55}

    donor.insert_one(new_donor)

    log.info('\n\nStep 2: Now we add data from the dictionary above')
    donor_items = populate_donors()
    donor.insert_many(donor_items)

    log.info("Show the collections in the DB.")
    print(db.list_collection_names())

def main_menu():
    
    main_menu_dict = {'1': thank_you, 
                      '2': create_report, 
                      '3': thank_you_to_all_donors,
                      '4': delete_donor,
                      '5': quit}
    
    main_prompt = 'Enter 1-5 from the following options:\n\
                   (1) Add A Donation from a New or Existing Donor\n\
                   (2) Create a Report\n\
                   (3) Send thank you note to all donors\n\
                   (4) Delete Donor\n\
                   (5) Exit\n\
                   >> ' 
    main_menu_response(main_prompt, main_menu_dict)


def main_menu_response(prompt, main_menu_dict):
    while True:
        response = input(prompt)
        try:
            if main_menu_dict[response]() == "exit menu":
                client.close()
                sys.exit(0)
        except KeyError:
            print("Enter a number between 1-5.")    

def quit():
    return 'exit menu'

def thank_you():
        try:
            name = donor_name_prompt()

            if name.lower() == 'list':
                donor_names = set()
                for i in donor.find():
                    name = ' '.join([i['name']['first_name'],
                                     i['name']['last_name']])
                    donor_names.add(name)
                for i in donor_names:
                    print(i)
            elif name.upper() == 'Q':
                main_menu()

            first, last = name.split(' ')
        except ValueError:
            print("Invalid input.")
            thank_you()               
            
        donation = donation_prompt()

        new_donor = {'name': {'first_name': first.title(),
                     'last_name': last.title()},
                     'donation': donation}
        donor.insert_one(new_donor)
        print(thank_you_message(first.title(), last.title(), donation))

def donor_name_prompt():
    return input('Enter the first and last name of the donor or enter ''list'' to see a list of previous donor names or enter Q to exit to main menu\n> ')          

def donation_prompt():
    donation = float(input('Enter the donation amount: '))
    return donation

def thank_you_to_all_donors():

    template = 'Dear {},\n\nThank you for your loyal support for our charity! Your {} donations have totaled \
                ${}. The money will be put to good use.\n\nSincerely,\n\t\t-The Team'

    result = donor.aggregate(
        [{'$group': {'_id': {'name': '$name'},
          'sum': {'$sum': '$donation'}, 'count': {'$sum': 1},
          'avg': {'$avg': '$donation'}}}, {'$sort': {'sum': -1}}])

    for i in result:
        i_name = ' '.join([i['_id']['name']['first_name'],
                           i['_id']['name']['last_name']])
        i_sum = i['sum']
        i_count = i['count']
        i_avg = i['avg']
        with open('{}.txt'.format(i_name.title().replace(' ',
                  '_')), 'w') as f:
            f.write(template.format(i_name, i_count, i_sum))
    print('Thank you letters have been generated successfully.')     

def thank_you_message(first, last, donation):
        return f"Thank you {first} {last} for your generous support for our charity! Your genereous donation of ${float(donation):.2f} is much appreciated."

def create_report():
    print('\n{:<20} {:>20} {:>20} {:>20}'.format('Donor Name',
          '| Total Given', '| Num Gifts', '| Average Gift'))
    print('{}'.format('-' * 83))

    result = donor.aggregate([{'$group': {'_id': {'name': '$name'},
                                  'sum': {'$sum': '$donation'},
                                  'count': {'$sum': 1}}},                               
                                  {'$sort': {'sum': -1}}])

    for i in result:
        i_name = ' '.join([i['_id']['name']['first_name'],
                           i['_id']['name']['last_name']])
        i_sum = i['sum']
        i_count = i['count']
        i_avg = i['sum'] / i['count']
        print('{:<20} {:>20.02f} {:>20} {:>20.02f}'.format(i_name,
                                                           i_sum, i_count,
                                                           i_avg))
def delete_donor():
   while True:
        reply = input("Enter first and last name of the donor you would like to remove or enter 'Q' to return to main menu\n>> ")
        if reply.upper() == 'Q':
            main_menu()
        try:
            first, last = reply.split(' ')
        except ValueError:
            print("Invalid input. Must enter a first and last name only.")
            continue

        del_donor = {'name': {'first_name': first.title(),
                     'last_name': last.title()}}
        check_donor = donor.count_documents(del_donor) > 0
        if check_donor:
            donor.delete_many(del_donor)
            print(f'{first.title()} {last.title()} has been successfully removed from the database.')
            return
        else:
            print("Donor not found! Please try again.")
        
if __name__ == '__main__':

    main_menu()
