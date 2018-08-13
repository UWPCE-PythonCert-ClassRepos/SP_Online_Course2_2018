#Natalie Rodriguez
#August 10, 2018
#Lesson 04: Mailroom json
#Modify mailroom to be able to load and save classes as JSON.


#!/usr/bin/env python3
import sys
from collections import defaultdict
import json
import json_save.json_save_dec as js


@js.json_save
class DonorHistory:

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
            print("Please enter a donation amount.")

    def number_donations(self):
        return len(self.donations)

    def total_donation(self):
        try:
            return sum(self.donations)
        except TypeError:
            return self.donations

    def donation_avg(self):
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
                print("Please enter a valid amount.")
        else:
            new_donor_object = DonorHistory(new_donor, [amount])
            self.donor_list.append(new_donor_object)
            print('Thank you {} for your generous donation of ${:.2f}'.format(new_donor, amount))

    def donor_report(self):

        print('Here is a list of donors and the amount donated.')
        report = []
        report.append('|{:<20}|{:<20}|{:<20}|{:<20}|'.format('Name', 'Total Donation', 'No. of Donations', 'Average Donation'))
        for donor in self.donor_list:
            report.append('|{:<20}|{:>20}|{:>20}|{:>20}|'.format(donor.name, donor.total_donation(), donor.number_donations(), donor.donation_avg()))
        return '\n'.join(report)

    def print_donors(self):
        print(self.donor_report())


    def write_files(self):

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
                raise ValueError('Maximum must be greater than the minimum amount.')
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
            name = DonorHistory(name[0], name[1])
            new_list.append(name)
        return Roster(new_list)

    def donation_projected(self, factor, lo=None, hi=None):
        return sum(list(sum(self.challenge(factor, lo, hi), [])))


def print_donors():
    mailroom.print_donors()


def send_thankyou():
    mailroom.write_files()


def save_new_roster():
    mailroom.save_roster()


def add_phil():
    print('Please enter the minimum and maximum amounts of the donations you would like to match:')
    min = float(input('Minimum:'))
    max = float(input('Maximum:'))
    factor = float(input('Please enter the factor by which you want to multiply your donation:'))
    big_money = mailroom.make_roster(factor, min, max)
    return big_money.donor_report()


def projected():
    print('Please enter the minimum and maximum values of the donations you wish to match:')
    min = float(input('Minimum:'))
    max = float(input('Maximum:'))
    factor = float(input('Please enter the factor by which you want to multiply your donation:'))
    fake_money = mailroom.donation_projected(factor, min, max)
    print(f"{fake_money} is the amount of the projected donation.")


def create_thank_you():
    print('Please enter the donor name or enter "list" for a list of current donors.)\n '
          'Enter "quit" to return to the Donor Dashboard.')
    new_donor = input(':')
    if new_donor.lower() == 'list':
        print(mailroom.donor_roster())
    elif new_donor.lower() == 'q':
        quit_dashboard()
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
            print('Please enter a selection from the dashboard.')



def quit_dashboard():
    sys.exit("Exiting the Nature Conservancy Donor Dashboard. Goodbye!")


if __name__ == '__main__':

    Luke = DonorHistory('Luke Rodriguez', [5512.75, 3250.50, 42.50])
    River = DonorHistory('River Tails', [63.00, 1200.00, 300.00, 450.00, 4000.00])
    Virgil = DonorHistory('Virgil Ferdinand', [350.00, 5000.00])
    Jokib = DonorHistory('Joseph Kibson', [3498.00, 5.50])
    mailroom = Roster([Luke, River, Virgil, Jokib])


    def load_new_roster():
        global mailroom
        mailroom = mailroom.load_roster()
        mailroom.print_donors()


    donor_dashboard = ("\nWelcome to the Nature Conservancy Donor Dashboard!\n"
                      "Please enter a number to make a selection.\n"
                      "\n1.) Send a thank you note.\n"
                      "2.) Create a Report.\n"
                      "3.) Send thank you notes to all donors.\n"
                      "4.) Match an existing donation.\n"
                      "5.) Create a projected donation amount.\n"
                      "6.) Save the roster.\n"
                      "7.) Load the roster.\n"  
                      "8.) Quit(enter 'quit')\n")

    dashboard_dict = {'1': create_thank_you,
                    '2': print_donors,
                    '3': send_thankyou,
                    '4': add_phil,
                    '5': projected,
                    '6': save_new_roster,
                    '7': load_new_roster,
                    '8': quit_dashboard,
                    'quit': quit_dashboard,
                    'Quit': quit_dashboard}

    # mailroom = load_new_roster()
    menu_selection(donor_dashboard, dashboard_dict)


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