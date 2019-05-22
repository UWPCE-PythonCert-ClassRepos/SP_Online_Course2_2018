import os
import donors_neo4j as d
import utilities
import login_database
import Load_Tables
log = utilities.configure_logger('default', '../logs/mailroom_ne04j.log')


def load_mailroom():
    driver = login_database.login_neo4j_cloud()
    log.debug('Step 1: We are going to use a neo4j database"')

    file_name = input('\nYou are working with a database'
                      'on Neo4j.\n'
                      'Would you like to delete existing people and start over?'
                      'e - to exit\n')
    if file_name == 'e':
        return

    # Delete 'people' from ne04j database and start over with default people.
    Load_Tables.load_neo4j(driver)

    # load the Redis database
    r = login_database.login_redis_cloud()
    Load_Tables.populate_redis(r)
    log.debug('Database has been created and is closed.')


def more_choices():
    driver = login_database.login_neo4j_cloud()
    mail = d.Group(driver)
    individual = d.Individual(driver)
    r = login_database.login_redis_cloud()

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
                               'Would you like to add this name? y or n >>\n')
                if yes_no == 'n':
                    return

                if yes_no == 'y':
                    last_name = input(f"What is {name}'s last name?\n")
                    email = input(f"What is {name}'s email?\n")
                    telephone = input(f"What is {name}'s telephone #?\n")
                    d.Individual.redis_add_new(r,
                                               name,
                                               last_name,
                                               telephone,
                                               email)
                else:
                    return
            print(f"First confirm {name}'s information")
            individual.donor_verification(r, name)
            confirm_info = input("Does the donor info look ok? y or n >>\n")
            if confirm_info == 'n':
                update_redis(r, name)
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
                individual.add_donation(name, float(amount))
                print(individual.thank_you(name, float(amount)))


def print_report():
    driver = login_database.login_neo4j_cloud()
    mail = d.Group(driver)
    print(mail.report())


def letters_for_all():
    driver = login_database.login_neo4j_cloud()
    mail = d.Group(driver)
    path_letters = os.getcwd()
    print(f"You chose to send letters for everyone. "
          f"The letters have been completed and you "
          f"can find them here: {path_letters}")
    mail.letters()


def delete_donor():
    driver = login_database.login_neo4j_cloud()
    mail = d.Group(driver)
    individual = d.Individual(driver)
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


def update_redis(path, name):
    update = input('Which entry would you like to update?\n'
                                     '1 - Last Name\n'
                                     '2 - Telephone\n'
                                     '3 - email\n'
                                     '>>>')
    if update == '1':
        last_name = input(f"What is {name}'s last name?\n")
        d.Individual.update_last_name(path, name, last_name)
    if update == '2':
        telephone = input(f"What is {name}'s telephone #?\n")
        d.Individual.update_telephone(path, name, telephone)
    if update == '3':
        email = input(f"What is {name}'s email?\n")
        d.Individual.update_email(path, name, email)

def wrong_choice():
    pass


def quit_program():
    exit()


if __name__ == '__main__':

    switch_dict = {'1': more_choices,
                   '2': print_report,
                   '3': letters_for_all,
                   '4': delete_donor,
                   '5': load_mailroom,
                   '6': quit_program}
    while True:
        response = input(
            '\nChoose an Action:\n'
            '1 - Send a Thank You\n'
            '2 - Create a Report\n'
            '3 - Send letters to everyone\n'
            '4 - Delete a Donor\n'
            '5 - Reset Database\n'
            '6 - Quit\n'
            '>>')

        switch_dict.get(response, wrong_choice)()
