"""
    Mailroom utilizing a database
"""
import sys
import logging
import login_mongodb

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Donorhandle:
    def __init__(self, query, temp = None):
        if temp != None:
            donor_data.update_one(
            {'first_name': query['first_name'], 'last_name': query['last_name']},
            {'$set':{'donations': temp}}
            )

        self.query = donor_data.find_one({'first_name': query['first_name'], 'last_name': query['last_name']})

    @property
    def gifts(self):
        query = donor_data.find_one({'first_name': self.query['first_name'], 'last_name': self.query['last_name']})
        donor_data.update_one(
        {'first_name': query['first_name'], 'last_name': query['last_name']},
        {'$set':{'transactions': (len(query['donations']))}}
        )
        query = donor_data.find_one({'first_name': self.query['first_name'], 'last_name': self.query['last_name']})
        return query['transactions']

    @property
    def total_donations(self):
        query = donor_data.find_one({'first_name': self.query['first_name'], 'last_name': self.query['last_name']})
        donor_data.update_one(
        {'first_name': query['first_name'], 'last_name': query['last_name']},
        {'$set':{'total_donations': sum(query['donations'])}}
        )
        query = donor_data.find_one({'first_name': self.query['first_name'], 'last_name': self.query['last_name']})
        return query['total_donations']

    @property
    def average(self):
        query = donor_data.find_one({'first_name': self.query['first_name'], 'last_name': self.query['last_name']})
        try:
            donor_data.update_one(
            {'first_name': query['first_name'], 'last_name': query['last_name']},
            {'$set':{'average': (sum(query['donations']) / query['transactions'])}}
            )
        #removes a donor if the last donation of a donor is deleted
        except ZeroDivisionError:
            donor_data.update_one(
            {'first_name': query['first_name'], 'last_name': query['last_name']},
            {'$set':{'average': 0}}
            )
        query = donor_data.find_one({'first_name': self.query['first_name'], 'last_name': self.query['last_name']})
        return query['average']

    @property
    def first_gift(self):
        query = donor_data.find_one({'first_name': self.query['first_name'], 'last_name': self.query['last_name']})
        temp = []
        for dono in query['donations']:
            temp.append(dono)
        donor_data.update_one(
            {'first_name': query['first_name'], 'last_name': query['last_name']},
            {'$set':{'first_gift': temp[0]}}
            )
        query = donor_data.find_one({'first_name': self.query['first_name'], 'last_name': self.query['last_name']})
        return query['first_gift']

    @property
    def last_gift(self):
        query = donor_data.find_one({'first_name': self.query['first_name'], 'last_name': self.query['last_name']})
        temp = []
        for dono in query['donations']:
            temp.append(dono)
        donor_data.update_one(
            {'first_name': query['first_name'], 'last_name': query['last_name']},
            {'$set':{'last_gift': temp[-1]}}
            )
        query = donor_data.find_one({'first_name': self.query['first_name'], 'last_name': self.query['last_name']})
        return query['last_gift']

def set_variables(query, temp = None):
    if not temp:
        donor_data.delete_one( {'first_name': query['first_name'], 'last_name': query['last_name']})
        return
    setting = Donorhandle(query, temp)
    setting.gifts
    setting.total_donations
    setting.average
    setting.first_gift
    setting.last_gift

def new_donor(first_name, last_name, donation):
    email = input('What is the email?: ')
    phone = input('What is the phone number?: ')
    donor_data.insert_one({'first_name': first_name,
        'last_name': last_name,
        'donations': [donation],
        'total_donations': donation,
        'average': donation,
        'first_gift': donation,
        'last_gift': donation,
        'transactions': 1,
        'email': email,
        'phone': phone
        })

def existing_donor(first_name, last_name, donation):
    donor_data.update_one(
    {'first_name': first_name, 'last_name': last_name},
    {'$push':{'donations': donation}, '$set':{'last_gift': donation}}
    )
    return

def show_list():
    cursor = donor_data.find()
    for doc in cursor:
        print(f'{doc["first_name"]}')
    return

def report():
    cursor = donor_data.find()
    for doc in cursor:
        print(f'{doc["first_name"]} {doc["last_name"]}')
        print(f'   Donations:')
        for dono in doc['donations']:
            print(f'      {dono:.2f}')
        print(f'   Total Donos - {doc["total_donations"]:.2f}')
        print(f'   Average - {doc["average"]:.2f}')
        print(f'   First Gift - {doc["first_gift"]:.2f}')
        print(f'   Last Gift - {doc["last_gift"]:.2f}')
        print(f'   Transactions - {doc["transactions"]}')
        try:
            print(f'   Email - {doc["email"]}')
            print(f'   Phone # - {doc["phone"]}')
        except KeyError:
            continue

