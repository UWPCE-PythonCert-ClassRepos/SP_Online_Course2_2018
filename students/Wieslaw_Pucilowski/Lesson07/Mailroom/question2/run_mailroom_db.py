from peewee import *
from create_donors_db import *
import logging
import pprint
pp = pprint.PrettyPrinter(width=120)

__author__ = "Wieslaw Pucilowski"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# database has been created during create_donors_db import

class Main():
    database = SqliteDatabase('mailroom.db')
    
    def connect_db(Table=None):
        if database.connect():
            logger.info('Connecting to database...')
            logger.info('Working with table {}...'.format(Table))
        else:
            logger.info('Not connectred to database...')

    @staticmethod
    def report():
        logger.info('+++ Printing DB report')
        try:
            logger.info('Connecting to database...')
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Donor
                    .select(Donor.donor_name.alias('donor'),
                            fn.COUNT(Donation.donor_id).alias('num'),
                            fn.SUM(Donation.amount).alias('total'),
                            fn.AVG(Donation.amount).alias('avg'))
                    .join(Donation,
                          JOIN.LEFT_OUTER,
                          on=(Donor.donor_name == Donation.donor_id))
                    # .object()
                    .group_by(Donor.donor_name)
                    .order_by(fn.SUM(Donation.amount).desc())
            )
            pp.pprint('{:30} | {:20} | {:15} | {:17}'.format(
                                        'Donor',
                                        'Number',
                                        'Total',
                                        'Average')
                                )
            pp.pprint('='*91)
            for result in query:
                pp.pprint('{:<30} | {:<20} | {:<15.2f} | {:<17.2f}'.format(
                                                str(result.donor),
                                                str(result.num) if result.num else 0,
                                                result.total if result.num else 0.00,
                                                result.avg if result.num else 0.00
                                            )
                       )
        except Exception as e:
            logger.info(e)
        finally:
            database.close()

    def greetings(name, amount):
        gr = """
    Ex Programmers Charity
    1999 Heartbeat Avenue
    11111 Fresh Spring, Alaska

    Dear {}

    Thank you so much for your generous donation of ${}

    It will be put to very good use.

                       Sincerely,
                          -The Team

    """.format(name, amount)
        return(gr)

    def print_greetings(gr):
        print(gr)

    def write_letter(name, amount):
        try:
            with open("_".join(name.split()) +'.txt', 'w') as f:
                f.write(Main.greetings(name, amount))
        except IOErrors as e:
            print("""
                Cannot write a file, cought
                {}
            """.format(e))

    @staticmethod
    def letters():
        logger.info('Writing letters to all Donors...')
        try:
            logger.info('Connecting to database...')
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Donation
                    .select(Donation.donor_id.alias('donor'),
                            fn.SUM(Donation.amount).alias('total'))
                    .group_by(Donation.donor_id)
            )
            for result in query:
                Main.write_letter(str(result.donor),
                             str(result.total)
                             )
        except Exception as e:
            logger.info(e)
        finally:
            database.close()

    @staticmethod
    def add_donor():
        """
        Adds new donor and donation,
        or adds donation to existing donor
        """
        logger.info('+++ Adding/Updating Donors')
        Main.connect_db()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        name = input("Type donor first and last name: ")
        location = input("Type donor location (optional): ")
        try:
            don = float(input(" Donation in USD: "))
        except ValueError:
                print("""
                      Donation must be in USD...
                      Donor not added
                      """)
                return()
        logger.info("Checking if donor {} is in Database".format(name))
        try:
            with database.transaction():
                try:
                    person = Donor.get(
                                        Donor.donor_name == name
                                       )
                except Exception as e:
                    logger.info("Adding new donor {} from {} to Database".format(name, location))
                    new_donor = Donor.create(
                                                donor_name = name,
                                                donor_location = location
                                             )
                    new_donor.save()
                else:
                    logger.info("Donor {} is in Database, only donation will be added".format(name))
        except Exception as e:
            logger.info(f'Exception cought when adding Donor!')
            logger.info("Exception: {}".format(e))
        finally:
            try:
                with database.transaction():
                    new_donation = Donation.create(
                                            donor = name,
                                            amount = don
                            )
                new_donation.save()
            except Exception as e:
                logger.info(f'Exception cought when adding Donation!')
                logger.info("Exception: {}".format(e))
            logger.info('Closing database...')
            database.close()

        Main.print_greetings(Main.greetings(name, don))

    @staticmethod
    def delete_donation():
        """
        Delete donor and all her/his donations from Donation
        """
        name = input("Donor to delete first and last name: ")
        Main.connect_db("Donation")
        try:
            with database.transaction():
                query = (Donation
                         .delete()
                         .where(Donation.donor == name)
                         )
            logger.info("Deleted rows: {}".format(query.execute()))
        except Exception as e:
            logger.info('Exception cought when deleting {} in Donation table'.format(name))
            logger.info("Exception: {}".format(e))
        finally:
            logger.info('Closing database...')
            database.close()
            return(name)

    @staticmethod
    def delete_donor():
        """
        Working with Donor table...
        """
        logger.info('+++ Delete donor')
        name = Main.delete_donation()
        Main.connect_db("Donor")
        try:
            with database.transaction():
               query = (Donor
                         .delete()
                         .where(Donor.donor_name == name)
                         )
               logger.info("Deleted rows: {}".format(query.execute()))
        except Exception as e:
            logger.info('Exception cought when deleting {} in Donor table'.format(name))
            logger.info("Exception: {}".format(e))
        finally:
            logger.info('Closing database...')
            database.close()

    @staticmethod
    def delete_donation_only():
        """
        Delete particular donation for donor
        """
        logger.info('+++ Delete donor\'s donation')
        Main.connect_db("Donation")
        database.execute_sql('PRAGMA foreign_keys = ON;')
        name = input("Provide donor\'s name to delete her/his donation: ")
        try:
            with database.transaction():
                query =  (Donation
                          .select(Donation.id,
                                  Donation.donor,
                                  Donation.amount)
                          .where(Donation.donor == name)
                          .order_by(Donation.id)
                         )
                for i in query:
                    print("ID: {}, Donor: {} Donation: {}".format(i.id,
                                                                  i.donor,
                                                                  i.amount))
        except Exception as e:
            logger.info('Exception cought'.format(name))
            logger.info("Exception: {}".format(e))
        finally:
            logger.info('Closing database...')
            database.close()
        indx = input("Provide donation id to delete: ")
        Main.connect_db("Donation")
        try:
            with database.transaction():
                query = (Donation
                         .delete()
                         .where(Donation.id == indx)
                         )
                logger.info("Deleted rows: {}".format(query.execute()))
        except Exception as e:
            logger.info('Exception cought when deleting {} in Donation table'.format(name))
            logger.info("Exception: {}".format(e))
        finally:
            logger.info('Closing database...')
            database.close()

    @staticmethod
    def show():
        """
        Print list of donors
        """
        logger.info('List donors')
        try:
            logger.info('Connecting to database...')
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            for i in Donor.select().order_by(Donor.donor_name):
                print(i)
        except Exception as e:
            logger.info(e)
        finally:
            database.close()                            

    @staticmethod
    def challenge(factor, min_donation=None, max_donation=None):
        """
        Updating Donations according to projections
        """
        logger.info('+++ Run Challane with factor: {}, min: {}, max: {}'.format(factor,
                                                                                min_donation,
                                                                                max_donation))
        logger.info('+++ Projection')
        Main.connect_db("Donation")
        try:
            with database.transaction():
                query = (Donation
                         .update(
                                amount = (Donation.amount)*factor
                                )
                         .where(
                                (Donation.amount > min_donation) &
                                (Donation.amount < max_donation)
                         )
                )
            logger.info('{} records updated in Donation Table'.format(query.execute()))
        except Exception as e:
            logger.info('Exception cought when updating {} donations DB'.format(name))
            logger.info("Exception: {}".format(e))
        finally:
            logger.info('Closing database...')
            database.close()

    @staticmethod
    def project(factor, min_donation, max_donation):
        """
        Projection of donations
        """     
        logger.info('+++ Projection')
        Main.connect_db("Donation")
        try:
            database.execute_sql('PRAGMA foreign_keys = ON;')
            with database.transaction():
                # part multiplied by factor
                query1 =  (Donation
                          .select(Donation.donor.alias('donor'),
                                  fn.SUM((Donation.amount)*factor).alias('total'))
                          .where(
                                    (Donation.amount > min_donation) &
                                    (Donation.amount < max_donation)
                                 )
                          .group_by(Donation.donor)
                         )
                # not concerend by projection & challenge
                query2 =  (Donation
                          .select(Donation.donor.alias('donor'),
                                  (fn.SUM(Donation.amount)).alias('total'))
                          .where(
                                    (Donation.amount <= min_donation) &
                                    (Donation.amount >= max_donation)
                                 )
                          .group_by(Donation.donor)
                         )

                query = ((query1 + query2)
                            .select(
                                SQL('donor'),
                                fn.SUM(SQL('total'))
                            )
                            .group_by(SQL('donor'))
                            .order_by(SQL('donor'))
                    )

                # query = (query1 | query2).order_by(SQL('donor'))
                pp.pprint("="*60)
                pp.pprint("Projected Donors for factor: {}, min: {}, max: {}".format(factor,
                                                                           min_donation,
                                                                           max_donation)
                      )
                pp.pprint('{:30} | {:30}'.format(
                                        'Donor',
                                        'Total'))
                pp.pprint("="*60)
                for i in query:
                    pp.pprint("{:30} | {:30}".format(str(i.donor),
                                                     str(i.total)
                                                )
                                    )
        except Exception as e:
            logger.info('Exception cought when selecting {} in Donation table'.format(name))
            logger.info("Exception: {}".format(e))
        finally:
            logger.info('Closing database...')
            database.close()
        # challenge part starts here
        answer = None
        while answer not in ['Yes', 'No']:
            answer = input("Whould you like to multiply " +
                           "(above min, below max) donations: [Yes, No]:")
        if answer == "Yes":
            Main.challenge(factor,
                           min_donation=min_donation,
                           max_donation=max_donation)
            logger.info("Changes applied to DB...")
        else:
            logger.info("No changes applied to DB...")

    @staticmethod
    def backup():
        logger.info('+++ Backup DB to JSON')
        print("sqlite3 DB backup to JSON file not implemented !")
        pass


