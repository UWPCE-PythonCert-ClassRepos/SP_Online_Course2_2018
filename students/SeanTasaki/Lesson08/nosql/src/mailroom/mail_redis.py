


from pprint import pprint as pp
import mr_login_database
import mr_utilities
import logging
import pymongo
import sys
from ast import literal_eval
import json

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

log.info('\n\nStep 1: connect to Redis')
r = mr_login_database.login_redis_cloud()

log.info('\n\nStep 2: cache some data in Redis')

donor_data = [
        {'Name': 'Bob Dylan', 'Nickname': 'The Musician',
        'Donations': [50, 25, 100],'Email': 'theband@gmail.com'},
        {'Name': 'Filippo Berio', 'Nickname': 'The Olive Oil Guy',
        'Donations': [321, 2, 5000],'Email': 'oliveoil@gmail.com'},
        {'Name': 'Sean Tasaki', 'Nickname': 'The Philosopher',
        'Donations': [123, 45, 67],'Email': 'stasaki@gmail.com'},
        {'Name': 'Florence Feist', 'Nickname': 'The British One',
        'Donations': [50, 100],'Email': 'florence@gmail.com'}
        ]

json_data = json.dumps(donor_data)
r.set('donor_data', json_data)


def main_menu():
    
    main_menu_dict = {'1': thank_you, 
                      '2': print_list_donors,
                      '3': create_report, 
                      '4': find_email,
                      '5': find_nickname,
                      '6': delete_donor,
                      '7': display_single_donor,
                      '8': quit}
    
    main_prompt = 'Enter 1-8 from the following options:\n\
                   (1) Add A Donation from a New or Existing Donor\n\
                   (2) List All Donors\n\
                   (3) Create Report\n\
                   (4) Find Email\n\
                   (5) Find Nickname\n\
                   (6) Delete Donor\n\
                   (7) Display Information for Single Donor\n\
                   (8) Exit\n\
                   >> ' 
    main_menu_response(main_prompt, main_menu_dict)


def main_menu_response(prompt, main_menu_dict):
    while True:
        response = input(prompt)
        try:
            if main_menu_dict[response]() == "exit menu":
                r.flushdb()
                print("Database has been cleared. Have a nice day...")
                sys.exit(0)
        except KeyError:
            print("Enter a number between 1-8.")    

def quit():
    return 'exit menu'

def list_donors():
    all_donors = []
    rcrds = json.loads(r.get('donor_data'))
    for record in rcrds:
        all_donors.append(record['Name'])
    return all_donors

def print_list_donors():
    donors = list_donors()
    for donor in donors:
        print(donor)

def thank_you():
        try:
            name = donor_name_prompt()
            if name in list_donors():
                print(f'{name} is a previous donor.')
                donation = donation_prompt()
                rcrds = json.loads(r.get('donor_data'))
                for donor in rcrds:
                    if donor['Name'] == name:
                        donor['Donations'].append(donation)
                        nickname = donor['Nickname']
                r.set('donor_data', json.dumps(rcrds))
                print(f'Donation from {name} added successfuly.')

                print(thank_you_message(name, nickname, donation))
    
            else:
                print(f'{name} is a new donor!')
                nickname = donor_nickname_prompt()
                donation = donation_prompt()
                email = donor_email_prompt()
                rcrds = json.loads(r.get('donor_data'))
                rcrds.append({'Name': name,
                             'Nickname': nickname,
                             'Donations': [donation],
                             'Email': email})
                r.set('donor_data', json.dumps(rcrds))
                print(thank_you_message(name, nickname, donation))

        except ValueError:
            print("Invalid input.")
            thank_you()               
    
        
def donor_name_prompt():
    reply = input('Enter the first and last name of the donor or enter ''list'' to see a list of previous donor names or enter Q to exit to main menu\n> ')          
    if reply.lower() == 'list':
        list_donors()
        main_menu()
    elif reply.upper() == 'Q':
        main_menu()
    else:
        first, last = reply.split(' ')
        full_name = first.title() + ' ' + last.title()
        return full_name


def donor_nickname_prompt():
    return input('Enter the nickname of the donor\n>> ')

def donation_prompt():
    donation = float(input('Enter the donation amount: '))
    return donation

def donor_email_prompt():
    return input('Enter the email of the donor\n>> ')


def find_email():
    name = donor_name_prompt()
    rcrds = json.loads(r.get('donor_data'))
    for donor in rcrds:
        if donor['Name'] == name:
            email = donor['Email']
            print(f'The email for {name} is: {email}.')
            return
    else:
        print(f'{name} is not in the database. Please try again.')

def find_nickname():
    name = donor_name_prompt()
    rcrds = json.loads(r.get('donor_data'))
    for donor in rcrds:
        if donor['Name'] == name:
            nick = donor['Nickname']
            print(f'The nickname for {name} is: {nick}.')
            return
    else:
        print(f'{name} is not in the database. Please try again.')


def thank_you_message(first, nickname, donation):
        return f"Thank you {first} aka '{nickname}'' for your generous support for our charity! Your genereous donation of ${float(donation):.2f} is much appreciated."

def display_single_donor():
    name = donor_name_prompt()
    rcrds = json.loads(r.get('donor_data'))
    for donor in rcrds:
        if donor['Name'] == name:
            nick = donor['Nickname']
            donations = donor['Donations']
            email = donor['Email']
            print(f'Name: {name}\nNickname: {nick}\nDonations: {donations}\nEmail: {email}')
            return
    else:
        print(f'{name} is not in the database. Please try again.')
        
def delete_donor():
   while True:
        name = donor_name_prompt()
        rcrds = json.loads(r.get('donor_data'))
        for donor in rcrds:
            if donor['Name'] == name:
                rcrds.remove(donor)
                r.set('donor_data', json.dumps(rcrds))
                print(f'{name} successfully deleted from database.')
                return
        else:
            print(f'{name} is not in the database! Please try again.')

def create_report():
    donation_list_format = []
    rcrds = json.loads(r.get('donor_data'))
    for donor in rcrds:
        name = donor['Name']
        nick = donor['Nickname']
        total = sum(donor['Donations'])
        count = len(donor['Donations'])
        avg = total / count
        donation_list_format.append([name, total, count, avg])
    donation_list_format.sort(key=lambda l: l[1], reverse = True)
    s1 = "Donor Name          |   Total Given  |  Num Gifts |  Average Gift\n"
    s2 = "-----------------------------------------------------------------\n"
    final_string = s1 + s2
    for z in range(0, len(donation_list_format)):
        s3 = '{:20} ${:13,.2f}{:14}  ${:13,.2f}\n'.format(*donation_list_format[z])
        final_string += s3
    print(final_string)
    
        
if __name__ == '__main__':

    main_menu()

