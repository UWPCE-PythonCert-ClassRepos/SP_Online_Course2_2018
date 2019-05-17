import os
import donors_sql as d
import create_mr_tables as new_database
import logging
import utilities
import login_database
# from peewee import *
mail = d.Group('mailroom.db')
individual = d.Individual('mailroom.db')

logging.basicConfig(level=logging.WARNING)
logger = logging.getLogger(__name__)


def create_database():

    file_name = input('\nWhat would you like to name your new database?\n'
                      'e - to exit\n')
    if file_name == 'e':
        return

    if os.path.exists(file_name):
        logging.info('This database already exists.')
        return

        # cwd = os.getcwd()
    file_name = file_name + '.db'
    logger.info(f'Creating new database {file_name}.')
    new_database.database.init(file_name)
    database = new_database.database
    database.connect()
    logger.info('Creating Modules in database')
    database.create_tables([new_database.Donor, new_database.Donations])
    database.close()
    logger.info('Database has been created and is closed.')


def delete_database():
    cur_dir = os.getcwd()
    logger.debug(f'Current Directory is {cur_dir}')
    file_list = os.listdir(cur_dir)
    logger.debug(f'File list is {file_list}')
    db_file = []
    for file in file_list:
        logger.debug(f'Print file in file_list {file}')
        if file.endswith('.db'):
            db_file.append(file)
            logger.debug(f'Print db_file,{db_file}')
    if db_file is not None:
        print(f"The following databases exist in current working directory,\n")
        for file in db_file:
            print(f"{file}\n")
    if len(db_file) == 0:
        print('No database exists. Please create a database.')
        return
    file_name = input('\nWhat database do you want to delete? Include ".db" \n'
                      'e - to exit\n')
    if file_name == 'e':
        return
    if os.path.exists(file_name):
        logging.info('Trying to delete the database.')
        os.remove(file_name)
        logger.info(f'Database is {file_name} has been deleted.')


def more_choices():
    while True:
        name = input('\nChoose an Option: \n'
                     'e - to exit\n'
                     'list - To see a list of names, or\n'
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
                d.Individual.add_donation(name, float(amount))
                print(individual.thank_you(name, float(amount)))


def print_report():
    print(mail.report())


def letters_for_all():
    path_letters = os.getcwd()
    print(f"You chose to send letters for everyone. "
          f"The letters have been completed and you "
          f"can find them here: {path_letters}")
    mail.letters()


def delete_donor():
    while True:
        name = input('\nWhich donor would you like to delete? \n'
                     'e - to exit\n'
                     'list To see a list of names, or\n'
                     'Type the name of the donor to delete.>>')
        if name == 'e':
            return
        if name == 'list':
            mail.print_donors()
        else:
            print('\n''Ok, you want to delete {}, '
                  'lets see what we can do.'.format(name))

            if mail.search(name) is None:
                print('The name you entered is not in the database.')
                return
            else:
                individual.delete_donor(name)


def wrong_choice():
    pass


def quit_program():
    exit()


if __name__ == '__main__':
    log = utilities.configure_logger('default', '../logs/mailroom_dev.log')

    switch_dict = {'1': more_choices,
                   '2': print_report,
                   '3': letters_for_all,
                   '4': delete_donor,
                   '5': create_database,
                   '6': delete_database,
                   '7': quit_program}
    while True:
        response = input(
            '\nChoose an Action:\n'
            '1 - Send a Thank You\n'
            '2 - Create a Report\n'
            '3 - Send letters to everyone\n'
            '4 - Delete a Donor\n'
            '5 - Create a new database\n'
            '6 - Delete a database\n'
            '7 - Quit\n'
            '>>')

        switch_dict.get(response, wrong_choice)()
