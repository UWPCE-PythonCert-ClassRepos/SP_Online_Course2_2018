import unittest
import collections
import donors_mongoDB as d
import utilities
import login_database
import Load_Tables
log = utilities.configure_logger('default', '../logs/test_dev.log')
people = Load_Tables.get_people_data()


class TestMailbox(unittest.TestCase):

    client = login_database.login_mongodb_cloud()
    log.info('Step 1: We are going to use a database called "test_db"')
    log.info('But if it doesnt exist mongodb creates it')
    db = client['test_db']

    # Delete test.db collection of people first to start fresh
    log.info('First delete the test_collection so we can start over.')
    db.drop_collection('people')

    # Make a new collection called 'people'.
    log.info('In the test_db use a collection called people')
    log.info('If it doesnt exist mongodb creates it')
    people_collection = db['people']

# Load the collection 'test_people' from the Load_Tables.py file.
    log.info('Populate the database with people. MongoDB is non-relational so'
             'the donors and the donations should be kept together.')
    people_collection.insert_many(people)
    log.info('Completed loading donors')

    def test_Connection(self):
        # with login_database.login_mongodb_cloud() as client:
        log.info('Find the person Zach')
        query = {'donor': 'Zach'}
        results = self.__class__.people_collection.find_one(query)
        self.assertEqual(results['donor'], 'Zach')  # Test donor was added

    def test_Individual_Add_Donation1(self):
        """Test Add_Donation when donor does not exist"""
        # pass db instance to Individulal Class Instance
        individual = d.Individual(self.__class__.people_collection)
        individual.add_donation('Luke', 5)
        result = self.__class__.people_collection.find_one({"donor": "Luke"})
        aperson = result['donor']
        adonation = result['donations']
        self.assertEqual(aperson, 'Luke')  # Test donor was added
        self.assertEqual(adonation[0], 5)  # Test donation was added for Luke

    def test_Individual_Add_Donation2(self):
        """Test Add_Donation when it is an existing donor."""
        # pass db instance to Individulal Class Instance
        individual = d.Individual(self.__class__.people_collection)
        individual.add_donation('Shane', 500)
        result = self.__class__.people_collection.find_one({"donor": "Shane"})
        aperson = result['donor']
        adonation = result['donations']
        self.assertEqual(aperson, 'Shane')  # Test donor was added
        self.assertEqual(adonation, [6, 5, 10, 500])  # Test donation was added for Luke

    def test_Count(self):
        """Test that there is only one Shane in database"""
        # pass db instance to Individulal Class Instance
        count = self.__class__.people_collection.count_documents({'donor': 'Shane'})
        self.assertEqual(count, 1)

    def test_Number_Donations(self):
        """Test Individual.Number_of_Donations"""
        individual = d.Individual(self.__class__.people_collection)
        number = individual.number_donations('Shane')
        result = self.__class__.people_collection.find_one({"donor": "Shane"})
        donations = result['donations']
        self.assertEqual(number, len(donations))

    def test_Sum_Donations(self):
        """Test Individual.Sum_Donations"""
        individual = d.Individual(self.__class__.people_collection)
        result = self.__class__.people_collection.find_one({"donor": "Joe"})
        sum_ind = sum(result['donations'])
        log.info(f"The sum of Joe's donations is {sum_ind}")
        self.assertEqual(sum_ind, individual.sum_donations('Joe'))

    def test_AVG_Donations(self):
        """Test Individual.avg_Donations"""
        individual = d.Individual(self.__class__.people_collection)
        result = self.__class__.people_collection.find_one({"donor": "Joe"})
        sum_ind = sum(result['donations'])
        len_ind = len(result['donations'])
        log.info(f"The average of Joe's donations is {sum_ind/len_ind}")
        self.assertEqual(sum_ind/len_ind, individual.avg_donations('Joe'))

    def test_Last_Donation(self):
        """Test Individual.last_donation"""
        individual = d.Individual(self.__class__.people_collection)
        result = self.__class__.people_collection.find_one({"donor": "Joe"})
        last_donation = result['donations'][-1]
        self.assertEqual(last_donation, individual.last_donation('Joe'))

    def test_delete_donor(self):
        """Test delete_donor"""
        individual = d.Individual(self.__class__.people_collection)
        log.info(f"Show that we can find donor.")
        result = self.__class__.people_collection.find_one({"donor": "Pete"})
        self.assertEqual(result['donor'], 'Pete')
        # Delete the document
        individual.delete_donor('Pete')
        # Show that we can no longer find entry
        result = self.__class__.people_collection.find_one({"donor": "Pete"})
        self.assertEqual(result, None)

    def test_Group_search1(self):
        """Returns None when name does not exist"""
        group = d.Group(self.__class__.people_collection)
        result = group.search('Bob') # Bob is not in database
        self.assertEqual(result, None)

    def test_Group_search2(self):
        """Returns 'name' when name does exist. We start with a new
        collection of people so we know what we start with."""

        group = d.Group(self.__class__.people_collection)
        result = group.search('Shane') # Bob is not in database
        self.assertEqual(result, 'Shane')

    def test_print_donors(self):
        """Prints all the people in the database"""

        # Delete test.db collection of people first to start fresh
        log.info('First delete the test_collection so we can start over.')
        self.__class__.db.drop_collection('people')

        # Make a new collection called 'people'.
        log.info('In the test_db use a collection called people')
        log.info('If it doesnt exist mongodb creates it')
        people_collection = self.__class__.db['people']

        # Load the collection 'test_people' from the Load_Tables.py file.
        log.info('Populate the database with people. MongoDB is non-relational so'
                 'the donors and the donations should be kept together.')
        people_collection.insert_many(people)
        log.info('Completed loading donors')

        # Start the test routine
        group = d.Group(self.__class__.people_collection)
        result = collections.Counter(group.print_donors())
        expected = collections.Counter(['Shane', 'Zach', 'Joe', 'Pete', 'Fitz'])
        self.assertEqual(result, expected)

    def test_summary(self):
        """Test dictionary set with {Donor: Total, number of donations,
#        and average donation amount}"""
        # Delete test.db collection of people first to start fresh
        log.info('First delete the test_collection so we can start over.')
        self.__class__.db.drop_collection('people')

        # Make a new collection called 'people'.
        log.info('In the test_db use a collection called people')
        log.info('If it doesnt exist mongodb creates it')
        people_collection = self.__class__.db['people']

        # Load the collection 'test_people' from the Load_Tables.py file.
        log.info('Populate the database with people.')
        people_collection.insert_many(people)
        log.info('Completed loading donors')

        # Start the test routine
        group = d.Group(self.__class__.people_collection)
        result = group.summary()
        test_against = {'Shane':[21,3,7.0], 'Joe':[15, 5, 3.0],
                      'Zach':[10, 1, 10.0], 'Pete': [15, 2, 7.5],
                      'Fitz':[1,1,1.0]}
        self.assertDictEqual(result, test_against)


