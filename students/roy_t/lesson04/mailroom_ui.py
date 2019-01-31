#!/usr/bin/python3


# Author/Student:  Roy Tate (githubtater)


import mailroom_backend as mb
import time


class MailroomUI:

    def __init__(self, collection):
        if isinstance(collection, mb.DonorCollection):
            self.collection = collection
        else:
            raise TypeError('DonorCollection instance not found.')

    def menu_selection(self, arg_dict, response):
        """Dislay the user menu
        Args:
            arg_dict: dict of options
            response: option selected

        Returns:
            None. Based on the response, a function is executed"""
        try:
            arg_dict[response]['function']()
        except KeyError as e:
            print('\nInvalid response: ' + str(e) + '\nTry again.\n')
        except ValueError as e:
            print('\nInvalid entry: ' + str(e) + '\nTry again.\n')

    def main_menu(self):
        main_menu_args = {
            '1':{'option': '- Send a thank you', 'function': self.send_thank_you},
            '2':{'option': '- Print donor report', 'function': self.print_report},
            '3':{'option': '- Email all donors', 'function': self.email_all},
            '4':{'option': '- Challenge', 'function': self.challenge_menu},
            '5':{'option': '- Run Projections', 'function': self.print_projections},
            '6':{'option': '- Save Donor DB to JSON file', 'function': self.save_donor_json},
            '7':{'option': '- Load Donor DB from JSON file', 'function': self.load_donor_json},
            '8':{'option': '- Exit', 'function': self.die}
        }
        print('\n{:*^20}'.format(' MAIN MENU '))
        while True:
            for k, v in sorted(main_menu_args.items()):
                print(k, v['option'])
            response = input('\nEnter your selection: \n').strip()
            self.menu_selection(main_menu_args, response)

    def challenge_menu(self):
        """Menu presenting user with option to multiply all donations by a factor
            Args:
                None
            Returns:
                None
            Inputs:
                multiplier: the value to multiply all donations by"""
        multiplier = float(input('Enter the multiplier value: '))
        challenge_coll = self.collection.challenge(multiplier)
        print(challenge_coll.create_report(f'Challenge Report - Factor = {multiplier}'))

    def print_projections(self):
        """Run the 'Under 50' and 'Over 100' projection reports"""
        proj_over50, proj_over100 = self.collection.run_projections()

    def die(self):
        """All good things must come to an end"""
        print('\nExiting.')
        exit(0)

    def send_thank_you(self):
        """Takes input and returns a thank you letter"""
        thank_you_args = {
            '1':{'option': '- Enter a new donation', 'function': self.get_donation_amount},
            '2':{'option': '- Back to the Main Menu', 'function': self.main_menu},
            'list':{'option': '- Print a list of all donors', 'function': self.print_list},
        }
        for k, v in sorted(thank_you_args.items()):
            print(k, v['option'])
        response = input('\nEnter your selection: \n').strip()
        self.menu_selection(thank_you_args, response)

    def print_report(self):
        """Print a report of all current donors and donations"""
        report = self.collection.create_report()
        print(report)

    def email_all(self):
        """Saves an 'email' in the current current directory for all users. The email thanks the user and outlines
        their total donation amount"""
        save_directory = input('\nEnter the directory to save to:  ')
        try:
            self.collection.save_emails(save_directory)
        except PermissionError:
            print(f'Invalid permissions on directory: {save_directory}\n'
                  f'Files not saved.')
        except OSError:
            print(f'Invalid path: {save_directory}\n'
                  f'Files not saved.\n')

    def get_donation_amount(self):
        """Receive input from the user to enter a new donation"""
        donor_name = input('\nEnter the donor name (First Last): \n')
        donation_amount = float(input('\nEnter the donation amount: \n'))
        found = False
        for donor in self.collection.donors:
            if donor.name == donor_name:
                found = True
        if found:
            donor.donations.append(donation_amount)
        else:
            new_donor = mb.Donor(donor_name, [donation_amount])
            self.collection.donors.append(new_donor)

    def save_donor_json(self):
        self.collection.save_json()

    def load_donor_json(self):
        self.collection.load_json()

    def print_list(self):
        """Print the names of the current donor list."""
        print('Donor List:')
        for donor in self.collection.donors:
            print(donor.name)


if __name__ == "__main__":
    collection = mb.DonorCollection()

    # initialize the application with some donors
    donor1 = mb.Donor('Fred Flintstone', [27.14, 89.14])
    donor2 = mb.Donor('Wilma Willbanks', [150.00])
    donor3 = mb.Donor('Barney Rubble', [250, 24, 57, 175])

    # add the donor objects to the collection
    collection.add_donor(donor1)
    collection.add_donor(donor2)
    collection.add_donor(donor3)
    ui = MailroomUI(collection)
    ui.main_menu()


