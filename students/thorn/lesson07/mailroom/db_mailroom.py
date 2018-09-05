"""
Thomas Horn
Database refactor of mailroom_oo.py
"""

import os
import logging 
from mailroom_db_model import Donor, Donation, SqliteDatabase

logger = logging.getLogger(__name__)
FORMAT = "%(filename)s : %(levelname)s : %(lineno)s: %(message)s"
logging.basicConfig(format=FORMAT)
logger.setLevel(logging.DEBUG)


class DonorDB:
    """
    Functions used to access the donor database with typical functionality including reporting, creating
    letters, adding donors and or donations, deleting donors.
    """
    def __init__(self, database):
        """ Parameter must be a SqliteDatabase. """
        self.database = database
        # Foreign keys shortcut var for laziness
        self.fk = 'PRAGMA foreign_keys = ON;'
    
    def donor_control(self, donor_name, amount):
        """ 
        Controls calls to add_donor, add_donation, and recalculate_statistics.
        """
        logger.info(f"Donor: {donor_name} | Donation: {amount} ")
        self.add_donor(donor_name)
        self.add_donation(donor_name, amount)
        self.recalculate_statistics(donor_name)
    
    def add_donor(self, donor_name):
        """ 
        Attempts to add a donor.  If donor exists, the primary key will cause an exception.  Donation handled separately.
        """
        try:
            self.database.connect()
            self.database.execute_sql(self.fk)
            with self.database.transaction():
                donor = Donor.create(name = donor_name)
                donor.save()
            logger.info(f"{donor_name} added to database.")

        except Exception as e:
            logger.error(f"{donor_name} not added to database.  {e}")
        finally:
            self.recalculate_statistics(donor_name)
            self.database.close()
            
    def add_donation(self, donor_name, amount):
        """
        Adds a donation amount to a donor.
        """
        try:
            self.database.connect()
            self.database.execute_sql(self.fk)
            with self.database.transaction():
                donation = Donation.create(
                    donor = donor_name,
                    donation_amt = amount
                )
                donation.save()
            logger.info(f"{donor_name} has donated {amount}.")
        except Exception as e:
            logger.error(f"Unable to save donation of {amount} for {donor_name}.  {e}")
        finally:
            self.database.close()

    def recalculate_statistics(self, donor_name):
        """
        Forces a recalculation of total donation amount, number of donations, and avg donations after
        updated information.
        """
        try:
            self.database.connect()
            self.database.execute_sql(self.fk)
            # Vars for calculations to be fed back into a query
            donation_sum = 0

            # for donation in Donation.select().where(Donation.donor == donor_name):
            #     donation_sum += donation.donation_amt
            #     counter += 1
            
            x = Donation.select().where(Donation.donor == donor_name)
            counter = x.count()
            for item in x:
                donation_sum += int(item.donation_amt)

            logger.info(f"{donor_name} | {donation_sum} | {counter}")

            # Update donor totals
            with self.database.transaction():
                donor = Donor.get(Donor.name == donor_name)
                donor.num_donations = counter
                donor.total_donation_amt = donation_sum
                donor.avg_donation = donation_sum / counter
                donor.save()

        except Exception as e:
            logger.error(e)
        finally:
            self.database.close()
    
    def print_donors(self):
        """
        Prints and returns a list of all donor names.
        """
        try:
            self.database.connect()
            self.database.execute_sql(self.fk)
            for donor in Donor.select():
                print(donor.name)
            return [donor.name for donor in Donor.select()]
        except Exception as e:
            logger.error(e)
        finally:
            self.database.close()

    def print_all_donor_info(self):
        """
        Save as print donors but includes donation statistics.
        """
        try:
            self.database.connect()
            self.database.execute_sql(self.fk)
            for donor in Donor.select():
                print(f"{donor.name} has donated ${donor.total_donation_amt:.02f} over {donor.num_donations} donations, averaging ${donor.avg_donation:.02f}")
        except Exception as e:
            logger.error(e)
        finally:
            self.database.close()

    def delete_donor(self):
        """
        Attempts to delete a donor from the Donor database.
        """
        donor_name = input("Please enter a donor to delete.  ")
        try:
            self.database.connect()
            self.database.execute_sql(self.fk)
            with self.database.transaction():
                donor = Donor.get(Donor.name == donor_name)
                donor.delete_instance()
                donation = Donation.get(Donation.donor == donor_name)
                donation.delete_instance()
            logging.info(f"{donor_name} has been deleted.")
        except Exception as e:
            logger.error(f"Unable to delete {donor_name}.  {e}")
        finally:
            self.database.close()

    def update_donor(self):
        """ 
        Attempts to update a donor's name.
        """
        existing_donor_name = input("Please enter a donor to update.  ")
        new_name = input("Please enter a new name.  ")
        try:
            self.database.connect()
            self.database.execute_sql(self.fk)
            with self.database.transaction():
                Donor.update(name=new_name).where(Donor.name == existing_donor_name).execute()
        except Exception as e:
            logger.error(f"Unable to delete {existing_donor_name}.  {e}")
        finally:
            self.database.close()

    def donor_report(self):
        """
        Creates a formatted report of donors and their donations.
        """
        # Table header formatting
        line_one = '{:20} | {:>15} | {:>5} | {:>15}'.format(
            'Donor', 'Total', '#', 'Avg'
        )
        print(line_one)
        print('-' * (len(line_one)))

        # Get actual data
        try:
            self.database.connect()
            self.database.execute_sql(self.fk)
            for donor in Donor.select():
                print(f'{donor.name:<20} | {donor.total_donation_amt:>15,.2f} | {donor.num_donations:>5} | {donor.avg_donation:>15,.2f}')
        except Exception as e:
            logger.error(e)
        finally:
            self.database.close()

    def send_letters(self):
        """
        Writes a letter to every donor thanking them for their total donations..
        """
        # Option flag to prevent cluttering the mailbox every time
        option_flag = False
        option = input("Do you want to actually create the letters?  Y/N:  ")
        if option.lower() == 'y' or 'yes':
            option_flag = True

        try:
            self.database.connect()
            self.database.execute_sql(self.fk)
            for donor in Donor.select():
                donor_name = donor.name
                total_donations = donor.total_donation_amt

                # Send letter.  Leaving this as print for now but built in an actual file writer
                letter  = f'Dear {donor_name},\n'
                letter += f'Thank you for your generous donations of ${total_donations:.2f}.\n'
                letter += f'                                   Sincerely,        \n'
                letter += f'                                    - Team'
                print(letter)

                if option_flag:
                    with open(f"{donor_name}_thanks.txt", 'w+') as outfile:
                        outfile.write(letter)

        except Exception as e:
            logger.error(e)
        finally:
            self.database.close()

    @staticmethod
    def get_name():
        return input("Please enter the donor's name.  ")

    @staticmethod
    def get_amount():
        return input("Please enter a donation amount.  ")

    def menu(self):
        while True:
            menu = input(
                        '\nPlease select an option:\n'
                        'Q - Quit\n'
                        '1 - Add Donation\n'
                        '2 - Update Donor Info\n'
                        '3 - View All Donors\n'
                        '4 - View Donor Report\n'
                        '5 - Delete Donor\n'
                        '6 - Create Letters\n'
                        '>  '
                    )
            if menu.lower() == 'q':
                break
            elif menu.isalpha() and menu.lower() != 'q':
                print("Please enter a valid selection.")
            elif menu == '1':
                name = self.get_name()
                amount = self.get_amount()
                self.donor_control(name, amount)
            elif menu == '2':
                self.update_donor()
            elif menu == '3':
                self.print_donors()
            elif menu == '4':
                self.donor_report()
            elif menu == '5':
                self.delete_donor()
            elif menu == '6':
                self.send_letters()

            # Hidden test
            elif menu == '7':
                name = self.get_name()
                self.recalculate_statistics(name)

    
if __name__ == "__main__":
    # Pass database to DonorDB constructor
    db = DonorDB(SqliteDatabase('mailroom_database.db'))
    db.menu()


        