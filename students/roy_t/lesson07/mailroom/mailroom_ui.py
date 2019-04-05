#!/usr/bin/env python3

"""
The front end of the mailroom application. Presents the main menu selections and takes requested actions by interacting with the Donor database.
"""


import mailroom_model as mm
import mailroom_backend as mb


def send_thank_you(donor_db):
    """
    Send a thank you to a specified donor.
    :param donor_db: the Donor database
    :return: thank you letter
    """
    name_queries = ('First name', 'Last name')
    full_name = list()
    count = 0
    while count < len(name_queries):
        print("Enter {}, 'list' for names in the donor database. Type 'b' to go back".format(
            name_queries[count]))
        name = input('> ')
        if name == 'b':
            return ''
        elif name.lower() == 'list':
            for donor in donor_db.get_donors():
                print(donor.get_name())
        else:
            full_name.append(name)
            count += 1
    amount = ''
    while not amount.isnumeric():
        print("Enter donation amount:\n(Type 'b' to go to Main Menu)")
        amount = input('$')
        if amount == 'b':
            return
    amount = float(amount)
    return mb.send_thank_you(donor_db, full_name[0], full_name[1], amount)


def send_letters(donor_db):
    """
    Create letters for all donors in the database and save each letter to file.
    :param donor_db: the database of donors
    :return: string
    """
    try:
        with open('template_thank_you.txt', 'r') as file:
            donor_letter = file.read()
    except FileNotFoundError as e:
        print('Error reading template:' + str(e))
        return 'Failed'

    donor_amount_tuple = mb.send_letters(donor_db, donor_letter)

    for tup in donor_amount_tuple:
        name = tup[0]
        amount = tup[1]
        filename = f'{name}.txt'.replace(' ', '_')
        with open(filename, 'w+') as file:
            individual_letter = donor_letter.format(name=name, amount=amount)
            file.write(individual_letter)
    return 'Created {} letters.'.format(len(donor_amount_tuple))


def find_donor(donor_db):
    """
    Find the donor and return their information.
    :param donor_db: the Donor database.
    :return: string of donor info
    """
    donor_names = dict()
    count = 1
    for donor in donor_db.get_donors():
        donor_names[str(count)] = donor.get_name_tuple()
        count += 1
    print("Select a donor by number or 'b' to go back")
    for k, v in donor_names.items():
        print(f'{k} {v[0]} {v[1]}')
    selection = input('> ')
    status = None
    if selection in donor_names:
        status = donor_names[selection]
    return status


def delete_donor(donor_db):
    """
    Delete a donor and all associated records from the database.
    :param donor_db: the Donor database
    :return: status - a string 
    """
    donor = find_donor(donor_db)
    status = 'No donors deleted.'
    if donor is not None:
        donor_db.delete_donor(donor[0], donor[1])
        status = "Deleted donor {0} {1}".format(*donor)
    return status


def modify_donor_info(donor_db):
    """
    Modify donor information
    :param donor_db: the Donor database
    :return: status (string)
    """
    donor = find_donor(donor_db)
    status = 'No changes made.'
    if donor is not None:
        first_name = input('Enter new first name: ')
        last_name = input('Enter new last name: ')
        if first_name is not None and last_name is not None:
            donor_db.modify_donor_name(donor[0], donor[1], first_name, last_name)
            status = f'Donor name changed: {first_name} {last_name}'
    return status


def modify_donation(donor_db):
    """
    Modify a donation.
    :param donor_db: the Donor database
    :return:
    """
    donor = find_donor(donor_db)
    print('Enter the number to change: ')
    donor_data = dict()
    count = 1
    for donation in donor_db.get_donations(donor[0], donor[1]):
        donor_data[str(count)] = f'Donation. {donation}'
        count += 1
    for k, v in donor_data.items():
        print(f'{k}: {v}')
    selection = input('Enter donation to change: ')
    if selection in donor_data:
        amount = input('Enter new donation value: ')
        donor_db.modify_donation(donor[0], donor[1], int(selection) - 1, float(amount))


def delete_donation(donor_db):
    """
    Delete a donation from donor.
    :param donor_db: the donor database
    :return: status string
    """
    donor = find_donor(donor_db)
    print('Select a donation to change, by number.')
    donor_data = dict()
    count = 1
    for donation in donor_db.get_donations(donor[0], donor[1]):
        donor_data[str(count)] = f'Donation. {donation}'
        count += 1
    for k, v in donor_data.items():
        print(f'{k}: {v}')
    status = 'Donations were not deleted.'
    selection = input('Enter the donation to delete: ')
    if selection in donor_data:
        donor_db.delete_donation(donor[0], donor[1], int(selection) - 1)
        status = 'Deleted ' + donor_data[selection]
    return status

menu_selections = [
    'Enter the number of the action to take:',
    '1 - Send individual thank you',
    '2 - Create Donor Report',
    '3 - Send letters to all donors.',
    '4 - Modify a donor',
    '5 - Delete a donor',
    '6 - Modify a donor donation',
    '7 - Delete a donor donation',
    'q - Quit'
]


main_menu_actions = {
    '1': send_thank_you,
    '2': mb.create_report,
    '3': send_letters,
    '4': modify_donor_info,
    '5': delete_donor,
    '6': modify_donation,
    '7': delete_donation
}


def main_menu():
    print('\n'.join(menu_selections))


def get_main_menu_input():
    """Get input from user."""
    user_input = input('> ')
    user_input = user_input.lower().strip()
    return user_input


if __name__ == '__main__':
    donor_db = mm.DonorCollection()

    # Default donor data
    donor_db.add_donation('Bobby', 'Jones', 350.22)
    donor_db.add_donation('Willie', 'Wonka', 98.20)
    donor_db.add_donation('Fred', 'Hammerman', 1000)
    donor_db.add_donation('Frank', 'Furt', 250.00)
    donor_db.add_donation('Bubba', 'Gump', 1200.00)

    is_running = True
    while is_running:
        main_menu()
        user_input = get_main_menu_input()
        if user_input in main_menu_actions.keys():
            print(main_menu_actions[user_input](donor_db), '\n')
        if user_input.lower() == 'q':
            break
