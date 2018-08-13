#!/usr/bin/env python3

from persist_donordonation import (create_donor, create_donation,
                                   get_donor_names, get_donor_donations)

import pathlib
pth = pathlib.Path('./')


class DonorList:

    def __init__(self):
        self._rollup = {}

    @property
    def rollup(self):
        return self._rollup

    def update_rollup(self, donor_rollup):
        self._rollup.update(donor_rollup)

    @property
    def donor_names(self):
        return get_donor_names()

    @property
    def donor_donations(self):
        return get_donor_donations()

    def add_donor(self, name):
        try:
            create_donor(name)
        except:
            pass

    def add_donation(self, donor, val):
        if val < 1:
            raise ValueError("A positive donation value is required.")

        try:
            create_donation(donor, val)
        except:
            pass

    def get_donor(self, name):
        if not name:
            raise ValueError("Please provide a donor name.")

        if name in self.donors:
            return name
        else:
            return "Donor not found."

    def get_donations(self, name):
        if not name:
            raise ValueError("Please provide a donor name.")

        if name in self.donor_donations:
            return self.donor_donations[name]
        else:
            return "Donor not found."

    def get_donor_names(self):
        print("\n".join([donor for donor in self.donor_names]))

    def compose_thank_you(self, donor):
        if not donor:
            raise ValueError("Please provide a donor.")

        message_obj = {
            'donor_name': donor,
            'donations': sum(self.get_donations(donor))
        }

        message = 'Dear {donor_name}, thanks so much '\
                  'for your generous donations in the amount of: '\
                  '${donations}.'.format(**message_obj)

        return message

    def generate_rollup(self):
        for donor in self.donor_names:
            donations = self.get_donations(donor)

            number = len(donations)
            total = int(sum(donations))
            average = float(format(sum(donations) / len(donations), '.2f'))

            donor_rollup = {
                donor: dict(zip(('number', 'total', 'average'),
                                (number, total, average)))
            }

            self.update_rollup(donor_rollup)

    def generate_table(self):
        if not len(self.donor_names):
            print('The list of donors is empty.')
            return

        self.generate_rollup()

        headings = ('Donor Name', 'Num Gifts', 'Total Given', 'Average Gift')

        print('{:20}{:<15}{:<15}{:<15}'.format(*headings))
        print('{:_<65}'.format(''))

        for donor in self.donor_names:
            print('{:<20}'.format(donor), ('{:<15}' * len(self.rollup[donor]))
                  .format(*self.rollup[donor].values()))

    def generate_letters(self):
        if not len(self.donor_names):
            print('The list of donors is empty.')
            return

        self.generate_rollup()

        for donor in self.donor_names:
            with open(donor.replace(' ', '_') + '.txt', 'w') as outfile:
                outfile.write(self.compose_thank_you(donor))

        print('Letters generated: ')

        for f in pth.iterdir():
            if '.txt' in str(f):
                print(f)


class DonorCli:

    def __init__(self, donorCollection):
        self._donorCollection = donorCollection

    @property
    def donorCollection(self):
        return self._donorCollection

    def set_donor(self):
        while True:
            try:
                name = input('Please enter a donor name: ')
                if not name:
                    raise ValueError
            except ValueError:
                print('Oops, name is required.')
                return
            else:
                self.donorCollection.add_donor(name)
                self.set_donation(name)
                print('{} added. Current donors: '.format(name))
                self.donorCollection.get_donor_names()
                return

    def set_donation(self, donor):
        while True:
            try:
                donation = int(input('Please enter a donation amount: '))
                if not donation > 0:
                    raise ValueError
            except ValueError:
                print('Please provide a whole number greater than zero.')
            else:
                self.donorCollection.add_donation(donor, donation)
                print('${} donation received.'.format(donation))
                self.get_selection()

    def accept_donation(self):
        if not self.donorCollection.donor_names:
            print('The list of donors is empty.')
            return

        instruction = 'Please enter a full name '\
                      'or type \'list\' to see donors:\n'

        name_input = input(instruction)

        if name_input == 'list':
            self.donorCollection.get_donor_names()
            self.accept_donation()
        elif name_input in self.donorCollection.donor_names:
            self.set_donation(name_input)
        else:
            print('Donor not found.')

    def apply_selection(self, selection):
        arg_dict = {
            '1': self.set_donor,
            '2': self.accept_donation,
            '3': self.donorCollection.generate_table,
            '4': self.donorCollection.generate_letters,
            '5': quit
        }
        try:
            if not arg_dict.get(selection):
                raise KeyError
            arg_dict.get(selection)()
        except KeyError:
            print('Oops, invalid selection.')

    def get_selection(self):
        options = 'Please select from the menu:\n'\
                  '1) add new donor\n'\
                  '2) log donation\n'\
                  '3) create a report\n'\
                  '4) send letters to everyone\n'\
                  '5) quit\n'
        while True:
            selection = input(options)
            self.apply_selection(selection)
            if selection == '2':
                self.get_selection()


def main():
    dl = DonorList()
    cli = DonorCli(dl)
    cli.get_selection()


if __name__ == "__main__":
    main()
