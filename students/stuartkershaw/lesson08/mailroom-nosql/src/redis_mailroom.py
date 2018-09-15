#!/usr/bin/env python3

from mongo_persist_donordonation import (create_donor, create_donation,
                                         update_donor, update_donation,
                                         delete_donor, delete_donation,
                                         get_donor_names, get_donor_donations)

from redis_persist_donordonation import (set_rollup_num_donations,
                                         set_rollup_sum_donations,
                                         set_rollup_avg_donations,
                                         get_num_donations,
                                         get_sum_donations,
                                         get_avg_donations,
                                         delete_donor_donations)

import pprint
import pathlib
pth = pathlib.Path('./')


class DonorList:

    def __init__(self):
        self._rollup = {}
        self._donor_names = get_donor_names()
        self._donor_donations = get_donor_donations()

    @property
    def rollup(self):
        return self._rollup

    def update_rollup(self):
        for donor in self.donor_names:
            self._rollup.setdefault(
                donor, dict(zip(('number', 'total', 'average'),
                                (get_num_donations(donor),
                                 get_sum_donations(donor),
                                 get_avg_donations(donor)))))

    @property
    def donor_names(self):
        return self._donor_names

    def update_donor_names(self):
        self._donor_names = get_donor_names()

    @property
    def donor_donations(self):
        return self._donor_donations

    def update_donor_donations(self):
        self._donor_donations = get_donor_donations()

    def add_donor(self, name):
        try:
            create_donor(name)
            self.update_donor_names()
        except:
            pass

    def add_donation(self, donor, val):
        if val < 1:
            raise ValueError("A positive donation value is required.")

        try:
            create_donation(donor, val)
            self.update_donor_donations()
        except:
            pass

    def get_donor(self, name):
        if not name:
            raise ValueError("Please provide a donor name.")

        if name in self.donors:
            return name
        else:
            return "Donor not found."

    def get_donations_by_name(self, name):
        if not name:
            raise ValueError("Please provide a donor name.")

        if name in self.donor_donations:
            return self.donor_donations[name]
        else:
            return "Donor not found."

    def compose_thank_you(self, donor):
        if not donor:
            raise ValueError("Please provide a donor.")

        message_obj = {
            'donor_name': donor,
            'donations': sum(self.get_donations_by_name(donor))
        }

        message = 'Dear {donor_name}, thanks so much '\
                  'for your generous donations in the amount of: '\
                  '${donations}.'.format(**message_obj)

        return message

    def generate_rollup(self):
        for donor in self.donor_names:
            donations = self._donor_donations[donor]

            set_rollup_num_donations(donor, donations)
            set_rollup_sum_donations(donor, donations)
            set_rollup_avg_donations(donor, donations)

    def generate_table(self):
        if not len(self.donor_names):
            print('The list of donors is empty.')
            return

        self.update_rollup()

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

    def set_donor_donations(self):
        self.donorCollection.update_donor_names()
        self.donorCollection.update_donor_donations()
        self.donorCollection.generate_rollup()

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
                self.add_donation(name)
                print('{} added. Current donors: '.format(name))
                print("\n".join(self.donorCollection.donor_names))
                return

    def add_donation(self, donor):
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
                self.donorCollection.generate_rollup()
                self.get_selection()

    def find_donor_donation_update(self, donor, donation=None):
        if not donation:
            while True:
                try:
                    action = input('Please enter \'1\' to update or \'2\' to '
                                   'delete: '.format(donor))
                    if action not in ['1', '2']:
                        raise ValueError
                except ValueError:
                    print('Oops, invalid selection...')
                    return
                else:
                    if action == '1':
                        updated_name = input('Please enter a new name for {}: '
                                             .format(donor))
                        update_donor(donor, updated_name)
                        delete_donor_donations(donor)
                    elif action == '2':
                        validate = input('Are are you sure you wish to delete '
                                         '{}? (yes/no): '.format(donor))
                        if validate.lower() == 'yes':
                            delete_donor(donor)
                            delete_donor_donations(donor)
                        else:
                            print('Donor {} unchanged.'.format(donor))
                    self.set_donor_donations()
                    return
        else:
            while True:
                try:
                    action = input('Please enter \'1\' to update or \'2\' to '
                                   'delete: '.format(donation))
                    if action not in ['1', '2']:
                        raise ValueError
                except ValueError:
                    print('Oops, invalid selection...')
                    return
                else:
                    if action == '1':
                        updated_value = input('Please enter a new val for {}: '
                                              .format(donation))
                        try:
                            updated_value = int(updated_value)
                            if not updated_value > 0:
                                raise ValueError
                            else:
                                update_donation(donor, donation, updated_value)
                                
                        except ValueError:
                            print('Oops, invalid selection...')
                            return
                    elif action == '2':
                        validate = input('Are are you sure you wish to delete '
                                         '{}? (yes/no): '.format(donation))
                        if validate.lower() == 'yes':
                            delete_donation(donor, donation)
                        else:
                            print('Donation {} unchanged.'.format(donation))
                    self.set_donor_donations()
                    return

    def select_donation(self, donor):
        donations = self.donorCollection.get_donations_by_name(donor)
        range_donations = range(1, len(donations) + 1)
        donations_dict = dict(zip(range_donations, donations))

        while True:
            try:
                print('Updating {}\'s donations.'.format(donor))
                pp = pprint.PrettyPrinter(width=1)
                pp.pprint(donations_dict)
                select = int(input('Please enter \'1\' through \'{}\' '
                                   'to select a donation to update: '
                                   .format(len(donations))))
                if select not in donations_dict.keys():
                    raise ValueError
            except ValueError:
                print('Oops, invalid selection...')
                return
            else:
                print('Updating {}\'s donation of {}.'
                      .format(donor, donations[select - 1]))
                self.find_donor_donation_update(donor, donations[select - 1])
                return

    def get_donor_operation(self, operation=None):
        if not self.donorCollection.donor_names:
            print('The list of donors is empty.')
            return

        instruction = 'Please enter a name '\
                      'or type \'list\' to see donors:\n'

        name_input = input(instruction)

        if name_input == 'list':
            print("\n".join(self.donorCollection.donor_names))
            self.get_donor_operation(operation)
        elif name_input in self.donorCollection.donor_names:
            if operation == 'update_donor':
                self.find_donor_donation_update(name_input)
            elif operation == 'set_donation':
                self.add_donation(name_input)
            elif operation == 'update_donation':
                self.select_donation(name_input)
        else:
            print('Donor not found.')
            self.get_donor_operation(operation)

    def apply_selection(self, selection):
        arg_dict = {
            '1': self.set_donor,
            '2': self.get_donor_operation,
            '3': self.get_donor_operation,
            '4': self.get_donor_operation,
            '5': self.donorCollection.generate_table,
            '6': self.donorCollection.generate_letters,
            '7': quit
        }
        try:
            if not arg_dict.get(selection):
                raise KeyError
            elif selection == '2':
                arg_dict.get(selection)('update_donor')
            elif selection == '3':
                arg_dict.get(selection)('set_donation')
            elif selection == '4':
                arg_dict.get(selection)('update_donation')
            else:
                arg_dict.get(selection)()
        except KeyError:
            print('Oops, invalid selection.')

    def get_selection(self):
        options = 'Please select from the menu:\n'\
                  '1) add new donor\n'\
                  '2) update donor\n'\
                  '3) add new donation\n'\
                  '4) update donation\n'\
                  '5) create a report\n'\
                  '6) send letters to everyone\n'\
                  '7) quit\n'
        while True:
            selection = input(options)
            self.apply_selection(selection)
            if selection == '3':
                self.get_donor_operation()


def main():
    dl = DonorList()
    cli = DonorCli(dl)
    cli.get_selection()


if __name__ == "__main__":
    main()
