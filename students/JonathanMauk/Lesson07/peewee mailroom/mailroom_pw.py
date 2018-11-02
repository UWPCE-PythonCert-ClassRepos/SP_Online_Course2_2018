import os
import sys
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DonorDatabase:
    """
    Class to manipulate the new donors.db database.
    """
    def __init__(self, database):
        self.database = database

    def append_donation(self, donor, amount):
        """
        Add a donation to database.
        :param donor: Name of donor.
        :param amount: Amount of money. Needs to be int or float.
        """
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                donation = Donation.create(
                    donation_amount=amount,
                    donor_name=donor
                    )
                donation.save()
                logger.info('Database add successful.')

        except Exception as e:
            logger.info('Unable to add donation. Please try again.')
            logger.info(e)

        finally:
            self.database.close()

    def list_donors(self):
        """List all donors by name. Called by thank_you() menu."""
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            for donor in Donor.select():
                print(donor.donor_name)

        except Exception as e:
            logger.info(e)

        finally:
            self.database.close()

    def add_new_donor(self, donor):
        """
        Add new donor.
        :param donor: Name of donor.
        """
        try:
            self.database.connect()
            self.database.execute_sql('PRAGMA foreign_keys = ON;')
            with self.database.transaction():
                new_donor = Donor.create(
                    donor_name=donor
                )
                new_donor.save()
                logger.info('Database add successful.')

        except Exception as e:
            logger.info('Unable to add donor. Please try again.')
            logger.info(e)

        finally:
            self.database.close()

    def create_report(self):
        report = ""
        for donor in self.donors:
            k = donor.name
            num_gifts = donor.number_donations()
            total_given = donor.sum_donations()
            average_gifts = donor.avg_donations()
            report = report + f'{k: <26}| ${total_given:>10.2f} |{num_gifts:^11}| ${average_gifts:>11.2f}\n'
        return report


def thank_you():
    """Module with three functions:
    1) Append donation to record (if existing donor) or create a new record in database (if not an existing donor.
    2) Print thank you letter after updating database record.
    3) List all current donors in database."""
    user_input = input('Enter a donor\'s full name, or type \'list\' for a full list. ' +
                       'Type \'e\' to exit and return to the main menu.\n> ').title()
    if user_input.lower() == 'list':
        print(donor_db.list_donors())
        thank_you()
    elif user_input.lower() == 'e':
        mailroom()
    else:
        try:
            donation = float(input("Please enter a donation amount: "))
        except ValueError:
            print("Error: donations can only be entered as numbers and decimals.")
            print("Returning to previous menu...")
            thank_you()
        donor_list = donor_db.list_donors()
        for donor in donor_db.donors:
            if user_input in donor_list and donor.name != user_input:
                continue
            elif user_input in donor_list and donor.name == user_input:
                donor.append_donations(donation)
                print("Existing donor found.")
                print("Appending the amount of {0} to {1}'s file...".format(donation, user_input))
                print("Printing thank you email...")
                print("---------------------------")
                print(create_letter(0, user_input, donation))
                print("---------------------------")
                print("Returning to thank you letter menu...")
                thank_you()
            else:
                donor_db.add_new_donor(Donor(user_input, [donation]))
                print("New donor detected. Creating record for {0}...".format(user_input))
                print("Printing thank you email...")
                print("---------------------------")
                print(create_letter(1, user_input, donation))
                print("---------------------------")
                print("Returning to thank you letter menu...")
                thank_you()


def report_printing():
    """Print some user-friendly text and call report_generation() function below."""
    while True:
        print('Donor Name' + ' ' * 16 + '| Total Given | Num Gifts | Average Gift')
        print('-' * 66)
        print(donor_db.create_report())
        print('Returning to main menu...\n')
        return


def create_letter(donor_status, donor_name, donation_amt):
    """Return formatted letters, depending on options selected. Not intended to be used by itself."""
    if donor_status == 0:
        letter_text = '''
        Dear {0},

            Thank you for your very kind donation of ${1:.2f}, and for your continuing support.

            Your generous contribution will be put to very good use.

                           Sincerely,
                              -The Team
                              '''.format(donor_name, donation_amt)
        return letter_text
    elif donor_status == 1:
        letter_text = '''
        Dear {0},

            Thank you for your very kind donation of ${1:.2f}.

            Your generous contribution will be put to very good use.

                           Sincerely,
                              -The Team
                              '''.format(donor_name, donation_amt)
        return letter_text
    elif donor_status == 2:
        return('''
        Dear {0},

            Thank you for your very kind contribution(s) totaling ${1:.2f}.

            We would like you to know that your generous donation(s) will be put to very good use.

                           Sincerely,
                              -The Team
                              '''.format(donor_name, donation_amt))


# def thank_all():
#     """Print some user-friendly text and calls create_txt_files() function."""
#     current_dir = os.getcwd()
#     print("Saving letters to {0}...".format(current_dir))
#     create_txt_files()
#     print("---------------------------")
#     print("Letters saved to text files in directory. Returning to main menu...")
#     mailroom()
#
#
# def create_txt_files():
#     """Write letters generated by create_letter to text files, saving them to same directory as script."""
#
#     for donor in donor_db.donors:
#         name = donor.name
#         donation = sum(donor.donations)
#         letter = create_letter(2, name, donation)
#         with open('{:s}.txt'.format(donor.name), 'w') as f:
#             f.write(letter)


def mailroom():
    """Generate main menu options and activate other functions."""
    while True:
        selection = input('MAILROOM v0.5.1: SQLite Branch\n------------------------' +
                          '\nChoose an option:\n1) Send a thank you' +
                          '\n2) Create a report\n3) Quit\n> ')
        menu_dict = {'1': thank_you, '2': report_printing, '3': quit_program}
        try:
            menu_dict.get(selection)()
        except TypeError:
            print("Invalid value. Enter a number from 1-3.")
            pass


def quit_program():
    """Quit Mailroom program."""
    print("Exiting...")
    sys.exit()


if __name__ == "__main__":
    mailroom()
