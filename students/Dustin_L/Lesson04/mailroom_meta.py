#!/usr/bin/env python3
"""Mail Room Meta Programming Module

This module contains all of the functions for the meta programming
Mail Room module.
"""

import os
from donor import Donor
from donor_database import DonorDatabase, DonorDict

SELECT_PROMPT = ('\nPlease select from the following options:\n'
                 '\t1. Send a Thank You\n'
                 '\t2. Create a Report\n'
                 '\t3. Send letters to all donors\n'
                 '\t4. Create contribution projection\n'
                 '\t5. quit\n'
                 ' --> ')
PROMPT_OPTS = (1, 2, 3, 4, 5)


def get_usr_input():
    """Get input from user.

    Prompt user to select one of three choices. If the user selects one of
    these three, that value is returned. If not, the user is prompted again to
    select.

    Returns:
        int: Value corresponding to user choice
    """
    usr_in = None
    while usr_in not in PROMPT_OPTS:
        try:
            usr_in = int(input(SELECT_PROMPT))
        except ValueError:
            print(f'\nPlease try again. Valid options are: {PROMPT_OPTS}')
        else:
            if usr_in not in PROMPT_OPTS:
                print(f'\nPlease select a number between {PROMPT_OPTS[0]}'
                      f' and {PROMPT_OPTS[-1]}')

    return usr_in


def prompt_for_donor(prompt, donor_db):
    """Prompt user to enter a donor name.

    Allows user the additional options of:
     - 'quit': quit donor prompt
     - 'list': list all current donors

    Args:
        prompt (str): String to prompt user with.
        donor_db (DonorDatabase): Database instance containing all donors

    Returns:
        str: Donor name.
    """
    donor = None

    while not donor:
        usr_in = input(prompt).strip().lower()

        if usr_in.startswith('q'):
            break
        elif usr_in == 'list':
            print()
            for name in donor_db.keys():
                print(name.title())
        else:
            donor = " ".join([name.title() for name in usr_in.split()])

    return donor


def prompt_for_float(prompt, error_prompt):
    """Prompt for user contribution factor

    Args:
        prompt (str): String to prompt user with.
        error_prompt (str): Error response to invalid user input.

    Returns:
        float: Factor value
    """
    val = None

    while not val and val != 0.0:
        usr_in = input(prompt).strip().lower()

        if usr_in.startswith('q'):
            break
        else:
            try:
                val = float(usr_in)
            except ValueError:
                print(error_prompt)

    return val


def send_thank_you(donor_db):
    """Send a thank you.

    Prompt for a Full Name.
    If the user types ‘list’, show them a list of the donor names and re-prompt
    If the user types a name not in the list, add that name to the data
    structure and use it.
    If the user types a name in the list, use it.
    Once a name has been selected, prompt for a donation amount.
    Turn the amount into a number – it is OK at this point for the program to
    crash if someone types a bogus amount.
    Once an amount has been given, add that amount to the donation history of
    the selected user.
    Finally, use string formatting to compose an email thanking the donor for
    their generous donation. Print the email to the terminal and return to the
    original prompt.

    Args:
        donor_db (DonorDatabase): Database instance containing all donors
    """
    name_prompt = ('\nPlease enter name of "Thank You" recipient:\n'
                   '(Enter "list" to see all donors)\n'
                   '(Enter "quit" to return to main menu)\n'
                   ' --> ')
    amount_prompt = ('\nPlease enter the donation amount:\n'
                     '(Enter "quit" to return to main menu)\n'
                     ' --> ')
    error_prompt = '\nDonation amount must be a number'

    donor = prompt_for_donor(name_prompt, donor_db)
    if not donor:
        return

    donation = prompt_for_float(amount_prompt, error_prompt)
    if not donation:
        return

    donor_db[donor].add_donation(donation)
    print(donor_db.thank_you_fmt.format(donor, donation))


def create_report(donor_db):
    """Generate and print a report of donors in the database

    Prints a list of donors, sorted by total historical donation amount.
    Includes Donor Name, total donated, number of donations and average
    donation

    Args:
        donor_db (DonorDatabase): Database instance containing all donors
    """
    print(donor_db.create_report())


def send_letters(donor_db):
    """Create a letter for each donor and write to disk as a text file"""
    donor_db.send_letters()


def create_projection(donor_db):
    """Create contribution projection based on user constraints"""
    factor_prompt = ('\nPlease enter the contribution multiplicative factor:\n'
                     '(Enter "quit" to return to main menu)\n'
                     ' --> ')
    min_prompt = ('\nPlease enter the minimum donation limit:\n'
                  '(Optional, press "0" to continue)\n'
                  ' --> ')
    max_prompt = ('\nPlease enter the maximum donation limit:\n'
                  '(Optional, press "0" to continue)\n'
                  ' --> ')
    error_prompt = ('\nValue must be a float')

    factor = prompt_for_float(factor_prompt, error_prompt)
    if not factor:
        return

    min_don = prompt_for_float(min_prompt, error_prompt)
    max_don = prompt_for_float(max_prompt, error_prompt)
    projection = donor_db.projection(factor, min_don=min_don, max_don=max_don)

    print(f'\nProjected contribution value: ${projection:,.2f}')


def quit_mailroom(donor_db):
    """Exit operations when quitting mail room"""
    prompt = ('\nWould you like to save the Donor Database? (y/[n])\n'
              ' --> ')

    usr_in = input(prompt).strip().lower()
    if usr_in.startswith('y'):
        donor_db.save()

    print('Quitting mailroom...')


def main():
    """Main function"""
    with open(os.path.join(os.getcwd(), 'donors.json'), 'r') as f:
        donor_db = DonorDatabase.load(f)

    opt_dict = dict(zip(PROMPT_OPTS, (send_thank_you,
                                      create_report,
                                      send_letters,
                                      create_projection,
                                      quit_mailroom)))
    choice = ''
    while choice != PROMPT_OPTS[-1]:
        choice = get_usr_input()
        opt_dict.get(choice)(donor_db)


if __name__ == '__main__':
    main()
