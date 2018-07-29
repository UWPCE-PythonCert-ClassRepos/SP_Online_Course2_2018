#!/usr/bin/env python3
import sys


donors_dct = {'Gates': {'title': 'Mr.', 'donations': 150000,
                        'num_donations': 3},
              'Brin': {'title': 'Mr.', 'donations': 150000,
                       'num_donations': 3},
              'Cerf': {'title': 'Mr.', 'donations': 50000,
                       'num_donations': 2},
              'Musk': {'title': 'Mr.', 'donations': 100000,
                       'num_donations': 1},
              'Berners-Lee': {'title': 'Mr.', 'donations':
                              50000, 'num_donations': 2},
              'Wojcicki': {'title': 'Ms.', 'donations': 125000,
                           'num_donations': 1},
              'Avey': {'title': 'Ms.', 'donations': 200000,
                       'num_donations': 2}}


class Donor:
    """creates objects for individual donors"""
    def __init__(self, title, last_name, donation):
        self.title = title
        self.last_name = last_name
        self.donations = [donation]

    @property
    def donor(self):
        """getter for individual donor"""
        return {self.last_name: {'title': self.title, 'donations':
                sum(self.donations), 'num_donations': len(self.donations)}}

    @property
    def donation(self):
        """getter for most recent donation amount"""
        return self.donations[-1]

    @donation.setter
    def donation(self, donation):
        """enables addition of new donation"""
        self.donations.append(donation)


class DonorGroup:
    """creates donor group dictionary objs for multiple donor dictionaries"""
    def __init__(self, donors):
        self.donors = donors

    def donorgroup(self):
        """returns list of donors in group"""
        print(sorted([donor for donor in self.donors]))

    def add_donor_to_donorgroup(self):
        q_title = input('Enter donor title: ')
        q_lastname = input('Enter last name: ')
        q_donation = int(input('Donation amount (USD)?: '))
        self.new_donor = Donor(q_title, q_lastname, q_donation)
        self.donors = dict(**self.donors, **self.new_donor.donor)
        self.donorgroup_new_donor = self.new_donor
        return self.donorgroup

    def withdraw(self, title, last_name):
        """given donor last name as string, removes donor from self.donors"""
        for donor in self.donors[:]:
            for key, val in donor.items():
                if key == last_name and val['title'] == title:
                    self.donors.remove(donor)

    def get_report(self):
        print()
        psv = ['Donor Name', '| Total Given', '| Num Gifts',
               '| Average Gift']
        print('{:<15}{:>12}{:>12}{:>12}'.format(psv[0], psv[1],
              psv[2], psv[3]))
        for i in range(55):
            print('-', end='')
        print()
        new_list = [[self.donors[donor]['donations'], donor,
                     self.donors[donor]['num_donations']] for
                    donor in self.donors]
        new_list.sort(reverse=True)
        for donor_list in new_list:
            formatted_donor = ('{:<15}'.format(donor_list[1])
                               + '{}{:>10}'.format(' $', donor_list[0])
                               + '{:>13}'.format(donor_list[2])
                               + '{}{:>11}'.format(' $',
                               donor_list[0] // donor_list[2]))
            print(formatted_donor)

    def save_data(self):
        with open('test.txt', 'w') as outfile:
            outfile.write('This is current DonorGroup data:\n' +
                          str(self.donorgroup))


class UI:
    def __init__(self):
        self.donors = DonorGroup(donors_dct)
        self.menu_dct = {'1': self.donors.donorgroup,
                         '2': self.donors.get_report,
                         '3': self.donors.add_donor_to_donorgroup,
                         'q': sys.exit}
        # self.new_donor = self.donors.donorgroup_new_donor
        self.main_text = '\n'.join((
                                    'Choose from the following:',
                                    '"1" - Get a List of Donors,',
                                    '"2" - Create a Report,',
                                    '"3" - Add a Donor, or',
                                    '"q" to Quit: '
                                  ))
        while True:
            print('\nMain Menu:')
            response = input(self.main_text)
            print()
            try:
                if response == 'q':
                    print('Program execution completed.')
                # elif response == '1':
                #     print(self.donors.donorgroup)
                # if response != '1':
                    # if response == '3':
                    # q_title = input('Enter donor title: ')
                    # q_lastname = input('Enter last name: ')
                    # q_donation = int(input('Donation amount (USD)?: '))
                    # self.donors.donorgroup_new_donor = Donor(q_title,
                    #                                          q_lastname,
                    #                                          q_donation)
                if type(self.menu_dct[response]) != list:
                    self.menu_dct[response]()
                else:
                    print(self.menu_dct[response])

            except KeyError:
                print('\nThat selection is invalid. Please try again.')


interaction_instance = UI()
