# lesson 07 mailroom using peewee
# !/usr/bin/env python3

""" Run Mailroom """

import os
import logging

from mailroom_initial_populate import *
from mailroom_modify import *
from mailroom_analyze import *
from mailroom_write import *


def quit():
        print("\nGoodbye.")
        exit()


if __name__ == '__main__':
    ask_pop = input("Populate database for the first time?\n>>")
    if ask_pop.lower() == "yes":
        populate_initial_donors()
        populate_initial_donations()  
    while True:
        database.close()
        ask = input("\nPlease choose an action:\n"
                "1) Add donations and send thank yous\n"
                "2) Update donation\n"
                "3) Delete donation\n"
                "4) Create a report\n"
                "5) Analyze for contribution matching\n"
                "6) Write letters to all donors\n"
                "7) Save data to text file\n"
                "8) Quit\n"
                ">>")
        options = {"1": add_donation, "2": update_donation, "3": delete_donation, 
                   "4": print_report, "5": match_donations, "6": write_letters, 
                   "7": save_to_text, "8": quit}
        try:
            options[ask]()
        except KeyError:
            print("\nThere was an error. Please try again.")