class TestRedis(unittest.TestCase):
    # connect to database
    r = login_database.login_redis_cloud()
    # Populate the Redis database
    Load_Tables.populate_redis(r)

    def test_Exists(self):
        """ Test to see if your donor exists in database"""
        result = self.__class__.r.exists('Zach')
        self.assertEqual(result, 1)

        # Test to see if your donor does NOT exist in database
        result = self.__class__.r.exists('John')
        self.assertEqual(result, 0)

    def test_Get_CheckEntry(self):
        """Test that when the database loads,
        first it deletes existing entries"""
        result = self.__class__.r.llen('Zach')
        self.assertEqual(result, 3)

    def test_Get_Email(self):
        """Test that we can collect the email from Zach"""
        result = self.__class__.r.lindex('Zach', 2)
        self.assertEqual(result, 'zg@gmail.com')

    def test_donor_verification(self):
        """Test that we can confirm donor information in Redis"""
        Load_Tables.populate_redis(self.__class__.r)
        result = d.Individual.donor_verification(self.__class__.r, 'Joe')
        self.assertEqual(result, ['Slinger', '677-0182', 'js@gmail.com'])

    def test_update_last_name(self):
        """Test that we can confirm donor information in Redis"""
        Load_Tables.populate_redis(self.__class__.r)
        result = d.Individual.update_last_name(self.__class__.r, 'Joe', 'Sling')
        self.assertEqual(result, ['Sling', '677-0182', 'js@gmail.com'])

    def test_update_telephone(self):
        """Test that we can confirm donor information in Redis"""
        Load_Tables.populate_redis(self.__class__.r)
        result = d.Individual.update_telephone(self.__class__.r, 'Joe', '312-000-0000')
        self.assertEqual(result, ['Slinger', '312-000-0000', 'js@gmail.com'])

    def test_update_email(self):
        """Test that we can confirm donor information in Redis"""
        Load_Tables.populate_redis(self.__class__.r)
        result = d.Individual.update_email(self.__class__.r, 'Joe', 'joe@hotmail.com')
        self.assertEqual(result, ['Slinger', '677-0182', 'joe@hotmail.com'])

    def test_redis_add_new(self):
        """Test that we can confirm donor information in Redis"""
        result = d.Individual.redis_add_new(self.__class__.r, 'Sally',
                                            'Hines',
                                            '847-987-4567',
                                            'sally@hotmail.com'
                                            )
        self.assertEqual(result, ['Hines', '847-987-4567', 'sally@hotmail.com'])

if __name__ == '__main__':
    unittest.main()
