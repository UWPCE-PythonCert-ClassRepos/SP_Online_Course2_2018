# lesson 07 mailroom using peewee
# !/usr/bin/env python3

""" Print Donor Database Report """

import logging
from mailroom_setup import *
import datetime


def write_letters():
    """ Write txt file letter to each donor """
    
    logger.info('Trying to Save To Text')

    try:    
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        for donor in Donor:
            with database.transaction():
                current = datetime.datetime.now()
                date = [str(current.month), str(current.day), str(current.year)]
                current_date = "_".join(date)
                letter_name = donor.donor_name + " " + current_date + ".txt"
                with open(letter_name, "w") as donor_letter:
                    donor_letter.write("Dear {},\n\n"
                                       "Thank you for supporting The Brave Heart Foundation.\n"
                                       "Your donations totaling ${:,.0f} have made a positive,\n"
                                       "life-changing impact for teens nationwide.\n\n"
                                       "Blessings,\n"
                                       "BHF".format(donor.donor_name, donor.donor_total))
        print("Files completed.")
        
    except Exception as e:
        logger.info(f'Error writing letter to {donor.donor_name}')
        logger.info(e)
        logger.info(f'Writing letters failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()

def save_to_text():
    """ Save database to txt file """
    
    logger.info('Trying to Save To Text')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with open("Donation_Data.txt", "w") as save_file:
            with database.transaction():
                for donation in Donation:
                    save_file.write(f'{donation.donation_donor}, {donation.donation_amount}, {donation.donation_date}, {donation.donation_id}\n')
        print("File completed.")
        
    except Exception as e:
        logger.info(f'Error saving to txt file')
        logger.info(e)
        logger.info(f'Saving data failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()


if __name__ == '__main__':
    write_letters()
    save_to_text()
    