#!/usr/bin/python3
"""
updated mailroom program for Python 220 Lesson 7 assignment (relational databases)
changed json database to peewee/sqlite implementation
"""

from donors_model import Donations

def send_thank_you(db):
    """Add a donor/donation and print out a thank you letter"""
    # loop for user input: donor name, or list, or quit
    while True:
        name = input("\nDonor Full Name (type 'list' for donor list or 'q' to quit): ")
        if name in ('q', 'quit'):
            return
        if name == 'list':
            print(db.list_donors())
            continue
        while True:
            amount = input("Donation amount (type 'q' to quit): ")
            if amount in ('q', 'quit'):
                return
            try:
                db.add_donation(name, amount)
            except ValueError:
                print('Invalid input, try again')
            else:
                break
        print('\n' + db.thank_you_letter(name))


def create_a_report(db):
    """Print a summary of donors and amounts donated to screen"""
    print("\n"+db.summary_report())


def send_all_letters(db):
    """Write thank you letters to all donors to text files, filename = <donor_name>.txt"""
    dir_name = input("Output directory ('.' for current dir): ")
    db.send_all_letters(dir_name)


def run_projection(db):
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
            scenario = db.challenge(float(factor),
                                          float(min_filter) if min_filter else None,
                                          float(max_filter) if max_filter else None)
            print("\n"+scenario)
        except ValueError:
            print('Invalid inputs, try again')
        else:
            break


def update_donor_info(db):
    while True:
        name = input("\nDonor name ('q' to quit): ")
        if name in ('q', 'quit'):
            return
        info = input("   Update name or donation amount ('name', 'amount', or 'q' to quit: ")
        if info in ('q', 'quit'):
            return
        if info == 'name':
            new_name = input("   New name: ")
            if not db.update_donor(name, new_name):
                print("   Update failed, invalid inputs")
            continue
        if info == 'amount':
            old_amount = input("   Amount: ")
            new_amount = input("   New amount: ")
            if not db.update_donation(name, old_amount, new_amount):
                print("   Update failed, invalid inputs")


def delete_donor_info(db):
    while True:
        name = input("\nDonor name ('q' to quit): ")
        if name in ('q', 'quit'):
            return
        info = input("   Delete name or donation amount ('name', 'amount', or 'q' to quit): ")
        if info in ('q', 'quit'):
            return
        if info == 'name':
            if not db.delete_donor(name):
                print("   Delete failed, invalid inputs")
            continue
        if info == 'amount':
            amount = input("   Amount: ")
            if not db.delete_donation(name, amount):
                print("   Delete failed, invalid inputs")


def donation_log(db):
    """Print a summary of donors and amounts donated to screen"""
    print("\n"+db.donation_log())


def main_menu_error(_):
    """print error message if invalid menu item is entered"""
    print("Invalid choice, try again")


def quit_program(db):
    """close database, then exit program"""
    db.close_db()
    exit()


def main():
    """Main menu for mailroom program"""
    db = Donations('donor_db')
    db.load_db()

    switch_menu_dict = {
        "1": send_thank_you,
        "2": create_a_report,
        "3": send_all_letters,
        "4": run_projection,
        "5": update_donor_info,
        "6": delete_donor_info,
        "7": donation_log,
        "q": quit_program,
        "quit": quit_program
        }
    while True:
        print("\nMAIN MENU")
        print("   1 = Send a Thank You")
        print("   2 = Create a Report")
        print("   3 = Send Letters to Everyone")
        print("   4 = Run A Projection")
        print("   5 = Update Donor Name/Donation")
        print("   6 = Delete Donor Name/Donation")
        print("   7 = Print Donation Log")
        print("   q = Quit")
        choice = input("   ? ")
        switch_menu_dict.get(choice, main_menu_error)(db)


if __name__ == '__main__':
    main()
