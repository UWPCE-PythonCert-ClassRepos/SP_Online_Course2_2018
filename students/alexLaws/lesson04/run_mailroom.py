#!/usr/bin/env python3

import os
from mailroom import Donor, Donor_list
import json

my_donors = Donor_list(Donor('Ted Laws', [1000, 100]),
                       Donor('Kristin Laws', [150]),
                       Donor('Andrew Crawford', [2000, 2000, 4000]),
                       Donor('Beth Ross', [400]))


prompt = ("\nWhat would you like to do?\n"
          "Choose an action from this list:\n"
          "1 - Load Donation Records\n"
          "2 - Save Current Donation Records\n"
          "3 - Add a New Donation to the Records\n"
          "4 - Send a Thank You\n"
          "5 - Thank Everyone\n"
          "6 - Create a Report\n"
          "7 - Manage a Philanthropist donation\n"
          "8 - Build projections for a philanthropist\n"
          "9 - Quit\n")

directory_prompt = ("\nWhere would you like to save the thank you note?"
                    "\n(Leave blank for this directory): ")


def menu_selection(prompt, dispatch_dict):
    while True:
        response = input(prompt)
        try:
            if dispatch_dict[response]() == "Exit Menu":
                break
        except KeyError:
            print("\nThat was not one of the options.")


def exit():
    return "Exit Menu"


def load():
    global my_donors
    to_load = input("What file would you like to load?\n"
                    "Note: this will overwrite current info.\n"
                    "Note: include any .txt extensions!\n")
    with open(to_load, 'r') as f:
        donor_load = json.load(f)
    my_donors = my_donors.from_json_dict(donor_load)


def save():
    record_name = input("Please name your records file.\n"
                        "Note: Do not include a .txt extension:\n")
    info = my_donors.to_json()
    my_donors.save(record_name, info)


def report():
    my_donors.donor_report()


def generate_file(letter, destination):
    with open(destination, 'w') as f:
        f.write(letter)


def generate_destination(donor, need_dir='y', directory=""):
    if need_dir == "y":
        directory = input(directory_prompt)
    destination = os.path.join(directory,
                               "{}.txt".format(donor.name.replace(' ', '_')))
    return destination


def get_donation_amt(name):
    while True:
        try:
            amount = int(input("\nHow much did {} donate: ".format(name)))
            break
        except ValueError:
            print("\nThat wasn't a number value.")
    return amount


def thank_everyone():
    directory = input(directory_prompt)
    for donor in my_donors.donor_dictionary:
        generate_file(donor.write_note(), generate_destination(donor, 'n', directory))
    print("\nFinished")


def add_donation(name, amount, donor_list_obj):
    new_donor = True
    for donor in donor_list_obj.donor_dictionary:
        if name == donor.name:
            donor.new_donation(amount)
            temp = donor
            new_donor = False
    if new_donor:
        temp = Donor(name, [amount])
        donor_list_obj.add_donor(temp)
    return temp


def add_new_full(name="", thank_you=""):
    if name == "":
        name = input("\nA new donation! Who donated? (First and Last Name): ")
    amount = get_donation_amt(name)
    donor = add_donation(name, amount, my_donors)
    if thank_you == "":
        thank_you = input("\nWould you like a thank you note for {} (y/n): ".format(name))        
    if thank_you.lower() == 'y':
        generate_file(donor.write_note(amount), generate_destination(donor))


def send_to():
    recipient = input("\nWho is the thank you note for?\n"
                      "Enter a full name or 'list' to see a list: ")
    if recipient.lower() == 'list':
        print("\nHere are all the donors:")
        print(my_donors)
        recipient = input("\nWho is the thank you note for? ")
        return recipient
    else:
        return recipient


def thank_you():
    name = send_to()
    donor_exists = my_donors.check_donor(name)
    if donor_exists:
        donor = my_donors.get_donor(name)
        new_donation = input("\nDid {} make a new donation (y/n)? ".format(name))
        if new_donation.lower() == 'y':
            amount = get_donation_amt(name)
            donor.new_donation(amount)
        else:
            amount = 0
        generate_file(donor.write_note(amount), generate_destination(donor))
    else:
        add_new_full(name, 'y')


def donor_list_sum(donor_list):
    tot_donations = 0
    for donor in donor_list.donor_dictionary:
        tot_donations += donor.tot_given
    return tot_donations


def donation_multiplier(donation, multiplier, min=0, max=9999999):
    if donation > min and donation < max:
        return donation * multiplier
    else:
        return donation


def donor_multiplier(donor, multiplier, min, max):
    return Donor(donor.name, [donation_multiplier(x, multiplier, min, max) for x in donor.donations])


def donor_list_multiplier(donor_reference, multiplier, min, max):
    return [donor_multiplier(x, multiplier, min, max) for x in donor_reference.donor_dictionary]


def get_philan_info():
    while True:
        try:
            multiplier = int(input("\nWhat factor would the philanthropist "
                                   "like to multiply donations by? "))
            break
        except ValueError:
            print("\nThat wasn't a number value.")
    while True:
        try:
            min_donation = int(input("\nWhat is the min donation to match? "))
            break
        except ValueError:
            print("\nThat wasn't a number value.")
    while True:
        try:
            max_donation = int(input("\nWhat is the max donation to match? "))
            break
        except ValueError:
            print("\nThat wasn't a number value.")
    return (multiplier, min_donation, max_donation)


def philanthropist():
    global my_donors
    multip, min_donate, max_donate = get_philan_info()
    new_list = donor_list_multiplier(my_donors, multip, min_donate, max_donate)
    new_donor_list = Donor_list()
    for new_donor in new_list:
        new_donor_list.add_donor(new_donor)
    my_donors = new_donor_list


def hypothetical_philanthropist():
    global my_donors
    multip, min_donate, max_donate = get_philan_info()
    new_list = donor_list_multiplier(my_donors, multip, min_donate, max_donate)
    new_donor_list = Donor_list()
    for new_donor in new_list:
        new_donor_list.add_donor(new_donor)
    orig_total = donor_list_sum(my_donors)
    hypo_total = donor_list_sum(new_donor_list)
    print('\nThe total donations after your gift will be {}. Your share is '
          '{}'.format(hypo_total, hypo_total-orig_total))


menu_dict = {"1": load, "2": save, "3": add_new_full, "4": thank_you,
             "5": thank_everyone, "6": report, "7": philanthropist,
             "8": hypothetical_philanthropist, "9": exit}

if __name__ == '__main__':
    menu_selection(prompt, menu_dict)
