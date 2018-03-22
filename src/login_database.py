"""
    module that will login to the various demnstartion databases consistently

"""

import configparser
from pathlib import Path
import pymongo


def get_credentials(instance_name):
    """
        database credentials stored outside of git with .gitignore
        user, pw and connect string (all in one place)
        NOTE: proabably unsafe! Not encrypted on local machine!

    """
    CONFIG_FILE = Path(__file__).parent.parent / '.config/config.ini'
    config = configparser.ConfigParser()

    try:
        config.read(CONFIG_FILE)
        user = config["mongodb_cloud"]["user"]
        pw = config["mongodb_cloud"]["pw"]
        connection = config["mongodb_cloud"]["connection"]
        return (user, pw, connection)

    except Exception as e:
        print(f'error: {e}')


def login_mongodb_cloud(credentials):
    """
        connect to mongodb and login
    """

#    logger.info('Here is where we use the connect to mongodb.')
#    logger.info(
#        'Note use of f string to embed the user & password (from the tuple).')

    client = pymongo.MongoClient(f'mongodb://{credentials[0]}:{credentials[1]}'
                                 '@cluster0-shard-00-00-wphqo.mongodb.net:27017,'
                                 'cluster0-shard-00-01-wphqo.mongodb.net:27017,'
                                 'cluster0-shard-00-02-wphqo.mongodb.net:27017/test'
                                 '?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin')

    return client


def login_redis_cloud(credentials):
    """
        connect to redis and login
    """

#    logger.info('Here is where we use the connect to redis.')
#    logger.info('')
    r = redis.StrictRedis(host=host, port=port,
                          password=redis_pw, decode_responses=True)
    return r


def login_neo4j_cloud(credentials):
    """
        connect to neo4j and login

    """

#    logger.info('Here is where we use the connect to neo4j.')
#    logger.info('')

    config = ConfigParser()
    config.read(CONFIG)

    graphenedb_user = config["configuration"]["neo4juser"]
    graphenedb_pass = config["configuration"]["neo4jpw"]
    # graphenedb_url = 'bolt://hobby-opmhmhgpkdehgbkejbochpal.dbs.graphenedb.com:24786'
    graphenedb_url = 'bolt://hobby-khhgnhgpkdehgbkeoldljpal.dbs.graphenedb.com:24786'

    driver = GraphDatabase.driver(graphenedb_url,
                                  auth=basic_auth(graphenedb_user, graphenedb_pass))

    return driver
