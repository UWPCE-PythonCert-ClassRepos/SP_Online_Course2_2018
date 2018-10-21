"""
Module for querying Mongo
"""
import login_database
import utilities
import sample_data
from bson.objectid import ObjectId

log = utilities.configure_logger('default', './logs/redis_script.log')
sample_data = sample_data.get_data()


class QueriesMongo:
    """ Defines Queries class for interacting with DB """

    # ::: SETUP :::::::::::::::::::::::::::::::::::::::::: #
    @staticmethod
    def setup_data():
        try:
            database = login_database.login_mongodb_cloud()
            log.info('Sample donors added')
            with database as client:
                db = client['mailroom']
                table = db['donors']
                db.drop_collection('donors')
                table.insert_many(sample_data)
                documents = table.find({})
                for d in documents:
                    print(f"{d['first_name']} {d['last_name']}")

        except Exception as e:
            log.info(e)
            return False

    @staticmethod
    def drop_donors():
        try:
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                db.drop_collection('donors')
                log.info('Donors dropped.')
        except Exception as e:
            log.info(e)

    # ::: SEARCH :::::::::::::::::::::::::::::::::::::::::: #
    @staticmethod
    def get_donor_by_last(last_name):
        try:
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                table = db['donors']
                result = table.find_one({'last_name': last_name})
            return result
        except Exception as e:
            log.info(e)

    @staticmethod
    def get_donor_by_id(donor_id):
        try:
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                table = db['donors']
                result = table.find_one({'_id': ObjectId(donor_id)})
            return result
        except Exception as e:
            log.info(e)

    @staticmethod
    def get_donors():
        try:
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                table = db['donors']
                documents = table.find({})
                dl = []
                for d in documents:
                    dl.append(d)
                return dl
        except Exception as e:
            log.info(e)

    # ::: MODIFY :::::::::::::::::::::::::::::::::::::::::: #
    @staticmethod
    def insert_donor(d):
        try:
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                table = db['donors']
                table.insert_one({'first_name': d.first_name,
                                  'last_name': d.last_name,
                                  'email': d.email,
                                  'phone': d.phone,
                                  'zip_code': d.zip_code,
                                  'donations': d.donation})

                result = table.find_one({
                    'first_name': d.first_name,
                    'last_name': d.last_name})

                # rs = "\n{} \n{} \n{} \n{} \n{} \n{}"
                # print(rs.format(
                #     result['first_name'],
                #     result['last_name'],
                #     result['email'],
                #     result['phone'],
                #     result['zip_code'],
                #     result['donations']))

        except Exception as e:
            log.info(e)
            return False

    @staticmethod
    def insert_donation(d, donation):
        try:
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                table = db['donors']
                table.update(
                    {'_id': d['_id']},
                    {'$push': {'donations': donation}})

        except Exception as e:
            log.info(e)

    @staticmethod
    def update_donor(d, ud):
        try:
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                table = db['donors']
                table.update(
                    {'_id': d['_id']},
                    {'$set': {'first_name': ud.first_name,
                              'last_name': ud.last_name,
                              'email': ud.email,
                              'phone': ud.phone,
                              'zip_code': ud.zip_code}})
        except Exception as e:
            log.info(e)

    @staticmethod
    def delete_donor(d):
        """ deletes donor """
        try:
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                table = db['donors']
                table.delete_one({'_id': d['_id']})
        except Exception as e:
            log.info(e)

    # ::: PREPARE :::::::::::::::::::::::::::::::::::::::::: #
    def get_donor_multiple_summary(self):
        try:
            """
            Compiles a list for printing multiple donor summaries
            Called methods establish DB connection
            """
            nl = list()
            documents = self.get_donors()
            for d in documents:
                total = self.donations_total(d) if self.donations_total(d) else 0
                count = self.donations_count(d) if self.donations_count(d) else 0
                average = 0
                if total > 0 and count > 0:
                    average = total / count
                nl.append([d['first_name'], d['last_name'], total, count, average])
            return nl

        except Exception as e:
            log.info(e)

    @staticmethod
    def donations_total(d):
        try:
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                table = db['donors']
                result = table.find_one({'_id': d['_id']})
            return sum(result['donations'])
        except Exception as e:
            log.info(e)
        finally:
            database.close()

    @staticmethod
    def donations_count(d):
        try:
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                table = db['donors']
                result = table.find_one({'_id': d['_id']})
            return len(result['donations'])
        except Exception as e:
            log.info(e)
        finally:
            database.close()

    def get_donor_single_summary(self, d):
        try:
            """
            Compiles a list for printing a single donor summary
            Called methods establish DB connection
            """
            database = login_database.login_mongodb_cloud()
            with database as client:
                db = client['mailroom']
                table = db['donors']
                result = table.find_one({'_id': d['_id']})

            if result:
                nl = list()
                total = self.donations_total(d) if self.donations_total(d) else 0
                count = self.donations_count(d) if self.donations_count(d) else 0
                average = 0
                if total > 0 and count > 0:
                    average = total / count
                nl.append([result['first_name'],
                           result['last_name'],
                           total, count, average])
            return nl

        except Exception as e:
            log.info(e)

# qc = QueriesMongo()
# qc.setup_data(sample_data)
