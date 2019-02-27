"""

Integrated example for nosql databases

"""
import learn_data
import mongodb_script
import redis_script
import neo4j_script
import simple_script
import utilities
from simple_script_csv import *

#DefaultVerifyPaths(cafile='/Users/aurelperianu/anaconda3/ssl/cert.pem', capath=None, openssl_cafile_env='SSL_CERT_FILE',
#openssl_cafile='/Users/aurelperianu/anaconda3/ssl/cert.pem',
#openssl_capath_env='SSL_CERT_DIR', openssl_capath='/Users/aurelperianu/anaconda3/ssl/certs')

def showoff_databases():
    """
    Here we illustrate basic interaction with nosql databases
    """
    log = utilities.configure_logger('default', '../logs/nosql_dev.log')

    log.info("Mongodb example to use data from Furniture module, so get it")
    furniture = learn_data.get_furniture_data()

    mongodb_script.run_example(furniture)

    log.info("Other databases use data embedded in the modules")

    redis_script.run_example()
    neo4j_script.run_example()
    #simple_script.run_example(furniture)
    log.info("Run csv simple script")
    run_csv_hw()

if __name__ == '__main__':
    """
    orchestrate nosql examples
    """

    showoff_databases()
