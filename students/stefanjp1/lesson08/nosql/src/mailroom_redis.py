""" Module to run user interface to mailroom database """

import sys
import login_database
from donor_data import get_donor_data

r = login_database.login_redis_cloud()


def donor_totals(name):
    """ Return the count and sum of donations for a donor """
    all_donation_records = list()
    all_donation_records.append(r.get(name))

    total_donated = 0
    total_donations = 0
    for donation in all_donation_records:
        total_donated += float(donation)
        total_donations += 1

    return total_donations, total_donated


def add_new_donation():
    """ add a new donation to the database """
    name = input("Enter the donor's full name > ")

    amount = float(input("\nEnter donation amount: "))
    
    r.set(name, amount)

    return name


def send_thank_you(name='add_donation'):
    """ Print or return a stock thank you letter """
    if name == 'add_donation':
        name = add_new_donation()
        total_donations, total_donated = donor_totals(name)

        print("""Dear {},\n\n\tThank you for your kind donations totaling ${:.2f}.\n\n\t
        It will go a long way to feed the needy. \n\n\t\tSincerely, \n\n\t\t  -The Team""".format(name, total_donated))
    else:
        total_donations, total_donated = donor_totals(name)

        return"""Dear {},\n\n\tThank you for your kind donations totaling ${:.2f}.\n\n\t
        It will go a long way to feed the needy. \n\n\t\tSincerely, \n\n\t\t  -The Team""".format(name, total_donated)


def send_letters():
    """ Create stock thank you letters for each donor """
    all_donors = r.keys()
    print(all_donors)
    for donor in all_donors:
        letter = send_thank_you(donor)

        file_path = donor + '.txt'
        with open(file_path, 'w') as outfile:
            outfile.write(letter)


def delete_donor():
    """ Remove a donor and his/her donations from the DB """
    name = input("Enter the donor's full name > ")

    r.delete(name)
        
    print("Deleted donor {}".format(name))



if __name__ == '__main__':
    r = login_database.login_redis_cloud()
    
    while True:
        prompt = input("""Enter:\n Send a Thank You (1)\n Send Letter to Everyone (2)\n Delete a donor (3)\n or quit (4) > """)

        try:
            prompt = int(prompt)
        except ValueError:
            print("Input must be an integer, try again.")
            continue

        prompt_dict = {1: send_thank_you,
                       2: send_letters,
                       3: delete_donor,
                       4: 'quitting program'}

        try:
            user_choice = prompt_dict[prompt]
        except KeyError:
            print("Input integer was outside range of choices, try again.")
            continue

        if prompt != 4:
            user_choice()
        else:
            print(user_choice)
            sys.exit()
