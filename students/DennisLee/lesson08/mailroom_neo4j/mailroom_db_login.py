"""
module that will sign in to the Redis database consistently
"""

import configparser
from pathlib import Path
from neo4j.v1 import GraphDatabase, basic_auth
import mailroom_utilities

LOG = mailroom_utilities.configure_logger(
    'default', '../logs/mailroom_login_neo4j_dev.log'
)
CONFIG_FILE = Path(
    __file__
).parent / '.config/config.ini'

CONFIG = configparser.ConfigParser()


def login_neo4j_cloud():
    """
    connect to neo4j and login
    """
    LOG.info('Here is where we use the connect to neo4j.')
    LOG.info('')

    CONFIG.read(CONFIG_FILE)
    graphenedb_user = CONFIG["neo4j_cloud"]["user"]
    graphenedb_pass = CONFIG["neo4j_cloud"]["pw"]
    graphenedb_url = CONFIG["neo4j_cloud"]["connect"]
    driver = GraphDatabase.driver(
        graphenedb_url, auth=basic_auth(graphenedb_user, graphenedb_pass)
    )
    return driver

NEO4J_CLIENT = login_neo4j_cloud()
LOG.info(f"Neo4j client: {NEO4J_CLIENT}")
