import logging
from donor_model import *
import sys


import logging
from donor_model import *



database.connect()
database.execute_sql('PRAGMA foreign_keys = ON;')
database = SqliteDatabase('donors.db')

def list_donors():
    a =[]
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')

        for donor in Donorinfo.select():
            a.append(donor.donor_name)
        return a

    except Exception as e:
        logger.info(e)

    finally:
        database.close()



def add_donor_in_data(name, amount):
    if name in list_donors():
        try:
            new_donation = Donationinfo.create(
                donation_amount = amount,
                donor_name = name
            )
            new_donation.save()

            adonor = Donorinfo.get(Donorinfo.donor_name == name)
            adonor.sum_donations += amount
            adonor.number_donations +=1
            adonor.avg_donations = adonor.sum_donations/adonor.number_donations
            adonor.save()

        except Exception as e:
            logger.info(e)

        finally:
            database.close()

    else:
        donors={name:[amount]}
        populate_donors(donors) #a function in donor_model.py


class Collection:

    def all_donor(self):
        print(list_donors())

    def send_a_thank_you(self):
        print('\n')
        print(self.all_donor())
        donor_name =input('\n\nPlease input the name or the donator > ')
        donation = float(input('\n\nThank you for donation , please type '
                    'the money you want to donate > '))
        #while not donation.isdigit():
        #    donation = input('\n\nPlease type number only > ')

        add_donor_in_data(donor_name,donation)
        menu_selection(main_prompt,main_dispatch)


    def creat_a_report(self):
        print('{:<20}'.format('Donor Name')+'| '+
              '{:<15}'.format('Total Given')+'| '+'{:<15}'.format('Num Gifts')+'| '+'{:<15}'.format('Average Gift'))
        print('='*68)
        for saved_donor in Donorinfo:

            print(f'{saved_donor.donor_name:<20}'+ f'$ {saved_donor.sum_donations :<16}'
            + f'{saved_donor.number_donations:<16}'
            + f'$ {saved_donor.avg_donations :<16}')


    def send_letters_to_everyone(self):
        for saved_donor in Donorinfo:
            name = saved_donor.donor_name
            amount =  saved_donor.avg_donations
            t_amount = saved_donor.sum_donations
            with open(name+'.txt', 'w') as wf, open("template.txt", 'r') as rf:
                for line in rf:
                    wf.write(line.replace('{name}', name).replace('{amount:.2f}',str(amount)).replace('{t_amount:.2f}',str(t_amount)))
        print('\n\nCreat report to everyone successfuly!')


    def delete_a_donation(self):

        for donation in Donationinfo:
            logger.info(f'{donation.donor_name} donated {donation.donation_amount}')

        print(' \n\ninput the name and the amount you want to delete')

        name= input('\n\nPlease input the name you want to delete ')
        amount = float(input('\n\ntransaction you want to delete '))
        adonation = Donationinfo.get(Donationinfo.donor_name == name, donation_amount = amount)
        adonation.delete_instance()
        adonor = Donorinfo.get(Donorinfo.donor_name == name)
        adonor.sum_donations -= amount
        adonor.number_donations -=1
        if adonor.number_donations == 0:
            adonor.avg_donations = 0
        else:
            adonor.avg_donations = adonor.sum_donations/adonor.number_donations
        adonor.save()



def menu_selection(prompt, dispatch_dict):
    while True:
        response = input(prompt)
        try:
            if dispatch_dict[response]() == 'back to upper menu':
                break
        except KeyError:
            print('\nError: Please input right instruction')

def main_menue():
    menu_selection(main_prompt,main_dispatch)

def sub1_menu():
    menu_selection(sub1_prompt,sub1_dispatch)

def go_back():
    return 'back to upper menu'

main_prompt = ('\n\nPlease select a action: \n1 Send a Thank You!'
               ' \n2 Create a Report  \n3 Send letters to everyone \n'
               '4 Delete a transaction \n5 Exit \n\n  >')
sub1_prompt = ('\n\nType "list" to show a list of the donor names, \n'
                'Or type "back" to Back\n')

main_dispatch ={'1':sub1_menu,'2':Collection().creat_a_report,'3':Collection().send_letters_to_everyone,
                '4':Collection().delete_a_donation, '5':sys.exit}
sub1_dispatch ={'list':Collection().send_a_thank_you, 'back':go_back}

def main():
    menu_selection(main_prompt,main_dispatch)

if __name__ == "__main__":
    main()
