"""
Module for querying Redis
"""
import login_database
import utilities
from queries_mongo import *  # noqa F403
import ast

log = utilities.configure_logger('default', './logs/redis_script.log')


class QueriesRedis:
    """ Defines Queries class for interacting with DB """

    @staticmethod
    def flush_cache():
        try:
            db = login_database.login_redis_cloud()
            keys = db.keys('*')
            for key in keys:
                db.delete(key)
        except Exception as e:
            log.info(e)

    # ::: POPULATE :::::::::::::::::::::::::::::::::::::::::: #
    def update_cache(self):
        try:
            db = login_database.login_redis_cloud()
            qm = QueriesMongo()  # noqa F403
            dl = qm.get_donors()
            self.flush_cache()

            # format for redis
            nl = []
            for d in dl:
                nl.append([str(d['_id']), {
                    '_id': str(d['_id']),
                    'first_name': d['first_name'],
                    'last_name': d['last_name'],
                    'email': d['email'],
                    'phone': d['phone'],
                    'zip_code': d['zip_code'],
                    'donations': d['donations']
                }])

            # set each donor
            for key, data in nl:
                db.hmset(key, data)

        except Exception as e:
            log.info(e)

    # ::: SEARCH :::::::::::::::::::::::::::::::::::::::::: #
    @staticmethod
    def get_donor_by_last(last_name):
        try:
            db = login_database.login_redis_cloud()
            result = db.hgetall(last_name)
            return result
        except Exception as e:
            log.info(e)

    @staticmethod
    def get_donor_by_id(donor_id):
        try:
            db = login_database.login_redis_cloud()
            result = db.hgetall(donor_id)
            return result
        except Exception as e:
            log.info(e)

    @staticmethod
    def get_donors():
        try:
            db = login_database.login_redis_cloud()
            keys = db.keys('*')
            dl = []
            for key in keys:
                dl.append(db.hgetall(key))
            return dl
        except Exception as e:
            log.info(e)

    # ::: PREPARE :::::::::::::::::::::::::::::::::::::::::: #
    @staticmethod
    def donations_total(d):
        try:
            db = login_database.login_redis_cloud()
            result = db.hgetall(str(d['_id']))
            totals = ast.literal_eval(result['donations'])
            return sum(totals)
        except Exception as e:
            log.info(e)

    @staticmethod
    def donations_count(d):
        try:
            db = login_database.login_redis_cloud()
            result = db.hgetall(str(d['_id']))
            count = ast.literal_eval(result['donations'])
            return len(count)
        except Exception as e:
            log.info(e)

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

    def get_donor_single_summary(self, d):
        try:
            """
            Compiles a list for printing a single donor summary
            Called methods establish DB connection
            """
            db = login_database.login_redis_cloud()
            result = db.hgetall(str(d['_id']))

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
