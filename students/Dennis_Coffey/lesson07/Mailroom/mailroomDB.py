#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import os
import logging
from peewee import *
from create_mailroom_db import *
from populate_mailroom_db import *
#import create_mailroom_db as createdb

"""
Created on Wed Apr 3 19:30:19 2019

@author: dennis coffey
"""

"""You work in the mail room at a local charity. Part of your job is to write incredibly boring, 
repetitive emails thanking your donors for their generous gifts. 
You are tired of doing this over and over again, so you’ve decided to let Python help 
you out of a jam and do your work for you."""

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define database
database = SqliteDatabase('donors.db')
   
# DonorDatabase class - properties and methods for managing donors database
class DonorDatabase:
        
    # Add new donor to donor collection
    def delete_donor(self):
        """ Delete all donor records"""
        del_donor_name = name_prompt()
        
        # Delete user from database
        try:
            nrows = Donation.delete().where(Donation.donor_name == del_donor_name).execute()
            
        except Exception as e:
            logger.info(f'Error deleting donor from database')
            logger.info(e)
     
    # Create report
    def create_report(self):
        #Create list of summarized donations so that total can be sorted
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            sorted_donors = (Donation
                     .select(Donation.donor_name,
                             fn.SUM(Donation.donation_amount).alias('sum_donations'),
                             fn.COUNT(Donation.donation_amount).alias('number_donations'),
                             (fn.SUM(Donation.donation_amount)/fn.COUNT(Donation.donation_amount)).alias('avg_donations'))
                     .group_by(Donation.donor_name)
                     .order_by(fn.SUM(Donation.donation_amount).desc()))
            
        except Exception as e:
            logger.info(f'Error retrieving donations from database')
            logger.info(e)
            
        finally:
            database.close()
                 
        # Print summarized data
        report = '\nDonor Name                | Total Given | Num Gifts | Average Gift\n'
        report += '-'*66 + '\n'
        for donor in sorted_donors:
                report +=  f'{donor.donor_name: <27}${donor.sum_donations: >12.2f}{donor.number_donations: >12}  ${round(donor.avg_donations,2): >11.2f}\n'
        print(report)
        return report

    # Send letters to everyone
    def send_letters(self):

        now = datetime.datetime.now()
        now = str(now.year) + '-' + str(now.month) + "-" + str(now.day)
        current_path = os.getcwd()
        new_path = current_path + '/letters'
    
        # Query database for donors and last donation
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
            sorted_donors = (Donation
                     .select(Donation.donor_name,
                             fn.MAX(Donation.donation_amount).alias('last_donation'))
                     .group_by(Donation.donor_name)
                     .order_by(Donation.donor_name))
            for donor in sorted_donors:
                print(donor.donor_name)
            
        except Exception as e:
            logger.info(f'Error retrieving donors last donation from database')
            logger.info(e)
            
        finally:
            database.close()
            
        # Change directory to letters directory, if it doesn't exist, create it
        try:
            os.chdir(new_path)
        except FileNotFoundError:
            os.makedirs(new_path)  
            os.chdir(new_path)
                
        # Loop through each donor and send thank you email
        try:
            for donor in sorted_donors:
                with open(donor.donor_name + '_' + str(now) + '.txt', 'w') as outfile:
                    outfile.write(create_email(donor.donor_name, donor.last_donation))
    
            print('\nThe thank you emails were sent!\n')
        except:
            print('\nThere was an error sending the thank you emails.')

        # Set directory back to base directory
        os.chdir(current_path)
                   
# Create email to donor thanking them for their generous donation
def create_email(donor_name, amount):
    return '\nDear {},\n\nThank you so much for generous donation of ${}.\n\n\t\t\tSincerely,\n\t\t\tPython Donation Team'.format(donor_name, amount)

# Sending a Thank You
def send_thankyou():
    """
    Prompts for donor name and donation amount.  If donor does not exist, donor 
    and donation will be added to database.  If donor does exist, donation
    will be updated for donor.
    """
    
    # Loop if user selects list
    full_name = 'list'
    while full_name.lower() == 'list':
        # Create prompt menu
        full_name = input('Please input your Full Name\n'
                          '\t or list if you would like to see a list of donors >> ')
            
        # Check user input and perform appropriate action    
        if full_name.lower() == 'list':
            # Query database for list of donors
            try:
                database.connect()
                database.execute_sql('PRAGMA foreign_keys = ON;')
                sorted_donors = (Donation
                         .select(Donation.donor_name)
                         .group_by(Donation.donor_name)
                         .order_by(Donation.donor_name))
                for donor in sorted_donors:
                    print(donor.donor_name)
                
            except Exception as e:
                logger.info(f'Error retrieving donors last donation from database')
                logger.info(e)
                
            finally:
                database.close()
        else:
            prompt_donation(full_name)
            break

# Prompt for donation amount and append donation to user    
def prompt_donation(full_name, donation_amount = None):

    # Promt for donation amount
    donation_amount = input('Please enter a donation amount $')
    
    if not donation_amount.isnumeric():
        print('Not a valid donation.')
        prompt_donation(full_name)
    else:
    
        # Open database and add donation information
        try:
            database.connect()
            database.execute_sql('PRAGMA foreign_keys = ON;')
    
            # Find max donation_id
            results = Donation.select(fn.MAX(Donation.donation_id).alias('max_donation_id'))
            for result in results:
                max_donation_id = result.max_donation_id        
            
            # Insert donor and donation into database
            res = Donation.insert({
                Donation.donation_id: max_donation_id + 1,
                Donation.donor_name: full_name,
                Donation.donation_amount: donation_amount}).execute()        
    
        except Exception as e:
            logger.info(f'Error adding donor and donation info to database')
            logger.info(e)
    
        finally:
            print(create_email(full_name, donation_amount) + '\n')
            database.close()

def name_prompt ():
    """Prompt for donor's name to delete"""
    return input('\nPlease enter the name of the Donor you want to delete:  ')

def user_quit():
    """Quit program"""
    database.close()
    print("\nThank you, have a nice day.")


if __name__ == '__main__':

    donors = DonorDatabase()

    # Loop until user selects Quit
    prompt = None
    switch_action_dict = {'a':send_thankyou, 'b':donors.create_report, 'c': donors.send_letters, 'd': donors.delete_donor, 'e': user_quit}
    while prompt != 'e':
        # Create prompt menu
        prompt = input('Actions to choose from:\n'
                         '\ta) Send a Thank You\n'
                         '\tb) Create a Report\n'
                         '\tc) Send letters to everyone\n'
                         '\td) Delete user\n'
                         '\te) Quit\n'
                         'Please choose an action: ')
        try:
            switch_action_dict.get(prompt)()
        # Handle error for when user does not choose a valid option in the list
        except TypeError:
            print('\nNot a valid option.  Please choose a value from the list (a, b, c, d or e)')
