

from peewee import *
import mailroom_database as maildb
from mailroomdb import *
from pprint import pprint
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PeeweeDBConnection():
    
    def __init__(self, database):
        self.database = database
        
    def __enter__(self):
        self.database.connect(reuse_if_open=True)
        self.database.execute_sql('PRAGMA foreign_keys = ON;')
        logger.info('Writing to database')
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            print(exc_val)
        self.database.close()
        

class DBQueries():
    
    def __init__(self, dbconnection):
        self.dbconnection = dbconnection
    

    def add_donor(self, donor):
        with self.dbconnection as db:
            cur_donor = maildb.Donor(first_name=donor._first,
                         last_name=donor._last)
            cur_donor.save()
            cur_id = cur_donor.donor_id
        donor.id_num=cur_id
     

    # donor parameter is string, returns donor_id   
    def search_donor(self, first1, last1, entry ='False'):   
        with self.dbconnection as db:
            first, last = first1.title(), last1.title()
            query = maildb.Donor.select(maildb.Donor.donor_id, maildb.Donor.first_name, maildb.Donor.last_name).where(maildb.Donor.last_name == last, maildb.Donor.first_name == first)
        return query

    


    def display_single_donor(self, reply, query_tuple):
        with self.dbconnection as db:
            first, last = reply.split()
            total = self.total_donations(query_tuple[0][0])
            count = self.num_of_donations(query_tuple[0][0])
            avg = self.average_donations(total, count)
            self.print_format(first, last, total, count, avg)


    def delete_donor(self, reply, query_tuple): 
        with self.dbconnection as db: 
            first, last = reply.split()
            answer = input(f"Are you sure you would like to erase {first.title()} {last.title()} from the database?\n Enter 'Y' or 'N'>>>")
            if answer.upper() == 'Y':
                maildb.Donation.delete().where(maildb.Donation.donor == query_tuple[0][0]).execute()
                maildb.Donor.delete().where(maildb.Donor.donor_id == query_tuple[0][0]).execute()
                print(f'{first.title()} {last.title()} removed successfully.')
            else:
                print("Invalid Response. Please try again.")

    def update_donor_query(self, query_tuple):
        try: 
            with self.dbconnection as db:
                reply = input("Enter which field you would like to update:\n1 to update first name\n2 to update last name.\n>>")
                if reply == '1':
                    reply2 = input('Enter the first name you would like to update:\n>>')
                    print(reply2.title())
                    update = (maildb.Donor
                             .update(first_name = reply2.title())
                             .where(maildb.Donor.donor_id == query_tuple[0][0])
                             .execute())
                    print(f'First name updated successfully from {query_tuple[0][1]} to {reply2.title()}')

                elif reply == '2':
                    reply2 = input('Enter the last name you would like to update:\n\
                                   >>')
                    update = (maildb.Donor
                             .update(last_name = reply2.title())
                             .where(maildb.Donor.donor_id == query_tuple[0][0])
                             .execute())
                    print(f'Last name updated successfully from {query_tuple[0][1]} to {reply2.title()}')

                else:
                    raise Exception
            
        except Exception:
            print("Invalid reponse. Please try again.")
            return False


    # Donation Table queries

    def add_donation(self, donor_id, donation):
        with self.dbconnection as db:
            maildb.Donation.insert(donation=donation, donor=donor_id).execute()
            
    def total_donations(self, cur_id):

        query = (maildb.Donation.select(fn.SUM(maildb.Donation.donation).alias('total'))
                .join(maildb.Donor)
                .where(maildb.Donor.donor_id == cur_id))
        logging.info(f'result of total donations: {query[0].total}')
        return query[0].total


    def num_of_donations(self, cur_id):


        query = (maildb.Donation.select(fn.COUNT(maildb.Donation.donation).alias('count'))
                .join(maildb.Donor)
                .where(maildb.Donor.donor_id == cur_id))
        return query[0].count

    def average_donations(self, total, count):

        self.average = total / count
        return self.average 


    def get_all_donors_summary(self):
        with self.dbconnection as db:
            dl = list(maildb.Donor.select().execute())
            for donor in dl:
                cur_id = donor.donor_id
                logging.info(f'value of donorID: {cur_id}')
                first = donor.first_name
                last = donor.last_name
                total = self.total_donations(cur_id)
                count = self.num_of_donations(cur_id)
                avg = self.average_donations(total, count)
                self.print_format(first, last, total, count, avg)



    def print_format(self, first, last, total, count, avg):
        print("Donor Name        |   Total Given   |   Num Gifts  |  Average Gift")
        print("-----------------------------------------------------------------------")
        print(f"{first} {last}\t  ${total:>11.2f}    {count:>10}       ${avg:>10.2f}")

        

