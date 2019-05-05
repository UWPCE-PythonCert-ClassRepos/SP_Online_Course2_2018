import os
import donors_sql as d
import create_mr_tables as new_database
import logging
from peewee import *

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
mail = d.Group(d.Individual('Shane', [200]))


if os.path.exists("demofile.txt"):
  os.remove("demofile.txt")
else:
  print("The file does not exist")


def create_database():

    file_name = input('\nAre you sure you want to delete?\n'
                            'e - to exit\n')
    if file_name == 'e':
        return
    else:
        if os.path.exists("mailroom.db"):
            logging.info('Trying to delete the database.')
            os.remove("mailroom.db")

        cwd = os.getcwd()
        os.path.join(cwd, 'mailroom.db')
        logger.info('Connecting to mailroom.db database.')
        database = SqliteDatabase('mailroom.db')
        database.connect()
        logger.info('Creating Modules in database')
        database.create_tables([new_database.Donor, new_database.Donations])
        database.close()
        logger.info('Database is closed.')


def more_choices():
    while True:
        name = input('\nChoose an Option: \n'
                     'e - to exit\n'
                     'list To see a list of names, or\n'
                     'Type a name to start your thank you letter >>')
        if name == 'e':
            return
        if name == 'list':
            mail.print_donors()
        else:
            print('\n''Ok, you want to write a letter for {}, '
                  'lets see what we can do.'.format(name))

            if mail.search(name) is None:
                yes_no = input('The name you entered is not in the database.'
                               'Would you like to add this name? y or n >>')
                if yes_no == 'n':
                    return

            amount = input('\n''What is the donation amount? or '
                           '\'e\' to exit >')
            if amount == 'e':
                return
            try:
                if int(amount) <= 0:
                    print('\nYou entered an invalid amount!!\n')
                    return
            except ValueError:
                print('\nYou entered an invalid amount!!\n')
                return ValueError
            else:
                mail.add(name, float(amount))
                donor_obj = mail._donor_raw[name]
                print(donor_obj.thank_you)


def print_report():
    print(mail.report())


def letters_for_all():
    path_letters = os.getcwd()
    print(f"You chose to send letters for everyone. "
          f"The letters have been completed and you "
          f"can find them here: {path_letters}")
    mail.letters()


def delete_donor():
    pass


def wrong_choice():
    pass


def quit_program():
    exit()


if __name__ == '__main__':

    switch_dict = {'1': more_choices,
                   '2': print_report,
                   '3': letters_for_all,
                   '4': delete_donor,
                   '5': create_database,
                   '6': quit_program}
    while True:
        response = input(
            '\nChoose an Action:\n'
            '1 - Send a Thank You\n'
            '2 - Create a Report\n'
            '3 - Send letters to everyone\n'
            '4 - Delete a Donor\n'
            '5 - Create a new database\n'
            '6 - Quit\n'
            '>>')

        switch_dict.get(response, wrong_choice)()
