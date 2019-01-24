"""
    module that will login to the various demonstration databases consistently
"""

import configparser
from pathlib import Path
from neo4j.v1 import GraphDatabase, basic_auth
import utilities

log = utilities.configure_logger('default', '../logs/login_databases_dev.log')
config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()


def login_neo4j_cloud():
    """
        connect to neo4j and login
    """

    log.info('Here is where we use the connect to neo4j.')
    log.info('')

    config.read(config_file)

    graphenedb_user = config["neo4j_cloud"]["user"]
    graphenedb_pass = config["neo4j_cloud"]["pw"]
    graphenedb_url = 'bolt://hobby-nejemdojocdngbkeeilgdjcl.dbs.graphenedb.com:24786'
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))

    return driver
