# lesson 07 mailroom using peewee
# !/usr/bin/env python3

""" Add, Delete, and Modify Donor Database Models in Peewee"""

import logging
from mailroom_setup import *
import datetime


logger = logging.getLogger(__name__)
database = SqliteDatabase('mailroom_db.db')


def add_donation():
    """ Add new donation data """

    logger.info('Trying to Add New Donation')
        
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        while True:
            add_name = input("\nTo whom would you like to send a thank you?\n"
                         "'List' will display current donors.\n"
                         "'Exit' will return to main menu.\n"
                         ">>")
            if add_name.lower() == "exit":
                database.close()
                print("\nExiting.\n")
                break
            elif add_name.lower() == "list":
                nameq = (Donor.select(Donor.donor_name))
                for name in nameq:
                    print(name)
            else:
                donation = input("\nWhat is the donation amount?\n>>")
                try:
                    donation = int(donation)
                    if donation >= (10 ** 6):
                        print("\nThe amount entered is too large.")
                    else:
                        logger.info('Trying to add new donation')
                        with database.transaction():
                            nameq = (Donor.select().where(Donor.donor_name == add_name))
                            if nameq.scalar() == None:   
                                """Add Donor to database if not in there"""
                                DONOR_NAME = 0
                                DONOR_TOTAL = 1
                                DONOR_COUNT = 2
                                DONOR_AVERAGE = 3
                                
                                donor = (add_name, 0, 0, 0)
                                new_donor = Donor.create(
                                        donor_name = donor[DONOR_NAME],
                                        donor_total = donor[DONOR_TOTAL],
                                        donor_count = donor[DONOR_COUNT],
                                        donor_average = donor[DONOR_AVERAGE]
                                        )
                                new_donor.save()
                                logger.info('Donor population successful')
                            
                            """Add Donation to database"""
                            todays_date = datetime.date.today()
                            todays_date = (f'{todays_date:%Y%m%d}')                            
                            DONATION_DONOR = 0
                            DONATION_AMOUNT = 1
                            DONATION_DATE = 2
                            donation = (add_name, donation, str(todays_date))
                            don_donor = donation[DONATION_DONOR].split()
                            don_id = donation[DONATION_DATE] + "_" + don_donor[0][0:2] + don_donor[1][0:2]
                            new_donation = Donation.create(
                                    donation_donor = donation[DONATION_DONOR],
                                    donation_amount = donation[DONATION_AMOUNT],
                                    donation_date = donation[DONATION_DATE],
                                    donation_id = don_id)
                            new_donation.save()
                            refreshq = (Donor
                                        .select(Donor, fn.SUM(Donation.donation_amount).alias('donor_total'), fn.COUNT(Donation.donation_id).alias('donor_count'), fn.AVG(Donation.donation_amount).alias('donor_average'))
                                        .join(Donation, JOIN.INNER)
                                        .group_by(Donor)
                                        .order_by(SQL('donor_total').desc())
                                        )
                            for don_ref in refreshq:
                                don_ref.donor_total = don_ref.donor_total
                                don_ref.donor_count = don_ref.donor_count
                                don_ref.donor_average = don_ref.donor_average
                                don_ref.save()
                            print(f"\nThank you, {new_donation.donation_donor}, for your generous donation of "
                                   f"${new_donation.donation_amount} to the Brave Heart Foundation.")
                            logger.info('Donation population successful')
                            break
                            
                except ValueError:
                    if donation.lower() == "exit":
                        print("\nExiting.")
                    else:
                        print("\nInvalid entry.")
            
    except Exception as e:
        logger.info(f'Error adding new donation')
        logger.info(e)
        logger.info(f'Adding of donation failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()    

def update_donation():
    """ Update donation data """
        
    logger.info('TODO')
    
    logger.info('Trying to Update Donation')
        
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        while True:
            ask_donor = input("\nFor whom would you like to update a donation?\n"
                              "'List' will display current donors.\n"
                              "'Exit' will return to main menu.\n"
                              ">>")
            nameq = Donation.select().where(Donation.donation_donor == ask_donor)
            if ask_donor.lower() == "exit":
                database.close()
                print("\nExiting.\n")
                break
            elif ask_donor.lower() == "list":
                nameq = Donor.select(Donor.donor_name)
                for name in nameq:
                    print(name)
            elif nameq.scalar() == None:   
                database.close()
                print("\nDonor not found.\n")
                break
            else:
                print("\n{:<25}  {:<10} {:<12}".format("Donor", "Date", "Amount"))
                donq = Donation.select().where(Donation.donation_donor == ask_donor)
                for donation in donq:
                    print(f'{str(donation.donation_donor):<25} {donation.donation_date:^10}  ${donation.donation_amount:>12,.2f}')
                ask_date = input("\nWhich donation date would you like to update?\n>>")
                dateq = donq.select().where(Donation.donation_date == ask_date)
                if dateq.scalar() == None:
                    print("\nThe date was not found.")
                else: 
                    update_don =  input("\nWhat is the donation amount?\n>>")
                    try:
                        if int(update_don) >= (10 ** 6):
                            print("\nThe amount entered is too large.")           
                    except ValueError:
                        if update_don.lower()== "exit":
                            print("\nExiting.")
                        else:
                            print("\nInvalid entry.")
                    update_date =  input("\nWhat is the donation date? (Format: YYYYMMDD)\n>>")
                    try:
                        int(update_date)          
                    except ValueError:
                        if update_date.lower()== "exit":
                            print("\nExiting.")
                        else:
                            print("\nInvalid entry.")
                    
                    updateq = Donation.select().where(Donation.donation_donor == ask_donor, Donation.donation_date == ask_date)
                    for upd in updateq: 
                        update_don_id = 12345678
                        upd.donation_amount = update_don
                        upd.donation_date = update_date
                        upd.save()
                        refreshq = (Donor
                                    .select(Donor, fn.SUM(Donation.donation_amount).alias('donor_total'), fn.COUNT(Donation.donation_id).alias('donor_count'), fn.AVG(Donation.donation_amount).alias('donor_average'))
                                    .join(Donation, JOIN.INNER)
                                    .group_by(Donor)
                                    .order_by(SQL('donor_total').desc())
                                    )
                        for don_ref in refreshq:
                            don_ref.donor_total = don_ref.donor_total
                            don_ref.donor_count = don_ref.donor_count
                            don_ref.donor_average = don_ref.donor_average
                            don_ref.save()
                        print(f"The donation for {upd.donation_donor} has been updated to ${upd.donation_amount} on {upd.donation_date}.")
                    break
        
    except Exception as e:
        logger.info(f'Error updating donation')
        logger.info(e)
        logger.info(f'Update of donation failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close() 
    
def delete_donation():
    """ Delete donation data """
    
    logger.info('Trying to Delete Donation')
        
    try:
        database.connect()
        database.execute_sql('PRAGMA foreign_keys = ON;')
        while True:
            ask_donor = input("\nFrom whom would you like to delete a donation?\n"
                              "'List' will display current donors.\n"
                              "'Exit' will return to main menu.\n"
                              ">>")
            nameq = Donation.select().where(Donation.donation_donor == ask_donor)
            if ask_donor.lower() == "exit":
                database.close()
                print("\nExiting.\n")
                break
            elif ask_donor.lower() == "list":
                nameq = Donor.select(Donor.donor_name)
                for name in nameq:
                    print(name)
            elif nameq.scalar() == None:   
                database.close()
                print("\nDonor not found.\n")
                break
            else:
                print("\n{:<25}  {:<10} {:<12}".format("Donor", "Date", "Amount"))
                donq = Donation.select().where(Donation.donation_donor == ask_donor)
                for donation in donq:
                    print(f'{str(donation.donation_donor):<25} {donation.donation_date:^10}  ${donation.donation_amount:>12,.2f}')
                ask_date = input("\nWhich donation date would you like to delete?\n>>")
                dateq = donq.select().where(Donation.donation_date == ask_date)
                if dateq.scalar() == None:
                    print("\nThe date was not found.")
                else: 
                    del_don = Donation.delete().where(Donation.donation_donor == ask_donor, Donation.donation_date == ask_date)
                    del_don.execute()
                    print(f"The donation record for {ask_donor} on {ask_date} was deleted.")
                    query = Donation.select().where(Donation.donation_donor == ask_donor)
                    if query.scalar() == None:
                        del_donor = Donor.delete().where(Donor.donor_name == ask_donor)
                        del_donor.execute()
                        print(f"The donor record for {ask_donor} was deleted.")
                    break
                    
    except Exception as e:
        logger.info(f'Error deleting donation')
        logger.info(e)
        logger.info(f'Deletion of donation failed')
        exit()

    finally:
        logger.info('Database closed')
        database.close()
        
if __name__ == '__main__':
    add_donation()
    update_donation()
    delete_donation()
