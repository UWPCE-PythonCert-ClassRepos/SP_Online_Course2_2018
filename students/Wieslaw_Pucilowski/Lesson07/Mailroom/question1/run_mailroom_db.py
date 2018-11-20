from peewee import *
from create_donors_db import *
import logging
import pprint
pp = pprint.PrettyPrinter(width=120)

__author__ = "Wieslaw Pucilowski"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# database has been created during create_donors_db import


class Donation:
    @staticmethod
    def above_min(self, min_don):
        return list(filter(lambda x: x >= min_don, self.donations))
    @staticmethod
    def below_max(self, max_don):
        return list(filter(lambda x: x <= max_don, self.donations))
    @staticmethod
    def between_min_max(self, min_don, max_don):
        return list(filter(lambda x: min_don <= x <= max_don, self.donations))
    @staticmethod
    def above(self, min_don):
        return list(filter(lambda x: x > min_don, self.donations))
    @staticmethod
    def below(self, max_don):
        return list(filter(lambda x: x < max_don, self.donations))
    @staticmethod
    def multiply_donations(self, factor, min_donation=None,
                           max_donation=None):
        if min_donation and max_donation:
            ll = self.below(min_donation) + \
                 list(map(lambda x: x * factor,
                          self.between_min_max(min_donation,
                                               max_donation))) + \
                 self.above(max_donation)
        elif min_donation and not max_donation:
            ll = self.below(min_donation) + (
                list(map(lambda x: x * factor, self.above_min(min_donation))))
        elif max_donation and not min_donation:
            ll = list(map(lambda x: x * factor, self.below_max(max_donation))
                      ) + self.above(max_donation)
        else:
            ll = list(map(lambda x: x * factor, self.donations))
        self.donations = ll
        return(self)


class Main():

    @staticmethod
    def report():
        logger.info('+++ Printing DB report')
        try:
            logger.info('Connecting to database...')
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            query = (Donation
                    .select(Donation.donor_id.alias('donor'),
                            fn.COUNT(Donation.donor_id).alias('num'),
                            fn.SUM(Donation.amount).alias('total'),
                            fn.AVG(Donation.amount).alias('avg'))
                    .group_by(Donation.donor_id)
            )
            pp.pprint('{:30} | {:20} | {:15} | {:15}'.format(
                                        'Donor',
                                        'Total',
                                        'Number',
                                        'Average')
                                )
            pp.pprint('='*89)
            for result in query:
                pp.pprint('{:30} | {:20} | {:15} | {:15}'.format(
                                                str(result.donor),
                                                str(result.num),
                                                str(result.total),
                                                str(result.avg)
                                            )
                       )
        except Exception as e:
            logger.info(e)
        finally:
            database.close()

    @staticmethod
    def letters():
        logger.info('+++ Writing letters')
        pass

    @staticmethod
    def donor():
        logger.info('+++ Adding Donors')
        pass

    @staticmethod
    def show():
        logger.info('+++ Shows but what?')
        pass

    @staticmethod
    def challenge():
        logger.info('+++ Challaging donors/donation but')
        pass

    @staticmethod
    def project(factor, min_donation, max_donation):
        logger.info('+++ Projection')
        pass

    @staticmethod
    def backup():
        logger.info('+++ Backup DB to JSON')
        print("sqlite3 DB backup to JSON file not implemented !")
        pass

    @staticmethod
    def delete_donor():
        logger.info('+++ Delete donor')
        pass

    @staticmethod
    def delete_donation():
        logger.info('+++ Delete donation')
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

    # def report():
    #     logger.info('+++ Printing DB report')
    #     try:
    #         logger.info('Connecting to database...')
    #         database.connect()
    #         database.execute_sql('PRAGMA foreign_keys = ON;')
    #         query = (Donation
    #                 .select(Donation.donor_id.alias('donor'),
    #                         fn.COUNT(Donation.donor_id).alias('num'),
    #                         fn.SUM(Donation.amount).alias('total'),
    #                         fn.AVG(Donation.amount).alias('avg'))
    #                 .group_by(Donation.donor_id)
    #         )
    #         pp.pprint('{:30} | {:20} | {:15} | {:15}'.format(
    #                                     'Donor',
    #                                     'Total',
    #                                     'Number',
    #                                     'Average')
    #                             )
    #         pp.pprint('='*89)
    #         for result in query:
    #             pp.pprint('{:30} | {:20} | {:15} | {:15}'.format(
    #                                             str(result.donor),
    #                                             str(result.num),
    #                                             str(result.total),
    #                                             str(result.avg)
    #                                         )
    #                    )
    # 
    #     except Exception as e:
    #         logger.info(e)
    #     finally:
    #         database.close()

    
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
        3 - delete donor
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
            '1': Main.donor,
            '2': Main.show,
            '3': Main.delete_donor,
            '4': Main.delete_donation,
            'q': sub_quit,
            }


    # start program menu
    menu_selection(menu, features)

