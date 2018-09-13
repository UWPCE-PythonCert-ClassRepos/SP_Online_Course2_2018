"""
Main control of mailroom.py
"""

from mailroom import Donor, DonorList

def main():
    """ Controls the menu. """
    donor1 = Donor("Tom Horn", [599.23, 1000.00])
    donor2 = Donor("Theo Hartwell", [0.01, 0.01, 0.1])
    donor3 = Donor("Bailey Kimmitt", [8723.22, 27167.22, 91817.66])
    donor4 = Donor("Paul Hubbell", [90012.32, 2312.24])
    donor5 = Donor("David Beckham", [1817266.11, 123123.66, 111335.112])
    donors = DonorList([donor1, donor2, donor3, donor4, donor5])

    while True:
        choice = input(
        "Please select an option:\n\
        1 - Send Thanks\n\
        2 - Create Donor Report\n\
        3 - Send Letters\n\
        4 - Quit\n")
        print()
        if choice == '1':
             # Get donor
            target_donor = input("Please enter the donor's full name.  ")
            # Get donation
            try:
                new_donation = float(input("Please enter the donation amount for {}.  ".format(target_donor)))
            except ValueError:
                print("Please enter a number.  ")
            donors.send_thanks(target_donor, new_donation)
        if choice == '2':
            donors.create_report()
        if choice == '3':
            donors.create_letters()
        if choice == '4':
            donors.quitter()

if __name__ == "__main__":
    main()