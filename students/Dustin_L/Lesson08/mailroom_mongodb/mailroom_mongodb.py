#!/usr/bin/env python3
"""Mail Room MongoDB Module

This module contains all of the functions for the Mail Room module that
utilizes MongoDB for its database.
"""
import sys
from donor_dict import DonorDict

SELECT_PROMPT = ('\nPlease select from the following options:\n'
                 '\t1. Send a Thank You\n'
                 '\t2. Create a Report\n'
                 '\t3. Send letters to all donors\n'
                 '\t4. Create contribution projection\n'
                 '\t5. Delete donor\n'
                 '\t6. Update donation\n'
                 '\t7. quit\n'
                 ' --> ')
PROMPT_OPTS = (1, 2, 3, 4, 5, 6, 7)


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
        donor_db (DonorDict): Database instance containing all donors

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
            for name in donor_db:
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
        donor_db (DonorDict): Database instance containing all donors
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

    donor_db.add_donation(donor, donation)
    print(DonorDict.thank_you_fmt.format(donor, donation))


def create_report(donor_db):
    """Generate and print a report of donors in the database

    Prints a list of donors, sorted by total historical donation amount.
    Includes Donor Name, total donated, number of donations and average
    donation

    Args:
        donor_db (DonorDict): Database instance containing all donors
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


def delete_donor(donor_db):
    """Prompts user for a donor to delete from the database.

    Args:
        donor_db (DonorDict): Database instance containing all donors.
    """
    name_prompt = ('\nPlease enter name of donor to delete:\n'
                   '(Enter "list" to see all donors)\n'
                   '(Enter "quit" to return to main menu)\n'
                   ' --> ')

    donor = prompt_for_donor(name_prompt, donor_db)
    if not donor:
        return

    if donor_db.delete_donor(donor):
        print(f'\n{donor} successfully removed')
    else:
        print(f'\n{donor} not found in database.')


def update_donation(donor_db):
    """Prompts user to update a donation made by a specific donor to a new
       donation amount.

    Args:
        donor_db (DonorDict): Database instance containing all donors.
    """
    name_prompt = ('\nPlease enter name of relevant donor:\n'
                   '(Enter "list" to see all donors)\n'
                   '(Enter "quit" to return to main menu)\n'
                   ' --> ')
    amount_prompt = ('\nPlease enter the donation amount to be updated:\n'
                     '(Enter "quit" to return to main menu)\n'
                     ' --> ')
    new_amount_prompt = ('\nPlease enter the new donation amount:\n'
                         '(Enter "quit" to return to main menu)\n'
                         ' --> ')
    error_prompt = '\nDonation amount must be a number'

    donor = prompt_for_donor(name_prompt, donor_db)
    if not donor:
        return

    old_donation = prompt_for_float(amount_prompt, error_prompt)
    if not old_donation:
        return

    new_donation = prompt_for_float(new_amount_prompt, error_prompt)
    if not new_donation:
        return

    if donor_db.update_donation(donor, old_donation, new_donation):
        print(f'\n{donor}\'s donation of ${old_donation} successfully updated '
              f'to ${new_donation}')
    else:
        print(f'\nUnable to locate {donor}\'s donation of ${old_donation} in '
              f'the database')


def quit_mailroom(donor_db):
    """Exit operations when quitting mail room"""
    print('Quitting mailroom...')


def main():
    """Main function"""
    donor_db = DonorDict()

    if len(sys.argv) > 1 and sys.argv[1] == 'purge':
        donor_db.purge_db()

    opt_dict = dict(zip(PROMPT_OPTS, (send_thank_you,
                                      create_report,
                                      send_letters,
                                      create_projection,
                                      delete_donor,
                                      update_donation,
                                      quit_mailroom)))
    choice = ''
    while choice != PROMPT_OPTS[-1]:
        choice = get_usr_input()
        opt_dict.get(choice)(donor_db)


if __name__ == '__main__':
    main()
