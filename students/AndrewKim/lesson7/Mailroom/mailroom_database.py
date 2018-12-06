# -*- coding: utf-8 -*-

import logging

from sys import exit
from create_mailroom import *
from peewee import *


class Main:
    def __init__(self):
        self.prompt = {1: 'Send A Thank You',
                       2: 'Create a Report',
                       3: 'Send letters to everyone',
                       4: 'Delete a Donor',
                       5: 'Exit'}

    def user_input(self):
        print("\nEnter the number from menu: ")
        return {(print(str(k) + ':', v)) for k, v in self.prompt.items()}

    def working_system(self):
        while True:
            temp = input()
            try:
                if int(temp) in range(1, 5):
                    if int(temp) == 1:
                        print('\n"Enter the donor name or list: "')
                        temp2 = input()
                        #for list
                        if temp2 == 'list':
                            query = (Donor.select(Donor,
                                                  fn.COUNT(Donor_Amount.id)
                                                  .alias('donation_count'))
                                     .join(Donor_Amount,
                                     JOIN.LEFT_OUTER).group_by(Donor)
                                     .order_by(Donor.donor_name))
                            for i in query:
                                print(i.donor_name)
                            Main()
                            self.user_input()
                            self.working_system()
                        #for new or existing donor
                        else:
                            donation_amount = input('Enter the donor_amount: ')
                            try:
                                new_donor_created = Donor.create(donor_name = temp2)
                                Donor_Amount.create(new_donor = new_donor_created,
                                                donor_amount=float(donation_amount))
                                self.thank_you(temp2, donation_amount)
                            except IntegrityError:
                                new_donor_created = Donor_Amount.create(new_donor=temp2,
                                                                donor_amount=float
                                                                (donation_amount))
                                new_donor_created.save()
                                Main()
                                self.user_input()
                                self.working_system()

                    elif int(temp) == 2:
                        self.create_report()
                    elif int(temp) == 3:
                        self.send_thank_you_all()
                    elif int(temp) == 4:
                        self.delete_donor()
                elif int(temp) == 5:
                    raise SystemExit()
            except ValueError:
                print("\nEnter the number from menu: ")

    def thank_you(self, donor, donor_amount):
        thankyou = "Dear {}, thank you for the donation of {}".format(donor, donor_amount)
        with open('{}.txt'.format(donor.replace(' ', '_')), 'w') as file:
            file.write(thankyou)

    def create_report(self):
        print("Donor Name       ||  Total Donation ||  Number of Gifts || Gift Average")
        print('----------------------------------------------------------------------------')
        report = (Donor.select(Donor, fn.Sum(Donor_Amount.donor_amount).alias('sum'),
                  fn.Count(Donor_Amount.id).alias('count'),
                           fn.AVG(Donor_Amount.donor_amount).alias('avg'))
                  .join(Donor_Amount).group_by(Donor)
                  .order_by(fn.Sum(Donor_Amount.donor_amount).desc()))

        for index in report:
            print('{:<18} {:>12.02f} {:>13} {:>24.02f}'.format(index.donor_name, index.sum, index.count, index.avg))

        Main()
        self.user_input()
        self.working_system()

    def send_thank_you_all(self):

        everyone = (Donor.select(Donor, fn.Sum(Donor_Amount.donor_amount).alias('sum'),fn.Count(Donor_Amount.id).alias('count'),fn.AVG(Donor_Amount.donor_amount).alias('avg'))
                  .join(Donor_Amount).group_by(Donor).order_by(fn.Sum(Donor_Amount.donor_amount).desc()))
                  
        letter = "Dear {}, thank you for the donation of {}"

        for index in everyone:
            with open('{}.txt'.format(index.donor_name.replace(' ', '_')), 'w') as f:
                f.write(letter.format(index.donor_name, index.sum))

        Main()
        self.user_input()
        self.working_system()

    def delete_donor(self):
        print('\nEnter the donor name or list: ')
        temp = input()
        if temp == 'list':
            lists = (Donor.select(Donor, fn.COUNT(Donor_Amount.id)
                     .alias('donation_count'))
                     .join(Donor_Amount, JOIN.LEFT_OUTER).group_by(Donor)
                     .order_by(Donor.donor_name))
            for index in lists:
                print(index.donor_name)
            Main()
            self.user_input()
            self.working_system()
        else:
            donor = Donor.get(Donor.donor_name == temp)
            donor.delete_instance()
            print(f'{temp} is deleted')
            Main()
            self.user_input()
            self.working_system()


if __name__ == '__main__':
    create_tables()
    system = Main()
    system.user_input()
    system.working_system()
