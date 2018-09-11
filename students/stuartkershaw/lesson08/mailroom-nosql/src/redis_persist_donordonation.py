import pprint

import login_database
import utilities

log = utilities.configure_logger('default', '../logs/redisdb.log')

def set_rollup_num_donations(donor, donations):
    try:
        r = login_database.login_redis_cloud()

        log.info('Cache donor number of donations for {} in Redis'.format(donor))

        donor_id = donor.replace(' ', '_').lower()

        r.set('{}_num_donations'.format(donor_id), len(donations))

    except Exception as e:
        print(f'Redis error: {e}')


def set_rollup_sum_donations(donor, donations):
    try:
        r = login_database.login_redis_cloud()

        log.info('Cache donor sum of donations for {} in Redis'.format(donor))

        donor_id = donor.replace(' ', '_').lower()

        r.set('{}_sum_donations'.format(donor_id), sum(donations))

    except Exception as e:
        print(f'Redis error: {e}')


def set_rollup_avg_donations(donor, donations):
    try:
        r = login_database.login_redis_cloud()

        log.info('Cache donor average of donations for {} in Redis'.format(donor))

        donor_id = donor.replace(' ', '_').lower()

        r.set('{}_avg_donations'.format(donor_id), float(format(sum(donations) / len(donations), '.2f')))

    except Exception as e:
        print(f'Redis error: {e}')


def get_num_donations(donor):
    try:
        r = login_database.login_redis_cloud()

        log.info('Get cached number of donations for {} in Redis'.format(donor))

        donor_id = donor.replace(' ', '_').lower()

        return r.get('{}_num_donations'.format(donor_id))

    except Exception as e:
        print(f'Redis error: {e}')


def get_sum_donations(donor):
    try:
        r = login_database.login_redis_cloud()

        log.info('Get cached sum of donations for {} in Redis'.format(donor))

        donor_id = donor.replace(' ', '_').lower()

        return r.get('{}_sum_donations'.format(donor_id))

    except Exception as e:
        print(f'Redis error: {e}')


def get_avg_donations(donor):
    try:
        r = login_database.login_redis_cloud()

        log.info('Get cached average of donations for {} in Redis'.format(donor))

        donor_id = donor.replace(' ', '_').lower()

        return r.get('{}_avg_donations'.format(donor_id))

    except Exception as e:
        print(f'Redis error: {e}')


def delete_donor_donations(donor):
    try:
        r = login_database.login_redis_cloud()

        log.info('Delete cached entries for {} in Redis'.format(donor))

        donor_id = donor.replace(' ', '_').lower()

        r.delete('{}_num_donations'.format(donor_id))
        r.delete('{}_sum_donations'.format(donor_id))
        r.delete('{}_avg_donations'.format(donor_id))

    except Exception as e:
        print(f'Redis error: {e}')