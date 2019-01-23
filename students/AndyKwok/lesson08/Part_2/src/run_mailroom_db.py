


import mailroom_data
import mongodb_mailroom
import neo4j_mailroom
import redis_mailroom
import utilities

def starting_mailroom():

    log = utilities.configure_logger('default', '../logs/nosql_dev.log')
    mailroom = mailroom_data.get_mailroom_db_data()

    log.info("Mailroom database with monogodb")
    mongodb_script.run_mailroom(mailroom)
    log.info("Mailroom database with redis")
    redis_script.run_mailroom()
    log.info("Mailroom database with neo4j")
    neo4j_script.run_mailroom()

if __name__ == '__main__':
    starting_mailroom()