if __name__ == "__main__":

    database = SqliteDatabase('mailroom.db')

    def menu_selection(prompt, dispatcher):
            while True:
                response = input(prompt)
                try:
                    if dispatcher[response]() == "exit menu":
                        break
                except KeyError:
                    print(response, "Wrong response !")
    
    def quit(msg):
        print("{}".format(msg))
        return "exit menu"

    def main_quit():
        return quit("Goodbye...")

    def sub_quit():
        return quit("Back to Main menu...")

    def sub_menu():
        menu_selection(submenu, subfeatures)

    def projections_prompt():
        try:
            factor = int(input("What is the multiplication factor:"))
        except ValueError:
            print("Multiplication factor should be integer...")
            return
        try:
            x = input("Above Min donation:")
            min_donation = float(x) if x != '' else None
            y = input("Below Max donation:")
            max_donation = float(y) if y != '' else None
        except ValueError:
            print("Min, Max donation should be in USD...")
            return
        Main.project(factor=factor, min_donation=min_donation, max_donation=max_donation)

    def restore():
        logger.info('+++ Restoring DB from JSON')
        print("sqlite3 DB restore from JSON file not implemented!")
        pass


    menu = """
        {:-^30}

        1 - Send a Thank You
        2 - Create a Report
        3 - Send letters to everyone
        4 - Projections
        5 - Backup to JSON (pending)
        6 - Restore from JSON (pending)
        q - Quit
    """.format(' Main Menu ')

    submenu = """
        {:-^30}

        1 - Add new donor, donation
        2 - List donors
        3 - delete donor/donation
        4 - delete donation
        q - Go to Main Menu

    """.format(' Add/List donors ')

    features = {
            '1': sub_menu,
            '2': Main.report,
            '3': Main.letters,
            '4': projections_prompt,
            '5': Main.backup,
            '6': restore,
            'q': main_quit,
            }

    subfeatures = {
            '1': Main.add_donor,
            '2': Main.show,
            '3': Main.delete_donor,
            '4': Main.delete_donation_only,
            'q': sub_quit,
            }


    # start program menu
    menu_selection(menu, features)

