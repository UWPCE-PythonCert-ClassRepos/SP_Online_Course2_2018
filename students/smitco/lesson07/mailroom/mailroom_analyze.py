# lesson 07 mailroom using peewee
# !/usr/bin/env python3

""" Print Donor Database Report """

import logging
from mailroom_setup import *

def print_report():
    """ print report of donor activity """
    
    logger.info('Trying to Print Donation Data')
        
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            query = (Donor
                     .select(Donor, fn.SUM(Donation.donation_amount).alias('donor_total'), fn.COUNT(Donation.donation_id).alias('donor_count'), fn.AVG(Donation.donation_amount).alias('donor_average'))
                     .join(Donation, JOIN.INNER)
                     .group_by(Donor)
                     .order_by(SQL('donor_total').desc())
                    )

            print("\n{:<25} {:<12}  {:^10} {:^12}".format("Donor", "Total", "Count", "Average"))
            for person in query:
                print(f'{person.donor_name:<25} ${person.donor_total:>12,.2f} {person.donor_count:^10}   ${person.donor_average:>12,.2f}')


        
    except Exception as e:
        logger.info(f'Error printing donation summary')
        logger.info(e)
        logger.info(f'Printing of remaining data failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()    


def match_donations():
    """ match donations based on inputs """
    
    logger.info('Trying to Match Donation Data')

    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        with database.transaction():
            minq = Donation.select(fn.MIN(Donation.donation_amount))
            min_don = minq.scalar()
            maxq = Donation.select(fn.MAX(Donation.donation_amount))
            max_don = maxq.scalar()
            print("\nThe donation range is ${:,.0f}-{:,.0f}.".format(min_don, max_don))
            min_match = input("\nWhat is the minimum value to match?\n>>")
            max_match = input("\nWhat is the maximum value to match?\n>>")
            
            query = (Donation
                     .select(Donation.donation_amount)
                     .group_by(Donation)
                     .having(Donation.donation_amount >= min_match, Donation.donation_amount <= max_match)
                     )
            original_sum = 0
            for donation in query:
                original_sum += donation.donation_amount
            print("\nThe total in this range is ${:,.0f}.".format(original_sum))
            
            factor = input("\nBy what factor would you like to match?\n>>")
            match_sum = original_sum * int(factor)
            print("\nThe matching contribution would be ${:,.0f}.\n".format(match_sum))

    
    except Exception as e:
        logger.info(f'Error matching donations')
        logger.info(e)
        logger.info(f'Matching data failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close() 

        
        
if __name__ == '__main__':
    print_report()
    match_donations()    
