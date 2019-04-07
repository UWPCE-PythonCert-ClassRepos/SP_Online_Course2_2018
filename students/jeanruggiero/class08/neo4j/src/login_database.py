"""
    module that will login to neo4j
"""

import configparser
from pathlib import Path
from neo4j.v1 import GraphDatabase, basic_auth


config_file = Path(__file__).parent.parent / '.config/config.ini'
config = configparser.ConfigParser()


def login_neo4j_cloud():
    """
        connect to neo4j and login
    """

    config.read(config_file)

    graphenedb_user = config["neo4j_cloud"]["user"]
    graphenedb_pass = config["neo4j_cloud"]["pw"]
    graphenedb_url = "bolt://hobby-hegikgbadkkkgbkedcfoiacl.dbs.graphenedb.com:24787"
    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))

    return driver