def letters():
    tab = '    '
    cursor = donor_data.find()
    for doc in cursor:
        with open(f'{doc["first_name"]} {doc["last_name"]}.txt', 'w') as outfile:                
            donation = doc["total_donations"]
            val = doc["last_gift"]
            outfile.write(f'Dear {doc["first_name"]} {doc["last_name"]}, \n\n{tab}Thank you very much for your most recent donation \
of ${val:.2f}! \n\n{tab}You have now donated a total of ${donation:.2f}. \n\n{tab}Your support \
is essential to our success and will be well utilized. \n\n{tab*2}Sincerely, \n{tab*3}-The Company')

def show_donations():
    show_list()
    while True:
        choice = input(f'Whose donations do you want to see?: ')
        if choice == 'quit':
            return
        cursor = donor_data.find()
        for doc in cursor:
            if choice == doc["first_name"]:
                query = donor_data.find_one({'first_name': choice})
                print(f'\n{choice}')
                for item in query['donations']:
                    print(f'{item}')
                return
        print('\nDonator does not exist.\n')
        continue

def delete():
    show_list()
    while True:
        first_name = input(f'Which donor would you like to edit?: ')
        if first_name == 'quit':
            return
        cursor = donor_data.find()
        for doc in cursor:
            if first_name == doc['first_name']:
                query = donor_data.find_one({'first_name': first_name})
                temp = []
                for ind in query['donations']:
                    print(f'{query["donations"].index(ind)+1}: {ind}')
                    temp.append(ind)
                number = int(input(f'Which donation would you like to delete?: ')) - 1
                if number == 'quit':
                    return
                del temp[number]
                set_variables(query, temp)                
                return
        print('\nDonator does not exist.\n')
        continue

def edit():
    show_list()
    while True:
        first_name = input(f'Which donor would you like to edit?: ')
        if first_name == 'quit':
            return
        cursor = donor_data.find()
        for doc in cursor:
            if first_name == doc['first_name']:
                query = donor_data.find_one({'first_name': first_name})
                temp = []
                for ind in query['donations']:
                    print(f'{query["donations"].index(ind)+1}: {ind}')
                    temp.append(ind)
                while True:
                    number = int(input(f'Which donation would you like to edit?: ')) - 1
                    if number == 'quit':
                        return
                    break
                while True:
                    replace = input(f'What is the correct donation amount?: ')
                    if replace == 'quit':
                        return
                    try:
                        float(replace)
                    except ValueError:
                        print('\nPlease give a number instead.\n')
                        continue
                    temp[number] = float(replace)
                    set_variables(query, temp)
                    return
        print('\nPlease type a name from the list.\n')
        continue

def thank_you():
    while True:
        first_name = input('\nWhat is the first name of the donor?: ')
        if first_name == 'list':
            show_list()
            continue
        elif first_name == 'quit':
            return
        last_name = input('\nWhat is the last name of the donor?: ')
        while True:
            try:
                donation = float(input('\nWhat is the donation amount?: '))
            except ValueError:
                print('\nPlease give a number instead.\n')
                continue
            break
        cursor = donor_data.find()
        for doc in cursor:
            if first_name == doc['first_name'] and last_name == doc['last_name']:
                print('Existing donor - adding donation to database')
                #come back here
                existing_donor(first_name, last_name, donation)
                query = donor_data.find_one({'first_name': first_name})
                set_variables(query)
                return
        print('New donor - adding donor to database')
        new_donor(first_name, last_name, donation)
        return

def quitting():
    """
    quits the program
    """
    sys.exit()

def continuing():
    """
    continues the program
    """
    print('Try Again.\n')

switch_func_dict = {
    '1':thank_you,
    '2':edit,
    '3':delete,
    '4':report,
    '5':letters,
    '6':show_donations,
    '7':quitting,
    'quit':quitting,
    'list':show_list
    }

if __name__ == '__main__':
    with login_mongodb.login_mongodb_cloud() as client:
        db = client['dev']
        donor_data = db['donor_data']
        while True:
            choice = input(f'\n1: Add Donation' +\
            f'\n2: Edit Donation' +\
            f'\n3: Delete Donation' +\
            f'\n4: Create a Report' +\
            f'\n5: Send Letters to Everyone' +\
            f'\n6: Show Donations' +\
            f'\n7: Quit' +\
            f'\n\nChoose an Option: '
            )
            c = switch_func_dict.get(choice, continuing)()