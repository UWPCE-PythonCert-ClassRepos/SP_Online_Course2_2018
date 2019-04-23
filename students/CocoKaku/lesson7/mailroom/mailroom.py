#!/usr/bin/python3
"""
updated mailroom program for Python 220 Lesson 7 assignment (relational databases)
changed json database to peewee/sqlite implementation
"""

from donors_model import Donation

def send_thank_you():
    """Add a donor/donation and print out a thank you letter"""
    # loop for user input: donor name, or list, or quit
    while True:
        name = input("\nDonor Full Name (type 'list' for donor list or 'q' to quit): ")
        if name in ('q', 'quit'):
            return
        if name == 'list':
            print(Donation.list_donors())
            continue
        while True:
            amount = input("Donation amount (type 'q' to quit): ")
            if amount in ('q', 'quit'):
                return
            try:
                Donation.add_donation(name, amount)
            except ValueError:
                print('Invalid input, try again')
            else:
                break
        print('\n' + Donation.thank_you_letter(name))


def create_a_report():
    """Print a summary of donors and amounts donated to screen"""
    print("\n"+Donation.summary_report())


def send_all_letters():
    """Write thank you letters to all donors to text files, filename = <donor_name>.txt"""
    dir_name = input("Output directory ('.' for current dir): ")
    Donation.send_all_letters(dir_name)


def run_projection():
    """Run projection showing total contribution of challenge scenario"""
    while True:
        factor = input("\nChallenge factor ('q' to quit): ")
        if factor in ('q', 'quit'):
            return
        min_filter = input("Minimum donation to challenge (<return> for none, 'q' to quit): ")
        if min_filter in ('q', 'quit'):
            return
        max_filter = input("Maximum donation to challenge (<return> for none, 'q' to quit): ")
        if max_filter in ('q', 'quit'):
            return
        try:
            scenario = Donation.challenge(float(factor),
                                          float(min_filter) if min_filter else None,
                                          float(max_filter) if max_filter else None)
            print("\n"+scenario)
        except ValueError:
            print('Invalid inputs, try again')
        else:
            break


def main_menu_error():
    """print error message if invalid menu item is entered"""
    print("Invalid choice, try again")


def quit_program():
    """close database, then exit program"""
    Donation.close_db()
    exit()


def main():
    """Main menu for mailroom program"""
    Donation.open_db("donations.db")

    switch_menu_dict = {
        "1": send_thank_you,
        "2": create_a_report,
        "3": send_all_letters,
        "4": run_projection,
        "q": quit_program,
        "quit": quit_program
        }
    while True:
        print("\nMAIN MENU")
        print("   1 = Send a Thank You")
        print("   2 = Create a Report")
        print("   3 = Send Letters to Everyone")
        print("   4 = Run A Projection")
        print("   q = Quit")
        choice = input("   ? ")
        switch_menu_dict.get(choice, main_menu_error)()


if __name__ == '__main__':
    main()
