import unittest
import pymongo
#from peewee import *
#import donors_sql as d
import logging
import logging.config
import utilities
#import create_mr_tables as new_database
#from create_mr_tables import *
#from create_mr_tables import database
import os
import login_database
import Load_Tables
log = utilities.configure_logger('default', '../logs/test_dev.log')
people = Load_Tables.get_people_data()

client = login_database.login_mongodb_cloud()
log.info('Step 1: We are going to use a database called mailroom')
log.info('But if it doesnt exist mongodb creates it')
test_db = client['test_db']




class TestMailbox(unittest.TestCase):

# Delete test.db first
    log.info('First delete the test_collection so we can start over.')
    test_db.drop_collection('test_collection')

    log.info('And in the test database use a collection called test_people')
    log.info('If it doesnt exist mongodb creates it')
    test_people = test_db['test_people']

#Load the collection 'test_people' from the Load_Tables.py file.
    log.info('Populate the database with people. MongoDB is non-relational so'
             'the donors and the donations should be kept together.')
    test_people.insert_many(people)
    logger.info('Completed loading donors')


    def test_Connection(self):
        log.info('Find the person Zach')
        query = {'donor': 'Zach'}
        results = test_people.find_one(query)
        self.assertEqual(results, 'Zach')  # Test donor was added

#    def test_Individual_Add_Donation1(self):
#        database.connect(reuse_if_open=True)
#        database.execute_sql('PRAGMA foreign_keys = ON;')
#        d.Individual.add_donation('Luke', 5)
#        aperson = Donor.get(Donor.donor_name == 'Luke')
#        adonation = Donations.get(Donations.donor_name == 'Luke')
#        self.assertEqual(aperson.donor_name, 'Luke')  # Test donor was added
#        self.assertEqual(adonation.donation, 5) # Test donation was added for Luke


#    def test_Group_search1(self):
#        """Returns None when name does not exist"""
#        #database.connect(reuse_if_open=True)
#        group_instance = d.Group('test.db')
#        search_result = group_instance.search('Bob') # Bob is not in database
#        self.assertEqual(search_result, None)

#    def test_Group_search2(self):
#        """Returns 'name' when name does exist"""
#        database.connect(reuse_if_open=True)
#        group_instance = d.Group('test.db')
#        search_result = group_instance.search('Zach') # 'Zach is in database
#        self.assertEqual(search_result, 'Zach')


#    def test_thankyou(self):
#        test_text = 'Thank you so much for the generous gift of $5.00, Shane!'
##        thank_you = d.Individual('Shane', [5])
#        self.assertEqual(d.Individual.thank_you('Shane', 5), test_text)

#    def test_summary(self):
#        """Test dictionary set with {Donor: Total, number of donations,
#        and average donation amount}"""
#        group_instance = d.Group('test.db')
#        summary = group_instance.summary() # 'Zach is in database
#        self.assertDictEqual(summary, {'Shane': [21, 3, 7.0],
#                                   'Joe': [5, 1, 5.0],
#                                   'Zach': [10, 1, 10.0],
#                                   'Pete':[15, 2, 7.5],
#                                   'Fitz':[1,1,1.0],
#                                   'Luke':[5, 1, 5.0]})

#    def test_sort_list(self):
#        """sorts the dictionary by largest to smallest donation"""
#        group_instance = d.Group('test.db')
#        summary = group_instance.summary()
#        sorted = group_instance.sort_list(summary)
#        self.assertEqual(sorted, ['Shane', 'Pete', 'Zach', 'Joe', 'Luke', 'Fitz'])


#    def test_number_donations(self):
#        num_donations = d.Individual.number_donations('Shane')
#        self.assertEqual(num_donations, 3)

#    def test_sum_donations(self):
#        sum_donation = d.Individual.sum_donations('Shane')
#        self.assertEqual(sum_donation, 21)

#    def test_avg_donations(self):
#        avg_donations = d.Individual.avg_donations('Shane')
#        self.assertEqual(avg_donations, 7)


#class TestDelete(unittest.TestCase):
#    """Test deleting a donor. Need to recreate the database to ensure deletion
#    doesn't happen before other test cases."""
#    cur_dir = os.getcwd()
#    logger.debug(f'Current Directory is {cur_dir}')
#    file_list = os.listdir(cur_dir)
#    logger.debug(f'File list is {file_list}')
#    db_file = []
#    if os.path.exists('test2.db'):
#        logging.info('Trying to delete the database.')
#        os.remove('test2.db')
#        logger.info(f'Database test.db has been deleted.')

    # Create a new database named test.db
#    cwd = os.getcwd()
#    logger.info(f'Creating new database test.db.')
#    database.init('test2.db')
#    database.connect()
#    logger.info('Creating Modules in database')
#    database.create_tables([Donor, Donations])
#    database.close()
#    logger.info('Database has been created and is closed.')

    # Loading tables in new database
#    database.connect()
#    logger.info('Connected to database')
#    database.execute_sql('PRAGMA foreign_keys = ON;')
#    donors = ['Shane', 'Pete', 'Zach', 'Joe', 'Fitz']
#    donations = [('Shane', 6), ('Shane', 5), ('Shane', 10), ('Joe', 5), ('Zach', 10),
#                 ('Pete', 7), ('Pete', 8), ('Fitz', 1)]

#    def test_delete_donor(self):
#        """Delete a donor and check that the name is deleted in both the Donor table
#        and the Donations table."""
#        #indiv_initalize = d.Individual('test2.db')
#        database.connect(reuse_if_open=True)
#        database.execute_sql('PRAGMA foreign_keys = ON;')

        #show that you can find 'Shane'
#        aperson = Donor.get(Donor.donor_name == 'Shane')
#        self.assertEqual(aperson.donor_name, 'Shane')  # Test donor exists


        # Delete the donor 'Shane'
#        d.Individual.delete_donor('Shane')

        # After deleting 'Shane', search donor table for shane
#        query_donor = Donor.select().where(Donor.donor_name == 'Shane')
#        donor_list = []  # Create a list of donations for 'name'.
#        for result in query_donor:
            # logger.info(f'{result.donor_name}')
#            donor_list.append(int(result.donor_name))
#        self.assertEqual(donor_list, [])

        # After deleting 'Shane', search donation table for shane
#        query_donation = Donations.select().where(Donations.donor_name == 'Shane')
#        donation_list = []  # Create a list of donations for 'name'.
#        for result in query_donation:
            # logger.info(f'{result.donor_name}')
#            donation_list.append(int(result.donation))
#        self.assertEqual(donation_list, [])

        # After deleting a donor, show that you can still find other donors.
#        aperson = Donor.get(Donor.donor_name == 'Pete')
#        self.assertEqual(aperson.donor_name, 'Pete')  # Test donor was added


if __name__ == '__main__':
    unittest.main()
