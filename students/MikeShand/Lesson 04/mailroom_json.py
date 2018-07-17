#!/usr/bin/env python3
import sys
from collections import defaultdict
import json
import json_save.json_save_dec as js


@js.json_save
class Donor:

    name = js.String()
    donations = js.List()

    def __init__(self, name, donations=None):

        self.name = name
        if donations is None:
            self.donations = []
        else:
            self.donations = donations

    def add_donation(self, amount):
        try:
            self.donations.append(int(amount))
        except ValueError:
            print("Please enter a number!")

    def number_donations(self):
        return len(self.donations)

    def total_donation(self):
        try:
            return sum(self.donations)
        except TypeError:
            return self.donations

    def avg_donation(self):
        try:
            return self.total_donation() / self.number_donations()
        except TypeError:
            return self.donations


@js.json_save
class Roster:

    donor_list = js.List()

    def __init__(self, donors):
        self.donor_list = donors

    def donor_roster(self):
        donor_names = []
        for donor in self.donor_list:
            donor_names.append(donor.name)
        return donor_names

    def save_roster(self):
        data = self.to_json_compat()
        data = json.dumps(data)
        with open('roster.json', 'w') as data_file:
            data_file.write(data)

    def load_roster(self):
        global mailroom
        with open('roster.json', 'r') as roster_json:
            roster = roster_json.read()
            roster_dict = json.loads(roster)
            mailroom = self.from_json_dict(roster_dict)
        return mailroom

    def thank_you(self, new_donor, amount):
        if new_donor in self.donor_list:
            try:
                donor_list[new_donor].add_donation(amount)
                print('Thank you {} for your generous donation of ${:.2f}'.format(new_donor, amount))
            except ValueError:
                print("Please enter a round number!")
        else:
            new_donor_object = Donor(new_donor, [amount])
            self.donor_list.append(new_donor_object)
            print('Thank you {} for your generous donation of ${:.2f}'.format(new_donor, amount))

    def donor_report(self):

        """Outputs a string that is a table of the donors and contributions"""

        print('Here is a list of donors and contributions')
        report = []
        report.append('|{:<20}|{:<20}|{:<20}|{:<20}|'.format('Name', 'Total', 'Donations', 'Average'))
        for donor in self.donor_list:
            report.append('|{:<20}|{:>20}|{:>20}|{:>20}|'.format(donor.name, donor.total_donation(), donor.number_donations(), donor.avg_donation()))
        return '\n'.join(report)

    def print_donors(self):
        print(self.donor_report())


    def batch_file(self):

        """Creates a text file with a thank you message for each of the donors in the dictionary"""

        for donor_data in self.donor_list:
            filename = donor_data.name.replace(" ", "_") + ".txt"
            total_donation = donor_data.total_donation()
            letter = ('Thank you {} for you generous contributions totalling {:.2f}!'.format(donor_data.name, total_donation))
            with open(filename, 'w') as letter_file:
                letter_file.write(letter)
            print(f"{donor_data.name}'s letter has been saved to " + filename)

    def challenge(self, factor, lo=None, hi=None):

        challenge = []

        if lo and hi:
            if lo > hi:
                raise ValueError('Max must be greater than min')
            else:
                for donor in self.donor_list:
                    challenge.append(
                        list(map(lambda x: x * factor, filter(lambda y: min <= y <= max, donor.donations))))
                    return challenge

        elif min:
            challenge.append(list(map(lambda x: x * factor, filter(lambda y: y >= min, donor.donations))))
            return challenge

        elif max:
            challenge.append(list(map(lambda x: x * factor, filter(lambda y: y <= max, donor.donations))))
            return challenge

        else:
            challenge.append(list(map(lambda x: x * factor, donor.donations)))
            return challenge

    def make_roster(self, factor, hi=None, lo=None):
        donor_names = self.donor_roster()
        philanthropist_donation = self.challenge(factor, hi, lo)
        donors_new = list(zip(donor_names, philanthropist_donation))
        for name in donors_new:
            new_list = []
            name = Donor(name[0], name[1])
            new_list.append(name)
        return Roster(new_list)

    def projection(self, factor, lo=None, hi=None):
        return sum(list(sum(self.challenge(factor, lo, hi), [])))


def print_donors():
    mailroom.print_donors()


def send_thankyou():
    mailroom.batch_file()


def save_new_roster():
    mailroom.save_roster()


def add_philanthropist():
    print('Please enter the minimum and maximum values of the donations you wish to match:')
    min = float(input('Minimum >'))
    max = float(input('Maximum >'))
    factor = float(input('Please enter the factor you wish to multiply these donations by'))
    big_money = mailroom.make_roster(factor, min, max)
    return big_money.donor_report()


def projection():
    print('Please enter the minimum and maximum values of the donations you wish to match:')
    min = float(input('Minimum >'))
    max = float(input('Maximum >'))
    factor = float(input('Please enter the factor you wish to multiply these donations by'))
    fake_money = mailroom.projection(factor, min, max)
    print(f"{fake_money} is the total donation projected")


def create_thank_you():
    print('Please enter the donor name\n (Type "list" for a list of current donor names)\n '
          'Press "q" to return to console')
    new_donor = input(':')
    if new_donor.lower() == 'list':
        print(mailroom.donor_roster())
    elif new_donor.lower() == 'q':
        quit_console()
    else:
        amount = float(input('Please enter the donation amount:'))
        mailroom.thank_you(new_donor, amount)


def menu_selection(prompt, dispatch_dict):
    '''Creates a menu that accepts user input and then selects a function based on that input'''
    while True:
        try:
            response = input(prompt)
            dispatch_dict[response]()
        except KeyError:
            print('Please enter a valid selection from the menu')



def quit_console():
    sys.exit("Exiting the program")


if __name__ == '__main__':

    Andy = Donor('Andy', [10.00])
    Bill = Donor('Bill', [15.00, 25.00])
    Chuck = Donor('Chuck', [20.00, 30.00, 40.00])
    mailroom = Roster([Andy, Bill, Chuck])


    def load_new_roster():
        global mailroom
        mailroom = mailroom.load_roster()
        mailroom.print_donors()


    console_prompt = ("\nWelcome to the Donor Tracking System\n"
                      "Please press a number to make a selection\n"
                      "1.) Send a thank you note\n"
                      "2.) Create a Report\n"
                      "3.) Send letters to everyone!\n"
                      "4.) Match donations!\n"
                      "5.) Project a matching donation amount\n"
                      "6.) Save the roster\n"
                      "7.) Load the roster\n"  
                      "8.) Quit(press 'q')\n")

    console_dict = {'1': create_thank_you,
                    '2': print_donors,
                    '3': send_thankyou,
                    '4': add_philanthropist,
                    '5': projection,
                    '6': save_new_roster,
                    '7': load_new_roster,
                    '8': quit_console,
                    'q': quit_console,
                    'Q': quit_console}

    # mailroom = load_new_roster()
    menu_selection(console_prompt, console_dict)


# def challenge(factor):
#    challenge = []
#    for donor in mailroom.donor_list:
#        challenge.append(donor.total_donation())
#    return list(map(lambda x: x* factor, challenge))




# def make_roster(factor, min = None, max = None):
#    donor_names = mailroom.donor_roster()
#    philanthropist_donation = challenge(factor, min, max)
#    donors_new = list(zip(donor_names, philanthropist_donation))
#    for name in donors_new:
#        new_list = []
#        name = Donor(name[0], name[1])
#        new_list.append(name)
#    return Roster(new_list)
