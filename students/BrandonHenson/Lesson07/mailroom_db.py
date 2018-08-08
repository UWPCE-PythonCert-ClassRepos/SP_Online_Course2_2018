# -*- coding: utf-8 -*-

import logging

from sys import exit
from mailroom_model import *
from peewee import *


class Main:
    def __init__(self):
        self.prompt = {1: 'Send A Thank You To New Or Exsisting Donor',
                       2: 'Create a Report',
                       3: 'Send letters to everyone',
                       4: 'Delete a Donor',
                       5: 'Exit'}

    def menu_selection(self):
        print("\nPick from the listed options.")
        return {(print(str(k) + ':', v)) for k, v in self.prompt.items()}

    def selection(self):
        while True:
            input1 = input()
            try:
                if int(input1) in range(1, 5):
                    if int(input1) == 1:
                        print('\n"Enter a name or list"')
                        input2 = input()
                        if input2 == 'list':
                            query = (Donor.select(Donor,
                                                  fn.COUNT(Donation.id)
                                                  .alias('donation_count'))
                                     .join(Donation,
                                     JOIN.LEFT_OUTER).group_by(Donor)
                                     .order_by(Donor.username))
                            for i in query:
                                print(i.username)
                            Main()
                            self.menu_selection()
                            self.selection()
                        else:
                            input3 = input('Donation amount: ')
                            try:
                                new_user = Donor.create(username=input2)
                                Donation.create(user=new_user,
                                                donation=float(input3))
                                self.thank_you(input2, input3)
                            except IntegrityError:
                                update_record = Donation.create(user=input2,
                                                                donation=float
                                                                (input3))
                                update_record.save()
                                Main()
                                self.menu_selection()
                                self.selection()

                    elif int(input1) == 2:
                        self.create_report()
                    elif int(input1) == 3:
                        self.thank_everyone()
                    elif int(input1) == 4:
                        self.delete_user()
                elif int(input1) == 5:
                    raise SystemExit()
            except ValueError:
                print("\nPick from the listed options.")

    def thank_you(self, name, amount):
        letter = "Dear {},\nThank you for your generous donation in the amount \
of ${}; \nThe money will be put to good use.\n\nSincerely, \n                -\
The Team".format(name, amount)
        with open('{}.txt'.format(name.lower().
                                  replace(' ', '_')), 'w') as f:
            f.write(letter)

    def create_report(self):
        print("Donor Name       |  Total Given |  Num Gifts | Average Gift")
        print('-----------------------------------------------------------')
        report = (Donor.select(Donor, fn.Sum(Donation.donation).alias('sum'),
                  fn.Count(Donation.id).alias('count'),
                           fn.AVG(Donation.donation).alias('avg'))
                  .join(Donation).group_by(Donor)
                  .order_by(fn.Sum(Donation.donation).desc()))

        for i in report:
            print('{:<18} {:>12.02f} {:>10} {:>12.02f}'
                  .format(i.username, i.sum, i.count, i.avg))

        Main()
        self.menu_selection()
        self.selection()

    def thank_everyone(self):

        notes = 'Dear {},\n\nThank you for your generous donations totaling \
${}. The money will be put to good use.\n\nSincerely,\n\t\t-The Team'

        report = (Donor.select(Donor, fn.Sum(Donation.donation).alias('sum'),
                  fn.Count(Donation.id).alias('count'),
                  fn.AVG(Donation.donation).alias('avg'))
                  .join(Donation).group_by(Donor)
                  .order_by(fn.Sum(Donation.donation).desc()))

        for i in report:
            with open('{}.txt'.format(i.username.lower()
                      .replace(' ', '_')), 'w') as f:
                f.write(notes.format(i.username, i.sum))

        Main()
        self.menu_selection()
        self.selection()

    def delete_user(self):
        print('\nEnter a name or list')
        input2 = input()
        if input2 == 'list':
            names = (Donor.select(Donor, fn.COUNT(Donation.id)
                     .alias('donation_count'))
                     .join(Donation, JOIN.LEFT_OUTER).group_by(Donor)
                     .order_by(Donor.username))
            for i in names:
                print(i.username)
            Main()
            self.menu_selection()
            self.selection()
        else:
            user = Donor.get(Donor.username == input2)
            user.delete_instance()
            print(f'Deleted {input2}')
            Main()
            self.menu_selection()
            self.selection()


if __name__ == '__main__':
    create_tables()
    ex = Main()
    ex.menu_selection()
    ex.selection()
