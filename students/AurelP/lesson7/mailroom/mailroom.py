#mailroon with peewee database

import random
import logging
from datetime import datetime, date, timedelta
from peewee import *
from ap_model import *
from ap_functions import *
from ap_populate import *


def menu_selection(prompt, dispatch_dict):
    while True:
        response=input(prompt).lower()
        try:
            if dispatch_dict[response]()=='exit menu':
                break
        except KeyError:
            print("Error: Value not an option, try again.")
            continue

def thank_you():
    menu_selection(thank_you_prompt, thank_you_dispatch)

def update_donors():
    menu_selection(update_donors_prompt, update_donors_dispatch)

def quit():
    print ('quit the menu')
    return "exit menu"

def input_donor():
    while True:
        try:
            x = str(input("Enter a donor name: "))
            if not all(a.isalpha() or a.isspace() for a in x) or x.isspace():
                raise ValueError()
            else:
                return(x)
        except ValueError:
            print("Error: Donor names must contain letters and spaces")

def input_donation():
    while True:
        try:
            d = float(input("Please enter a donation amount: "))
            if d < 0.01 :
                raise ValueError()
            else:
                return(d)
        except ValueError:
            print("Error: Not a number, negative number, or number too small")

def add_d():
    don_lst=donors_list()
    print ('add_donation')
    x=input_donor()
    if x.lower()=="q":
        print("q is not a donor name")
        return None
    d=input_donation()
    if x in don_lst:
        print('Donor:{} already in database'.format(x))
    else:
        add_donor(x)
        print('Donor:{} added to the database'.format(x))
    add_donation(x,d)
    letter(x,float(d))

def add_donor_q():
    don_lst=donors_list()
    print ('add_donation')
    x=input_donor()
    if x.lower()=="q":
        print("q is not a donor name")
        return None
    if x in don_lst:
        print('Donor:{} already in database'.format(x))
    else:
        add_donor(x)
        print('Donor:{} added to the database'.format(x))

def add_donation_q():
    don_lst=donors_list()
    print ('add_donation')
    x=input_donor()
    if x.lower()=="q":
        print("q is not a donor name")
        return None
    d=input_donation()
    if x in don_lst:
        add_donation(x,d)
        print('Donation of:{} from Donor:{} added to database'.format(d,x))
    else:
        print('Donor:{} not in database; Add Donor first'.format(x))


def donor_list():
    d=donors_list()
    print ('\nCurrent Donor list:')
    for i in d:
        print (i)

def letter(name, amount):
    txt = """\n
            To:       {0:s}
            Subject:  Your donation of ${1:,.2f}
            Dear {0:s},\n

            Thank you for your donation of ${1:,.2f}.\n
     """
    print (txt.format(name, amount))

def donor_stat():
    lc=donor_totals()
    lc.sort(key=lambda e: e[1], reverse=True)
    return lc

def report():
    """
    Generate the statistics for the donor list.
    """
    lst=donor_stat()
    print('\n')
    print ('Donor Name'+' '*16+'|'+' '*9+'Total Given'+' |'+' '*6+'Num Gifts'+' |'+' '*8+'Average Gift')
    print('-'*26+'|'+'-'*21+'|'+'-'*16+'|'+'-'*20+'|')
    for d in lst:
        print('{:<25s} | ${:>18,.2f} | {:>15d} | ${:>18,.2f}'.format(
                d[0], d[1],d[2],d[3]))
    print ('\n')

def write():
    donors=donors_dict()
    txt = """\n
        Dear {0:s},

        Thank you for your very kind donation of ${1:,.2f}.
        It will be put to very good use.

                    Sincerely,
                        -The Team
     """
    for d in donors.keys():
        file_name = d + ".txt"
        if donors[d][0] is not None:
            with open(file_name, 'w') as f:
                f.write(txt.format(d, sum(donors[d])))
                print("Generated letter for {:s}!\n".format(d))

def recent_donations():
    ls=donor_most_recent_donation()
    for i in ls:
        print(i)

def all_donations():
    donor_dict=donors_dict(list_of_donations())
    for item, value in donor_dict.items():
        print('Donor: {} donated:'.format(item), value)

def del_amount():
    x=input_donor()
    if x.lower()=="q":
        print("q is not a donor name")
        return None
    d=input_donation()
    delete_donation(x, d)

def update_amount():
    x=input_donor()
    if (x.lower()=="q") or (x not in donors_list()):
        print("q is not a donor name or donor not in database")
        return None
    print("\nEnter old donation")
    d_old=input_donation()
    print("\nEnter new donation")
    d_new=input_donation()
    update_donation(x, d_old, d_new)

def del_donor():
    x=input_donor()
    if x.lower()=="q":
        print("q is not a donor name")
        return None
    else:
        delete_donor(x)

main_dispatch = {
    "1": thank_you,
    "2": report,
    "3": write,
    "4": update_donors,
    "q": quit
}

thank_you_dispatch = {
    "1": add_d,
    "2": donor_list,
    "q": quit
}

update_donors_dispatch = {
    "1": recent_donations,
    "2": all_donations,
    "3": del_amount,
    "4": update_amount,
    "5": del_donor,
    "6": add_donor_q,
    "7": add_donation_q,
    "q": quit
}

main_prompt = ("\nMain Menu\n"
               "1 - Send a Thank You\n"
               "2 - Create a Report\n"
               "3 - Send letters to everyone\n"
               "4 - Administrative tasks: update & delete\n"
               "q  Quit\n")

thank_you_prompt = ("\nThank you menu:\n"
                    "1 - Add donation and send message\n"
                    "2 - Display list of current donors\n"
                    "q - Quit\n")

update_donors_prompt = ("\nUpdate menu:\n"
                    "1 - Last donation report\n"
                    "2 - All donations report\n"
                    "3 - Delete Donation\n"
                    "4 - Update Donation\n"
                    "5 - Delete Donor\n"
                    "6 - Add Donor - no thank you letter\n"
                    "7 - Add Donation - no thank you letter\n"
                    "q - Quit\n")

if __name__=='__main__':
    #populate_donors()
    #populate_donations()
    menu_selection(main_prompt, main_dispatch)
