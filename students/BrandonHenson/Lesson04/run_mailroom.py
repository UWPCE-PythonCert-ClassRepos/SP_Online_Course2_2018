# Brandon Henson
# Python 220
# Lesson 4
# 7-15-18
# !/usr/bin/env python3

import os
from mailroom import Donor, Donor_list
import json

donor_history = Donor_list(Donor('Brandon Henson', [1005.49, 3116.72, 5200]),
                                        Donor('Alicia Henson', [21.47, 1500]),
                       Donor('Michael Green', [2400.54]),
                       Donor('Brandon Henson Jr', [355.42, 579.31]),
                       Donor('Kaiya Henson', [636.9, 850.13, 125.23]))

prompt = ('\nSelect an option:\n'
             '[1] Send A Thank You To New Or Exsisting Donor\n'
             '[2] Create a Report\n'
             '[3] Send letters to everyone\n'
             '[4] Exit\n'
             '[5] Save\n'
             '[6] Load\n')


directory_prompt = ("\nChoose save location or press enter for default")


def menu_selection(prompt, dispatch_dict):
    while True:
        response = input(prompt)
        try:
            if dispatch_dict[response]() == "Exit Menu":
                break
        except KeyError:
            print("\nPick from the listed options.")


def exit():
    return "Exit Menu"


def load():
    global donor_history
    to_load = input("What do you want to load?\n")
    with open(to_load, 'r') as f:
        donor_load = json.load(f)
    donor_history = donor_history.from_json_dict(donor_load)


def save():
    record_name = input("Name Of file?")
    info = donor_history.to_json()
    donor_history.save(record_name, info)


def report():
    donor_history.donor_report()


def make_file(letter, destination):
    with open(destination, 'w') as f:
        f.write(letter)


def make_destination(donor, need_dir='y', directory=""):
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
            print("\nThis only works with a number!")
    return amount


def thank_everyone():
    directory = input(directory_prompt)
    for donor in donor_history.donor_dictionary:
        make_file(donor.write_note(), make_destination(donor, 'n', directory))


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
        name = input("\nWho is the donor?")
    amount = get_donation_amt(name)
    donor = add_donation(name, amount, donor_history)
    if thank_you == "":
        thank_you = input("\nSend a thank you to {}? (y/n): ".format(name))
    if thank_you.upper() == 'Y':
        make_file(donor.write_note(amount), make_destination(donor))


def send_to():
    recipient = input("\nWho is the donor?\n"
                      "Enter a full name or 'list' to see a list: ")
    if recipient.upper() == 'LIST':
        print("\nHere are the donors:")
        print(donor_history)
        recipient = input("\nWho is the donor? ")
        return recipient
    else:
        return recipient


def thank_you():
    name = send_to()
    donor_exists = donor_history.check_donor(name)
    if donor_exists:
        donor = donor_history.get_donor(name)
        new_donation = input("\n{} has donated. Another?(y/n)? ".format(name))
        if new_donation.upper() == 'Y':
            amount = get_donation_amt(name)
            donor.new_donation(amount)
        else:
            amount = 0
        make_file(donor.write_note(amount), make_destination(donor))
    else:
        add_new_full(name, 'y')


arg_dict = {"1": thank_you, "2": report, "3": thank_everyone,
            "4": exit, "5": save, "6": load}

if __name__ == '__main__':
    menu_selection(prompt, arg_dict)
