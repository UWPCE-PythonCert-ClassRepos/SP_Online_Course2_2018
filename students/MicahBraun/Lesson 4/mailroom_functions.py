# ----------------------------------------------------------------------------------------------------------------------
# AUTHOR: Micah Braun
# PROJECT NAME: run_mailroom.py
# DATE CREATED: 11/4/2018
# UPDATED: 11/7/2018
# PURPOSE: Lesson 04
# DESCRIPTION: The assignment allows the mailroom program to extend
# its function to writing files in the .json format via the files
# json_save_dec and/or json_save_meta provided by the instructor.
# For this method, I utilized the json_save_dec file to allow the
# mailroom program to mimic .json functionality in its output (save)
# feature and to allow the input (load) feature to read-in .json file
# information to the program as donor information.
# ** The biggest issue I have noticed with the load feature that I
#    cannot address is that on loading another file, the previously
#    loaded file is no longer available in-memory, so it does not
#    truly 'load' and stay within the existing_donors dictionary.
# ------------------------------------------------------------------------------------------------------------------
import os
import json
from run_mailroom import input_directory, existing_donors
from mailroom_json import EachDonor, DonorList


def menu_selection(menu_choice, menu):
    while True:
        response = input(menu_choice).upper()
        try:
            if menu[response]() == "Exit Menu":
                break
        except KeyError:
            print("\nPick from the listed options.")


def exit_():
    return "Exit Menu"


def load():
    global existing_donors
    to_load = input("What file do you want to load (include extension):  ")
    try:
        with open(to_load, 'r') as f:
            donor_load = json.load(f)
            existing_donors = existing_donors.from_json_dict(donor_load)
            print('File: {} loaded!'.format(to_load))
    except FileNotFoundError as e:
        print(e)


def save():
    record_name = input("Name of file (w/o extension):  ")
    info = existing_donors.to_json()
    existing_donors.save_(record_name, info)
    print('File: {} saved!'.format(record_name))


def report():
    existing_donors.report()


def make_file(letter, destination):
    with open(destination, 'w') as f:
        f.write(letter)


def make_destination(donor, need_dir='y', directory=""):
    if need_dir == "y":
        directory = input(input_directory)
    destination = os.path.join(directory,
                               "{}.txt".format(donor.name.replace(' ', '_')))
    return destination


def get_amount(name):
    while True:
        try:
            amount = int(input("\nHow much did {} donate: ".format(name)))
            break
        except ValueError:
            print("\nNumerical entries only!")
    return amount


def thank_everyone():
    directory = input(input_directory)
    for donor in existing_donors.donor_dict:
        print('Writing {}\'s thank you letter to-file...'.format(donor.name))
        make_file(donor.write_letter(), make_destination(donor, 'n', directory))
    print('Done!')


def add_donation(name, amount, donor_list_obj):
    new_donor = True
    for donor in donor_list_obj.donor_dict:
        if name == donor.name:
            donor.new_donation(amount)
            temp = donor
            new_donor = False
    if new_donor:
        temp = EachDonor(name, [amount])
        donor_list_obj.add_(temp)
    return temp


def donor_name():
    while True:
        firstname = input('\nWhat is the Donor\'s first name:  ').strip()
        recipient = capitalize_names_check(firstname)
        if recipient.lower() == 'list':
            print(existing_donors)
            continue
        else:
            recipient += ' '
            lastname = input('What is the Donor\'s last name:  ').strip()
            recipient_last = capitalize_names_check(lastname)
            recipient += recipient_last
        return recipient


def add_new_full(name="", thank_you=""):
    if name == "":
        fname = input("Donor's first name: ").strip()
        name = capitalize_names_check(fname)
        lname = input("Donor's last name: ").strip()
        name2 = capitalize_names_check(lname)
        name += ' '
        name += name2
    amnt = get_amount(name)
    donor = add_donation(name, amnt, existing_donors)
    if thank_you == "":
        thank_you = input("\nSend a thank you to {}? (Y/N): ".format(name))
    if thank_you.upper() == 'Y':
        make_file(donor.write_letter(amnt), make_destination(donor))
        print('\nFile, {}.txt, saved! '.format(donor.name))


def format_names(n):
    split_name = n.split(' ')
    fn = split_name[0]
    ln = split_name[1]
    name = capitalize_names_check(fn)
    name += ' '
    new_last = capitalize_names_check(ln)
    name += new_last
    return name


def capitalize_names_check(n):
    """
    Unlike .capitalize() this function allows for
    a name to have capitalization w/in itself
    (ie McDonald) w/o overwriting any mid-
    -name cap. letters.
    :param n:
    :return:
    """
    length = len(n)
    if n[0] != n[0].upper():
        new_n = ''.join(let[0].upper() + let[1:] for let in n.split())
        return new_n
    else:
        if n[0] == n[0].upper():
            return n


def add_new():
    name = donor_name()
    donor_exists = existing_donors.check_(name)
    if donor_exists:
        donor = existing_donors.get_(name)
        new_donation = input("\n{} has donated. Add another donation?(Y/N)? ".format(name))
        if new_donation.upper() == 'Y':
            amount = get_amount(name)
            donor.new_donation(amount)
            make_file(donor.write_letter(amount), make_destination(donor))
        else:
            amount = 0
    else:
        add_new_full(name, 'y')


def donor_list_sum(donor_list):
    tot_donations = 0
    for donor in donor_list.donor_dictionary:
        tot_donations += donor.total_donated
    return tot_donations


menu_dict = {"A": add_new, "B": report, "C": thank_everyone,
             "D": load, "E": save, "Q": exit}
