"""
    module that will login to the various demonstration databases consistently
"""

import configparser
from neo4j.v1 import GraphDatabase, basic_auth

config_file = 'config.ini'
config = configparser.ConfigParser()


def login_neo4j_cloud():

    config.read(config_file)

    graphenedb_user = config["neo4j_cloud"]["user"]
    graphenedb_pass = config["neo4j_cloud"]["pw"]
    graphenedb_url = 'bolt://hobby-dgnmcgjedgejgbkedooekccl.dbs.graphenedb.com:24787'
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))

    return driver
